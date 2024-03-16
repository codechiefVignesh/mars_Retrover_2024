#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/mazerover/src/mazerover/maze_bot_control"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/mazerover/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/mazerover/install/lib/python3/dist-packages:/mazerover/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/mazerover/build" \
    "/usr/bin/python3" \
    "/mazerover/src/mazerover/maze_bot_control/setup.py" \
     \
    build --build-base "/mazerover/build/mazerover/maze_bot_control" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/mazerover/install" --install-scripts="/mazerover/install/bin"

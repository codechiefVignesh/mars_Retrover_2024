execute_process(COMMAND "/mazerover/build/mazerover/maze_bot_control/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/mazerover/build/mazerover/maze_bot_control/catkin_generated/python_distutils_install.sh) returned error code ")
endif()

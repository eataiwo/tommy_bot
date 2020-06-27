# CMake generated Testfile for 
# Source directory: /home/pi/Github/Dexter_ROS/src/vision_opencv/image_geometry/test
# Build directory: /home/pi/Github/Dexter_ROS/build/vision_opencv/image_geometry/test
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(_ctest_image_geometry_nosetests_directed.py "/home/pi/Github/Dexter_ROS/build/catkin_generated/env_cached.sh" "/usr/bin/python3" "/opt/ros/noetic/share/catkin/cmake/test/run_tests.py" "/home/pi/Github/Dexter_ROS/build/test_results/image_geometry/nosetests-directed.py.xml" "--return-code" "\"/usr/bin/cmake\" -E make_directory /home/pi/Github/Dexter_ROS/build/test_results/image_geometry" "/usr/bin/nosetests3 -P --process-timeout=60 /home/pi/Github/Dexter_ROS/src/vision_opencv/image_geometry/test/directed.py --with-xunit --xunit-file=/home/pi/Github/Dexter_ROS/build/test_results/image_geometry/nosetests-directed.py.xml")
add_test(_ctest_image_geometry_gtest_image_geometry-utest "/home/pi/Github/Dexter_ROS/build/catkin_generated/env_cached.sh" "/usr/bin/python3" "/opt/ros/noetic/share/catkin/cmake/test/run_tests.py" "/home/pi/Github/Dexter_ROS/build/test_results/image_geometry/gtest-image_geometry-utest.xml" "--return-code" "/home/pi/Github/Dexter_ROS/devel/lib/image_geometry/image_geometry-utest --gtest_output=xml:/home/pi/Github/Dexter_ROS/build/test_results/image_geometry/gtest-image_geometry-utest.xml")

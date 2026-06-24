cmake_minimum_required(VERSION 3.8)
project(lab_3_pkg_tf)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)


install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}/
  )

# Make the python script executable during build/configuration
execute_process(
  COMMAND chmod +x ${CMAKE_CURRENT_SOURCE_DIR}/scripts/orientation_analysis.py
)

# Install Python scripts as programs so they are marked as executable and put in the target's bin path
install(PROGRAMS
  scripts/orientation_analysis.py
  DESTINATION lib/${PROJECT_NAME}
)
  
ament_package()

cmake_minimum_required(VERSION 3.8)
project(lab_2_turtle_patrol)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(turtlesim REQUIRED)
find_package(std_srvs REQUIRED)
# find_package(lab_2_turtle_patrol REQUIRED)

find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/RobotStatus.msg"
  DEPENDENCIES geometry_msgs # Add packages that above messages depend on, in this case geometry_msgs for Sphere.msg
)


# needed if msg is in same package
rosidl_get_typesupport_target(
  cpp_typesupport_target
  ${PROJECT_NAME}
  "rosidl_typesupport_cpp"
)



add_executable(status_publisher src/status_publisher.cpp)
ament_target_dependencies(status_publisher rclcpp std_msgs geometry_msgs turtlesim std_srvs )

add_executable(patrol_controller src/patrol_controller.cpp)
ament_target_dependencies(patrol_controller rclcpp std_msgs geometry_msgs turtlesim std_srvs )


# needed if msg is in same package
target_link_libraries(status_publisher
  ${cpp_typesupport_target}
)


install(TARGETS status_publisher
  DESTINATION lib/${PROJECT_NAME})

install(TARGETS patrol_controller
  DESTINATION lib/${PROJECT_NAME})

install(DIRECTORY
  launch
  params
  DESTINATION share/${PROJECT_NAME}/
  )

ament_package()

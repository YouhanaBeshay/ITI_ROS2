cmake_minimum_required(VERSION 3.8)
project(welcome_back)


# Default to C++17
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)


add_executable(pub_a src/pub_a.cpp)
ament_target_dependencies(pub_a rclcpp std_msgs)



add_executable(sum_sub src/sum_sub.cpp)
ament_target_dependencies(sum_sub rclcpp std_msgs)

add_executable(thermal_pub src/thermal_pub.cpp)
ament_target_dependencies(thermal_pub rclcpp std_msgs)

add_executable(vel_limiter src/vel_limiter.cpp)
ament_target_dependencies(vel_limiter rclcpp geometry_msgs)

add_executable(odom_simulation src/odom_simulation.cpp)
ament_target_dependencies(odom_simulation rclcpp nav_msgs)


install(TARGETS pub_a
                sum_sub
                thermal_pub
                vel_limiter
                odom_simulation
  DESTINATION lib/${PROJECT_NAME}
  )

install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
  )


ament_package()

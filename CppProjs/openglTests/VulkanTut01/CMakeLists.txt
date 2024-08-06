cmake_minimum_required(VERSION 3.10)
project(Tut01)

add_executable(main01 main.cpp first_app.cpp lve_window.cpp)
target_link_libraries(main01 glfw glad vulkan-1)

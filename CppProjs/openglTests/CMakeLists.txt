cmake_minimum_required(VERSION 3.10)
project(openglTestsO)

include_directories(${PROJECT_SOURCE_DIR}/glad-3.3/include/)
include_directories(${PROJECT_SOURCE_DIR}/glfw-3.4/include/)
include_directories(${PROJECT_SOURCE_DIR}/glm-1.0.1/)
include_directories(${PROJECT_SOURCE_DIR}/include/)
include_directories(${PROJECT_SOURCE_DIR}/VulklanSDK/Include/)

link_directories(${PROJECT_SOURCE_DIR}/VulklanSDK/Lib/)

configure_file(${PROJECT_SOURCE_DIR}/include/learnopengl/root_directory.h.in ${PROJECT_SOURCE_DIR}/include/learnopengl/root_directory.h)

add_library(glad ${PROJECT_SOURCE_DIR}/glad-3.3/src/glad.c)

add_subdirectory(glfw-3.4)
add_subdirectory(glm-1.0.1)

add_executable(window window.cpp)
target_link_libraries(window glfw glad)

add_executable(firdemo firstdemo.cpp)
target_link_libraries(firdemo glad glfw -static -static-libgcc -static-libstdc++)

add_executable(vulktes vulkan.cpp)
target_link_libraries(vulktes glfw glad vulkan-1 -static -static-libgcc -static-libstdc++)

add_subdirectory(VulkanTut01)
add_subdirectory(tutorial05)

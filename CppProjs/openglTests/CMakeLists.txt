cmake_minimum_required(VERSION 3.10)
project(openglTestsO)

include_directories(${PROJECT_SOURCE_DIR}/glad-4.3/include/)
include_directories(${PROJECT_SOURCE_DIR}/glfw-3.4/include/)
include_directories(${PROJECT_SOURCE_DIR}/glm-1.0.1/)
include_directories(${PROJECT_SOURCE_DIR}/include/)
include_directories(${PROJECT_SOURCE_DIR}/VulklanSDK/Include/)
include_directories(${PROJECT_SOURCE_DIR}/unexisgl/include)

link_directories(${PROJECT_SOURCE_DIR}/VulklanSDK/Lib/)

configure_file(${PROJECT_SOURCE_DIR}/include/learnopengl/root_directory.h.in ${PROJECT_SOURCE_DIR}/include/learnopengl/root_directory.h)

add_library(glad ${PROJECT_SOURCE_DIR}/glad-4.3/src/glad.c)

# set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)
aux_source_directory(${PROJECT_SOURCE_DIR}/unexisgl/src unexisgl_src)
add_library(unexisgl ${unexisgl_src})
target_link_libraries(unexisgl glfw glad)

add_subdirectory(glfw-3.4)
add_subdirectory(glm-1.0.1)

add_executable(window window.cpp)
target_link_libraries(window glfw glad)

add_executable(firdemo firstdemo.cpp)
target_link_libraries(firdemo glad glfw unexisgl -static -static-libgcc -static-libstdc++)

add_executable(testwindow testClaswindao.cpp)
target_link_libraries(testwindow unexisgl -static -static-libgcc -static-libstdc++)

add_executable(vulktes vulkan.cpp)
target_link_libraries(vulktes glfw glad vulkan-1 -static -static-libgcc -static-libstdc++)

add_subdirectory(VulkanTut01)
add_subdirectory(tutorial05)

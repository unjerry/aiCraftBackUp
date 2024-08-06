cmake_minimum_required(VERSION 3.10)
project(Tut05)

include_directories(${PROJECT_SOURCE_DIR}/include/)
# file(SRC_FILES ${PROJECT_SOURCE_DIR}/src/*.cpp)
add_library(tut05l  ${PROJECT_SOURCE_DIR}/src/first_app.cpp 
                    ${PROJECT_SOURCE_DIR}/src/lve_device.cpp
                    ${PROJECT_SOURCE_DIR}/src/lve_pipeline.cpp 
                    ${PROJECT_SOURCE_DIR}/src/lve_swap_chain.cpp
                    ${PROJECT_SOURCE_DIR}/src/lve_window.cpp)
target_link_libraries(tut05l glfw glad vulkan-1)

add_executable(main05 main.cpp)

target_link_libraries(main05 glfw glad vulkan-1 tut05l)

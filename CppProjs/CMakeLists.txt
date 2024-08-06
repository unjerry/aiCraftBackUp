cmake_minimum_required(VERSION 3.10)

project(UniCpp)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(LIBRARY_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/lib)

add_subdirectory(basicTests)
add_subdirectory(openglTests)

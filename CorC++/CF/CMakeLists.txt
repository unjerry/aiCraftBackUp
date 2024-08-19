cmake_minimum_required(VERSION 3.10)
project(CF)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)

set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR}/bin)
set(IOFILES_PATH ${CMAKE_SOURCE_DIR}/iofiles)
set(SEC_PATH ${CMAKE_SOURCE_DIR}/src)

file(COPY ${IOFILES_PATH}/ DESTINATION ${EXECUTABLE_OUTPUT_PATH})

add_executable(ECR169A ${SEC_PATH}/Educational_Codeforces_Round_169_A.cpp)
add_executable(ECR169B ${SEC_PATH}/Educational_Codeforces_Round_169_B.cpp)
add_executable(ECR169C ${SEC_PATH}/Educational_Codeforces_Round_169_C.cpp)

cmake_minimum_required(VERSION 3.14)
project(set)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage")
set(CMAKE_LINKER_FLAGS "${CMAKE_LINKER_FLAGS} -fprofile-arcs -ftest-coverage")

include_directories(include)

add_executable(set_app main.cpp src/Set.cpp)

enable_testing()
find_package(GTest REQUIRED)
add_executable(set_tests tests/set_tests.cpp src/Set.cpp)
target_link_libraries(set_tests GTest::gtest GTest::gtest_main pthread)

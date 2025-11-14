cmake_minimum_required(VERSION 3.14)
project(markov_algorithm)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Всегда включаем флаги покрытия
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fprofile-arcs -ftest-coverage")
set(CMAKE_LINKER_FLAGS "${CMAKE_LINKER_FLAGS} -fprofile-arcs -ftest-coverage")

include_directories(include)

file(GLOB SOURCES "src/*.cpp")

enable_testing()
find_package(GTest REQUIRED)

add_executable(markov_tests tests/markov_algorithm_tests.cpp ${SOURCES})
target_link_libraries(markov_tests GTest::gtest GTest::gtest_main pthread)

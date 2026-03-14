cmake_minimum_required(VERSION 3.10)
project(lab1_cpp)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)


set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -fprofile-arcs -ftest-coverage")
set(CMAKE_EXE_LINKER_FLAGS_DEBUG "${CMAKE_EXE_LINKER_FLAGS_DEBUG} -fprofile-arcs -ftest-coverage")


add_executable(lab1
    main.cpp
    binary_operations.cpp
    ieee754.cpp
    bcd2421.cpp
)


add_executable(test_runner
    test_runner.cpp
    binary_operations.cpp
    ieee754.cpp
    bcd2421.cpp
)


enable_testing()
add_test(NAME run_tests COMMAND test_runner)

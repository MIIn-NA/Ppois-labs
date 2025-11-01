cmake_minimum_required(VERSION 3.16)
project(SetLib VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

option(ENABLE_COVERAGE "Build with coverage flags" ON)
if(ENABLE_COVERAGE AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  add_compile_options(--coverage -O0 -g)
  add_link_options(--coverage)
endif()

# ===== Library =====
add_library(setlib src/Set.cpp)
target_include_directories(setlib PUBLIC include)

# ===== Manually include and link UnitTest++ =====
# 🟢 make sure headers + lib are visible
include_directories(/usr/local/include /usr/local/include/UnitTest++)
link_directories(/usr/local/lib)

enable_testing()
add_executable(setlib_tests tests/test_set.cpp)

# 🟢 link both your lib and UnitTest++
target_link_libraries(setlib_tests PRIVATE setlib UnitTest++)

add_test(NAME setlib_tests COMMAND setlib_tests)

# ===== Doxygen =====
find_package(Doxygen)
if(DOXYGEN_FOUND)
  add_custom_target(docs
    COMMAND ${DOXYGEN_EXECUTABLE} ${CMAKE_SOURCE_DIR}/Doxyfile
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
    COMMENT "Generating API documentation with Doxygen" VERBATIM)
endif()

cmake_minimum_required(VERSION 3.12)
project(pyfunc_native)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python and pybind11
find_package(Python COMPONENTS Interpreter Development REQUIRED)
find_package(pybind11 REQUIRED)

# Add the pybind11 module
pybind11_add_module(pyfunc_native
    pyfunc/native/operations.cpp
    pyfunc/native/bindings.cpp
)

# Set properties
target_compile_definitions(pyfunc_native PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})

# Optimization flags
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_options(pyfunc_native PRIVATE -O3 -march=native)
endif()

# Enable all warnings
target_compile_options(pyfunc_native PRIVATE -Wall -Wextra)

# Set output directory
set_target_properties(pyfunc_native PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)
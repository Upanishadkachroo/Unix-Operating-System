cmake_minimum_required(VERSION 3.16)

project(OpenCalc VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(opencalc
    src/main.cpp
    src/calculator.cpp
)

target_include_directories(opencalc
    PRIVATE ${PROJECT_SOURCE_DIR}/src
)

install(
    TARGETS opencalc
    RUNTIME DESTINATION bin
)

cmake_minimum_required(VERSION 3.30 )
project(test-papi)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../cmake")
include(base_config)

list(APPEND CMAKE_MODULE_PATH "${NUGGET_C_HOOKS_PATH}")
include(hooks)

add_executable(test-papi hello.c)

target_link_libraries(test-papi ${PAPI_LIB})
target_link_libraries(test-papi papi-naive)



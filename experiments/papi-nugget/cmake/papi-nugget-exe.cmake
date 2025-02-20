list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../cmake")
include(base_config)

list(APPEND CMAKE_MODULE_PATH "${NUGGET_LIBRARY_PATH}")
include(Nugget)

set(TARGET_NAME "papi_nugget_exe")
set(HOOK_TARGET single-threaded-papi-nugget)

set(ALL_NUGGET_RIDS 0 1 2)

set(NUGGET_BC_FILE_DIR
    "${CMAKE_CURRENT_BINARY_DIR}/llvm-bc")

set(NUGGET_BC_FILE_BASENAME
    "papi-nugget-bc")

set(LLC_EXTRATION_FILE_PATH
    "${NUGGET_UTIL_PATH}/cmake/check-cpu-features/llc-command.txt")

    if(LLC_EXTRATION_FILE_PATH AND EXISTS ${LLC_EXTRATION_FILE_PATH})
    nugget_read_list(LLC_CMD ${LLC_EXTRATION_FILE_PATH})
else()
    message(WARNING "LLC command not found in ${LLC_EXTRATION_FILE_PATH}")
endif()

if(LLC_CMD)
    list(APPEND LLC_CMD -relocation-model=pic -O3)
endif()

message(STATUS "LLC_CMD: ${LLC_CMD}")
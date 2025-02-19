list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../cmake")
include(base_config)

set(TARGET_NAME "papi_nugget_exe")
set(HOOK_TARGET single-threaded-papi-nugget)

set(ALL_NUGGET_RIDS 0 1 2)

set(NUGGET_BC_FILE_DIR
    "${CMAKE_CURRENT_BINARY_DIR}/llvm-bc")

set(NUGGET_BC_FILE_BASENAME
    "papi-nugget-bc")

set(LLC_EXTRATION_FILE_PATH
    "${NUGGET_UTIL_PATH}/cmake/check-cpu-features/llc-command.txt")
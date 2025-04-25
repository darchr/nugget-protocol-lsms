list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../cmake")
include(base_config)

list(APPEND CMAKE_MODULE_PATH "${NUGGET_LIBRARY_PATH}")
include(Nugget)

set(TARGET_NAME lsms_m5_naive_exe)
set(HOOK_TARGET m5-naive)

set(BC_FILE_PATH
    "${CMAKE_CURRENT_BINARY_DIR}/llvm-bc/lsms_m5_naive_bc/lsms_m5_naive_bc.bc")

if(NOT EXISTS ${BC_FILE_PATH})
    message(FATAL_ERROR "Analysis BC file not found: ${BC_FILE_PATH}")
endif()

set(LLC_EXTRATION_FILE_PATH
    ${NUGGET_UTIL_PATH}/cmake/check-cpu-features/llc-command.txt)

if(LLC_EXTRATION_FILE_PATH AND EXISTS ${LLC_EXTRATION_FILE_PATH})
    nugget_read_list(LLC_CMD ${LLC_EXTRATION_FILE_PATH})
else()
    message(WARNING "LLC command not found in ${LLC_EXTRATION_FILE_PATH}")
endif()

if(LLC_CMD)
    list(APPEND LLC_CMD -relocation-model=pic -O2)
endif()

list(APPEND EXTRA_FLAGS -no-pie)
set(EXTRA_LIB_PATHS -L${M5_PATH})
set(EXTRA_INCLUDES -I${M5_INCLUDE_PATH})
set(EXTRA_LIBS -lm5)

message(STATUS "LLC_CMD: ${LLC_CMD}")

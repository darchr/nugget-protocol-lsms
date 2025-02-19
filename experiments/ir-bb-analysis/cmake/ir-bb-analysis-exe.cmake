list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../cmake")
include(base_config)

set(LLC_EXTRATION_FILE_PATH
    ${NUGGET_UTIL_PATH}/cmake/check-cpu-features/llc-command.txt)

set(ANALYSIS_BC_FILE_PATH
    "${CMAKE_CURRENT_BINARY_DIR}/llvm-bc/lsms_ir_bb_analysis_bc/lsms_ir_bb_analysis_bc.bc")

if(NOT EXISTS ${ANALYSIS_BC_FILE_PATH})
    message(FATAL_ERROR "Analysis BC file not found: ${ANALYSIS_BC_FILE_PATH}")
endif()

set(TARGET_NAME "lsms_ir_bb_analysis_exe")


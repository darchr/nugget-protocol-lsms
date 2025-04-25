list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../cmake")
include(base_config)

set(TARGET_NAME "lsms_m5_naive_bc")
set(HOOK_TARGET m5-naive)

set(SOURCE_BC_FILE_PATH
    "${CMAKE_CURRENT_BINARY_DIR}/llvm-bc/lsms_ir_bb_analysis_bc_source_opted_bc/lsms_ir_bb_analysis_bc_source_opted_bc.bc")

set(EXTRA_LIB_PATHS -L${M5_PATH})
set(EXTRA_INCLUDES -I${M5_INCLUDE_PATH})
set(EXTRA_LIBS -lm5)

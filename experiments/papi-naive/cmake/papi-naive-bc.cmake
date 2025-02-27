list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../cmake")
include(base_config)

set(TARGET_NAME lsms_papi_naive_bc)
set(HOOK_TARGET papi-naive)

set(SOURCE_BC_FILE_PATH
    "${CMAKE_CURRENT_BINARY_DIR}/llvm-bc/lsms_ir_bb_analysis_bc_source_bc/lsms_ir_bb_analysis_bc_source_bc.bc")


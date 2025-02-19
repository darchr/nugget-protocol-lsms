list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../cmake")
include(base_config)

set(TARGET_NAME "papi_nugget_bc")
set(HOOK_TARGET single-threaded-papi-nugget)

set(SOURCE_BC_FILE_PATH
    "${CMAKE_CURRENT_BINARY_DIR}/llvm-bc/lsms_ir_bb_analysis_bc_source_bc/lsms_ir_bb_analysis_bc_source_bc.bc")

set(INPUT_FILE_DIR
    "${CMAKE_CURRENT_LIST_DIR}/../../nugget-info/input-files")

set(INPUT_FILE_NAME_BASE "-marker.txt")

set(BB_INFO_INPUT_PATH
    "${CMAKE_CURRENT_BINARY_DIR}/bb-info-output/basic-block-info.txt")

set(ALL_NUGGET_RIDS 0 1 2)


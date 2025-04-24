list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../cmake")
include(base_config)

set(TARGET_NAME "lsms_ir_bb_analysis_bc")
set(REGION_LENGTH 100000000)
set(HOOK_TARGET "single-threaded-ir-bb-analysis-balance")

set(OPT_CMD "-O2")

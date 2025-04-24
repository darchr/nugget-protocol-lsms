list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../cmake")
include(base_config)

list(APPEND CMAKE_MODULE_PATH "${NUGGET_LIBRARY_PATH}")
include(Nugget)

set(TARGET_NAME "lsms_papi_nuggets_bc")
set(HOOK_TARGET single-threaded-papi-nugget)

set(SOURCE_BC_FILE_PATH
    "${CMAKE_CURRENT_BINARY_DIR}/llvm-bc/lsms_ir_bb_analysis_bc_source_opted_bc/lsms_ir_bb_analysis_bc_source_opted_bc.bc")

set(INPUT_FILE_DIR
    "${CMAKE_CURRENT_LIST_DIR}/../../info/create-markers/marker-input-files")

set(INPUT_FILE_NAME_BASE "-marker.txt")

set(BB_INFO_INPUT_PATH
    "${CMAKE_CURRENT_LIST_DIR}/../../info/bb-info-output/basic-block-info.txt")

set(NUGGET_RID_FILE
    "${CMAKE_CURRENT_LIST_DIR}/../../info/k-means-selections/selected-regions.txt")

if(NOT EXISTS ${NUGGET_RID_FILE})
    message(FATAL_ERROR "Nugget RID file not found: ${NUGGET_RID_FILE}")
endif()

nugget_read_list(ALL_NUGGET_RIDS ${NUGGET_RID_FILE})

message(STATUS "ALL_NUGGET_RIDS: ${ALL_NUGGET_RIDS}")

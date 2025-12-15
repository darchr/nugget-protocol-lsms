list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../..")
include(base_config)

if (DEFINED ENV{REGION_LENGTH} AND NOT "$ENV{REGION_LENGTH}" STREQUAL "")
    set(REGION_LENGTH "$ENV{REGION_LENGTH}")
else()
    set(REGION_LENGTH "100000000")
endif()

set(TARGET_NAME lsms_ir_bb_analysis_bc)

set(BC_INFO_OUTPUT_DIR ${CMAKE_BINARY_DIR}/ir-bb-analysis-bb-info)

set(OPT_CMD "-O2")

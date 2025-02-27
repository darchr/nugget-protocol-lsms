list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../cmake")
include(base_config)

list(APPEND CMAKE_MODULE_PATH "${NUGGET_LIBRARY_PATH}")
include(Nugget)

set(TARGET_NAME "saphir_papi_nuggets_exe")

set(NUGGET_BC_FILE_DIR
    "${CMAKE_BINARY_DIR}/llvm-bc")

set(NUGGET_BC_FILE_BASENAME
    "saphir_papi_nuggets_bc")

set(NUGGET_RID_FILE
    "${CMAKE_CURRENT_LIST_DIR}/../../info/ir-bb-analysis/comparison/saphir-k-means-selection/selected-regions.txt")

if(NOT EXISTS ${NUGGET_RID_FILE})
    message(FATAL_ERROR "Nugget RID file not found: ${NUGGET_RID_FILE}")
endif()

nugget_read_list(ALL_NUGGET_RIDS ${NUGGET_RID_FILE})

message(STATUS "ALL_NUGGET_RIDS: ${ALL_NUGGET_RIDS}")

set(LLC_EXTRATION_FILE_PATH
    ${NUGGET_UTIL_PATH}/cmake/check-cpu-features/llc-command.txt)

if(LLC_EXTRATION_FILE_PATH AND EXISTS ${LLC_EXTRATION_FILE_PATH})
    nugget_read_list(LLC_CMD ${LLC_EXTRATION_FILE_PATH})
else()
    message(WARNING "LLC command not found in ${LLC_EXTRATION_FILE_PATH}")
endif()

if(LLC_CMD)
    list(APPEND LLC_CMD -relocation-model=pic -O3)
endif()

message(STATUS "LLC_CMD: ${LLC_CMD}")



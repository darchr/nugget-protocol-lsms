list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../cmake")
include(base_config)

list(APPEND CMAKE_MODULE_PATH "${NUGGET_LIBRARY_PATH}")
include(Nugget)

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

set(BB_FILE_PATH
    "${CMAKE_CURRENT_BINARY_DIR}/llvm-bc/lsms_ir_bb_analysis_include_library_bc/lsms_ir_bb_analysis_include_library_bc.bc")

if(NOT EXISTS ${BB_FILE_PATH})
    message(FATAL_ERROR "Analysis BC file not found: ${BB_FILE_PATH}")
endif()

set(TARGET_NAME "lsms_ir_bb_analysis_include_library_exe")

set(INCLUDE_LIBRARIES_IN_BC true)

set(EXTRACT_FUNCTIONS "work_gga_exc_unpol")

set(SHRUNK_BC true)

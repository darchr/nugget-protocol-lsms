list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../..")
include(base_config)

list(APPEND CMAKE_MODULE_PATH "${NUGGET_LIBRARY_PATH}")
include(Nugget)

set(TARGET_NAME lsms_papi_naive_${TARGET_ARCH}_exe)
set(HOOK_TARGET papi-naive)

if (DEFINED ENV{BC_FILE_PATH} AND NOT "$ENV{BC_FILE_PATH}" STREQUAL "")
    set(BC_FILE_PATH $ENV{BC_FILE_PATH})
else()
    message(FATAL_ERROR "Environment variable BC_FILE_PATH must be set")
endif()

if(NOT EXISTS ${BC_FILE_PATH})
    message(FATAL_ERROR "Analysis BC file not found: ${BC_FILE_PATH}")
endif()

set(LLC_EXTRACTION_FILE_PATH
    ${NUGGET_UTIL_PATH}/cmake/check-cpu-features/${TARGET_ARCH}/llc-command.txt)

if(LLC_EXTRACTION_FILE_PATH AND EXISTS ${LLC_EXTRACTION_FILE_PATH})
    nugget_read_list(LLC_CMD ${LLC_EXTRACTION_FILE_PATH})
else()
    message(WARNING "LLC command not found in ${LLC_EXTRACTION_FILE_PATH}")
endif()

if(LLC_CMD)
    list(APPEND LLC_CMD -relocation-model=pic -O2)
else()
    set(LLC_CMD -relocation-model=pic -O2)
endif()

message(STATUS "LLC_CMD: ${LLC_CMD}")

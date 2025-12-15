list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../..")
include(base_config)

list(APPEND CMAKE_MODULE_PATH "${NUGGET_LIBRARY_PATH}")
include(Nugget)

set(TARGET_NAME "papi_nugget_exe")
set(HOOK_TARGET single-threaded-papi-nugget)

set(NUGGET_BC_FILE_DIR
    "${CMAKE_CURRENT_BINARY_DIR}/llvm-bc")

set(NUGGET_BC_FILE_BASENAME
    "papi_nugget_bc")

set(LLC_EXTRACTION_FILE_PATH
    "${NUGGET_UTIL_PATH}/cmake/check-cpu-features/llc-command.txt")

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

# Pull required paths from environment; fail fast if missing.
if (NOT DEFINED ENV{ALL_NUGGET_RIDS_FILE} OR "$ENV{ALL_NUGGET_RIDS_FILE}" STREQUAL "")
	message(FATAL_ERROR "Environment variable ALL_NUGGET_RIDS_FILE must be set")
endif()

set(ALL_NUGGET_RIDS_FILE $ENV{ALL_NUGGET_RIDS_FILE})
if(NOT EXISTS ${ALL_NUGGET_RIDS_FILE})
	message(FATAL_ERROR "ALL_NUGGET_RIDS_FILE ${ALL_NUGGET_RIDS_FILE} does not exist")
endif()
nugget_read_list(ALL_NUGGET_RIDS ${ALL_NUGGET_RIDS_FILE})

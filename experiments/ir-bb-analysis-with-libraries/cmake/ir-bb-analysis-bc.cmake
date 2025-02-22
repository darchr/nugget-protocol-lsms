list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_LIST_DIR}/../../cmake")
include(base_config)

set(REGION_LENGTH 100000000)
set(TARGET_NAME lsms_ir_bb_analysis_include_library_bc)
set(INCLUDE_LIBRARIES_IN_BC true)

list(APPEND EXTRA_FLAGS "-D_longjmp=longjmp" "-D_POSIX_C_SOURCE=200809L")

set(NUGGET_UTIL_PATH "${CMAKE_CURRENT_LIST_DIR}/../../nugget_util")

set(NUGGET_LIBRARY_PATH "${NUGGET_UTIL_PATH}/cmake")
set(NUGGET_HOOKS_PATH "${NUGGET_UTIL_PATH}/hook_helper")
set(NUGGET_C_HOOKS_PATH "${NUGGET_HOOKS_PATH}/c_hooks")

set(PAPI_PATH "${NUGGET_HOOKS_PATH}/other_tools/papi/aarch64")
set(M5_PATH "${NUGGET_HOOKS_PATH}/other_tools/gem5/arm64")
set(M5_INCLUDE_PATH "${NUGGET_HOOKS_PATH}/other_tools/gem5/include")

# set if we should use addr mop m5 ops in the beginning and end of the ROI
# for
set(IF_USE_ADDR_VERSION_M5OPS_BEGIN TRUE)
set(IF_USE_ADDR_VERSION_M5OPS_END TRUE)


set(LLVM_ROOT "/home/ztpc/compiler/llvm-dir")
set(LLVM_BIN "${LLVM_ROOT}/bin")

set(MPI_INCLUDES
    -I/usr/lib/x86_64-linux-gnu/openmpi/include
    -I/usr/lib/x86_64-linux-gnu/openmpi/include/openmpi
)

set(MPI_LIB_PATHS
    -L/usr/lib/x86_64-linux-gnu/openmpi/lib
)

set(MPI_LIBS
    -lmpi_cxx
    -lmpi
)

set(Fortran_LIB_PATHS
    -L${LLVM_ROOT}/lib
)

set(Fortran_LIBS
    -lgfortran 
    -lFortranRuntime 
    -lFortranDecimal 
    -lFortran_main 
    -lflangFrontend 
)

set(PAPI_LIB "${NUGGET_HOOKS_PATH}/other_tools/papi/x86_64/lib/libpapi.a")

set(EXTRA_FLAGS "-DUSE_NUGGET_LIB")
set(EXTRA_LIBS ${MPI_LIBS} ${Fortran_LIBS} ${PAPI_LIB})
set(EXTRA_LIB_PATHS ${MPI_LIB_PATHS} ${Fortran_LIB_PATHS})
set(EXTRA_INCLUDES ${MPI_INCLUDES})

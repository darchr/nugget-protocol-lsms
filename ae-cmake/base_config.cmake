# Prefer environment overrides when present, otherwise fall back to defaults.
if(DEFINED ENV{NUGGET_UTIL_PATH} AND NOT "$ENV{NUGGET_UTIL_PATH}" STREQUAL "")
	set(NUGGET_UTIL_PATH "$ENV{NUGGET_UTIL_PATH}")
else()
	set(NUGGET_UTIL_PATH "${CMAKE_CURRENT_LIST_DIR}/../../nugget_util")
endif()

# Check the architecture of the target system.
if(CMAKE_SYSTEM_PROCESSOR MATCHES "aarch64")
	set(TARGET_ARCH "aarch64")
	set(GEM5_ABI "arm64")
elseif(CMAKE_SYSTEM_PROCESSOR MATCHES "x86_64")
	set(TARGET_ARCH "x86_64")
	set(GEM5_ABI "x86")
else()
	message(FATAL_ERROR "Unsupported target architecture: ${CMAKE_SYSTEM_PROCESSOR}")
endif()

set(NUGGET_LIBRARY_PATH "${NUGGET_UTIL_PATH}/cmake")
set(NUGGET_HOOKS_PATH "${NUGGET_UTIL_PATH}/hook_helper")
set(NUGGET_C_HOOKS_PATH "${NUGGET_HOOKS_PATH}/c_hooks")

set(PAPI_PATH "${NUGGET_HOOKS_PATH}/other_tools/papi/${TARGET_ARCH}")
set(M5_PATH "${NUGGET_HOOKS_PATH}/other_tools/gem5/${GEM5_ABI}")
set(M5_INCLUDE_PATH "${NUGGET_HOOKS_PATH}/other_tools/gem5/include")

if(DEFINED ENV{LLVM_DIR} AND NOT "$ENV{LLVM_DIR}" STREQUAL "")
	set(LLVM_DIR "$ENV{LLVM_DIR}")
else()
	set(LLVM_DIR "${CMAKE_CURRENT_LIST_DIR}/../../llvm-dir")
endif()
set(LLVM_BIN "${LLVM_DIR}/bin")

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

set(PAPI_LIB "${PAPI_PATH}/lib/libpapi.a")

set(EXTRA_FLAGS "-DUSE_NUGGET_LIB")
set(EXTRA_LIBS ${MPI_LIBS} ${Fortran_LIBS} ${PAPI_LIB})
set(EXTRA_LIB_PATHS ${MPI_LIB_PATHS} ${Fortran_LIB_PATHS})
set(EXTRA_INCLUDES ${MPI_INCLUDES})

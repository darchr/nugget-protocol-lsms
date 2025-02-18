An example of creating the ir bbv profiling bc with lsms

```
mkdir cbuild && cd cbuild
NUGGET_PROCESS_TYPE=lsms-ir-bb-analysis-bc cmake -DCMAKE_TOOLCHAIN_FILE=${PWD}/../lsms/toolchain/generic-cpu.cmake \
    ${PWD}/../lsms
cmake --build . --target=lsms_ir_bb_analysis_bc
```

You might need to change some parameters in `lsms/cmake/nugget-ir-bb-analysis-bc.cmake`, such as `set(LLVM_ROOT "[path/to/llvm/root]")`.

More details to come

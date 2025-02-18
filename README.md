An example of creating the ir bbv profiling bc with lsms

```
mkdir cbuild && cd cbuild
cmake -DCMAKE_TOOLCHAIN_FILE=${PWD}/../lsms/toolchain/nugget-generic-cpu.cmake \
    ${PWD}/../lsms
cmake --build . --target=lsms_ir_bb_analysis_bc
```

More details to come

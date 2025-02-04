# Nugget Protocol of lsms

This version of `lsms` uses a custom `llvm-ir-cmake-utils` to produce LLVM IR that is necessary for the Nugget methodology while continue using the original cmake process.

The way to compile:
```
mkdir cbuild
cd cbuild
CC=[path/to/llvm/bin]/clang CXX=[path/to/llvm/bin]/clang++ cmake ..
```

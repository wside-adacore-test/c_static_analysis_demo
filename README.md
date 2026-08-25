[![Board Status](https://dev.azure.com/wside/6d75b3c8-8faa-4376-bd41-055114e60eec/0208637f-2ad0-4d08-b6b3-01a883dd7a82/_apis/work/boardbadge/19b99bf2-52dd-49e8-9b5f-21f5b15dd667)](https://dev.azure.com/wside/6d75b3c8-8faa-4376-bd41-055114e60eec/_boards/board/t/0208637f-2ad0-4d08-b6b3-01a883dd7a82/Microsoft.RequirementCategory)
# C Static Analysis Test Project

This repository contains a C project intended for testing static code analysis tools (such as CodeSonar).

## Included Files
- `buffer.h` / `buffer.c`: Buffer allocation and string manipulation module containing pointer and allocation flaws.
- `math_utils.h` / `math_utils.c`: Math and logging helper module containing overflow, out-of-bounds, and file handle leaks.
- `main.c`: Entry point demonstrating calls that trigger static analysis warnings.
- `Makefile`: Build instructions for `gcc`.

## Quick Build
```bash
make
./c_bugs_demo
```

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

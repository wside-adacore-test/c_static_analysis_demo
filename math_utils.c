#include "math_utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <limits.h>

int divide_numbers(int a, int b) {
    /* Bug 9: Division by Zero 
       Does not check if 'b' is zero before performing division. */
    return a / b;
}

int calculate_square(int n) {
    /* Bug 10: Integer Overflow Hazard 
       n * n can easily exceed INT_MAX without any bounds check or promotion. */
    return n * n;
}

int process_array(const int *arr, size_t count) {
    int sum = 0;
    
    /* Bug 11: Out-of-Bounds Read / Off-by-One Loop Condition 
       Using '<=' instead of '<' reads past the end of the array by 1 element. */
    for (size_t i = 0; i <= count; i++) {
        sum += arr[i];
    }
    
    return sum;
}

void write_log_entry(const char *filename, const char *message) {
    FILE *f = fopen(filename, "a");
    
    /* Bug 12: Unchecked File Pointer Dereference 
       If fopen fails (returns NULL), fprintf will crash dereferencing 'f'. */
    fprintf(f, "LOG: %s\n", message);

    /* Bug 13: Resource Leak (Missing fclose) 
       The open file handle 'f' is never closed before returning. */
}

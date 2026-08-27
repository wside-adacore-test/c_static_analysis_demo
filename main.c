#include "buffer.h"
#include "math_utils.h"
#include <stdio.h>
#include <limits.h>

void process_data(int mode) {
    char *ptr = NULL;

    if (mode > 5) {
        ptr = "High Mode";
    }

    /* Bug 6: Conditional Null Pointer Dereference */
    if (mode != 0) {
        char first_char = *ptr;
        printf("Mode String: %s\n", first_char); 
    }
}

int main() {
    /* --- Buffer Module Tests --- */
    StringBuffer *my_buf = create_buffer(10);
    append_string(my_buf, "Hello World!!"); /* Triggers Bug 4 */
    print_buffer(my_buf);

    free_buffer(my_buf);
    free_buffer(my_buf); /* Bug 7: Double Free */

    StringBuffer *leaked_buf = create_buffer(32); /* Bug 8: Memory Leak */
    (void)leaked_buf;

    /* --- Math Utils Module Tests --- */
    int numbers[3] = {10, 20, 30};
    int total = process_array(numbers, 3); /* Triggers Bug 11 (Out-of-bounds) */
    printf("Array total: %d\n", total);

    int sq = calculate_square(INT_MAX); /* Triggers Bug 10 (Integer Overflow) */
    printf("Square result: %d\n", sq);

    write_log_entry("/non_existent_directory/log.txt", "Test log"); /* Triggers Bugs 12 & 13 */

    int div = divide_numbers(10, 0); /* Triggers Bug 9 (Division by Zero) */
    printf("Division result: %d\n", div);

    //process_data(2); /* Triggers Bug 6 */

    return 0;
}

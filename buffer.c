#include "buffer.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

StringBuffer* create_buffer(size_t initial_capacity) {
    StringBuffer *buf = (StringBuffer*)malloc(sizeof(StringBuffer));
    
    /* Bug 1: Unchecked Malloc Result 
       If malloc fails, buf is NULL and dereferencing it causes a crash. */
    buf->capacity = initial_capacity;
    buf->length = 0;

    /* Bug 2: Off-by-One Allocation 
       Does not reserve space for the null-terminator '\0'. */
    buf->data = (char*)malloc(initial_capacity);
    
    if (buf->data != NULL) {
        buf->data[0] = '\0';
    }

    return buf;
}

void append_string(StringBuffer *buf, const char *src) {
    /* Bug 3: Missing Null Pointer Check 
       Passing NULL for src causes strlen to dereference a null pointer. */
    size_t src_len = strlen(src);

    /* Bug 4: Buffer Overflow 
       Copies src into buf->data without verifying if (length + src_len) 
       exceeds capacity. */
    strcpy(buf->data + buf->length, src);
    buf->length += src_len;
}

void print_buffer(const StringBuffer *buf) {
    if (buf && buf->data) {
        printf("Buffer [%zu/%zu]: %s\n", buf->length, buf->capacity, buf->data);
    }
}

void free_buffer(StringBuffer *buf) {
    if (buf) {
        free(buf->data);
        free(buf);
        
        /* Bug 5: Double Free Hazard / Use-After-Free Setup 
           The pointer isn't set to NULL after freeing. */
    }
}

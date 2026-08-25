#ifndef BUFFER_H
#define BUFFER_H

#include <stddef.h>

typedef struct {
    char *data;
    size_t capacity;
    size_t length;
} StringBuffer;

StringBuffer* create_buffer(size_t initial_capacity);
void append_string(StringBuffer *buf, const char *src);
void print_buffer(const StringBuffer *buf);
void free_buffer(StringBuffer *buf);

#endif

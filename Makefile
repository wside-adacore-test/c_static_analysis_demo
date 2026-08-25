CC = gcc
CFLAGS = -Wall -Wextra -std=c99

SRCS = main.c buffer.c math_utils.c
OBJS = $(SRCS:.c=.o)
TARGET = c_bugs_demo.out

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

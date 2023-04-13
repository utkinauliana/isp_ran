#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>

void char_to_int(char *buf) {
    int number_first;
    number_first = *(int *) buf;
    if (number_first == 0x12345678) {
        exit(2);
    } else {
        exit(4);
    }
}


int main(int argc, char *argv[]) {
    int fd;
    fd = open(argv[1], O_RDONLY);
    char buf[256] = {};
    int size = lseek(fd, 0, SEEK_END);
    lseek(fd, 0, SEEK_SET);
    read(fd, buf, size);
    printf("%s\n", buf);
    char_to_int(buf);
    return 0;
}
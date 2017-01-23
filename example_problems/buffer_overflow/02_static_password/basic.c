#include <stdlib.h>
#include <stdio.h>

/*
    This app has a password declared in the code.
    It also suffers from the same buffer overflow that the rest do.
  an input that overflows the buffer will write into the password to expect
  Sample input: 123456781234567812345678
*/

void my_gets(char *destination) {
  int b;
  b = getchar();
  while (b != '\n' && b != EOF) {
    *destination++ = (char)b;
    b = getchar();
  }
}


int main(int argc, char *argv[]) {
  char flag[32] = "NOT_THE_FLAG";
  char buffer[15];
  char password[15] = "18atcskd2w";
  FILE *f;

  f = fopen("flag.txt", "r");
  if (f) {
    fgets(flag, 32, f);
    fclose(f);
  }

  printf("Enter password to get flag: ");
  fflush(stdout);
  my_gets(buffer);
  if (memcmp(buffer, password, 15) == 0) {
    printf("Password Accepted\nFlag = %s\n", flag);
  } else {
    printf("Wrong password\n");
  }
  return 0;
}

#include <stdlib.h>
#include <stdio.h>

/*
    This app doesn't validate input, and allows the input to overflow into the password to check.
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
  char flag[32];
  char buffer[9];
  char password[9];
  FILE *f;

  f = fopen("flag.txt", "r");
  fgets(flag, 32, f);
  fclose(f);

  f = fopen("password.txt", "r");
  fgets(password, 9, f);
  fclose(f);

  printf("Enter password to get flag: ");
  fflush(stdout);
  my_gets(buffer);
  if (memcmp(buffer, password, 8) == 0) {
    printf("Password Accepted\nFlag = %s\n", flag);
  } else {
    printf("Wrong password\n");
  }
  return 0;
}

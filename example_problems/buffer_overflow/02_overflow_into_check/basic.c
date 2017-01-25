#include <stdlib.h>
#include <stdio.h>

/*
    This app doesn't validate input, and allows the input to overflow into the password to check.
  an input that overflows the buffer will write into the password to expect
  Sample input: 12345678123456781234567812345678
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
  char password[15] = "Sh4rp13";
  FILE *f;

  f = fopen("flag.txt", "r");
  if (f) {
    fgets(flag, 32, f);
    fclose(f);
  }

  f = fopen("password.txt", "r");
  if (f) {
    fgets(password, 15, f);
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

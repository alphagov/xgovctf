#include <stdlib.h>
#include <stdio.h>

/*
  Deliberately vulnerable app 2
  This app implements their own gets that doesn't terminate the string
  OVerflowing the buffer causes the flag to be printed

  Sample:
  Enter password to get flag: 1234567812345678
1234567812345678flag_4_f1a9
 is not the password
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
  char buffer[15];
  char password[15] = "P0stIt!";
  char flag[32] = "NOT_THE_FLAG";
  FILE *f;

  memset(buffer, 0, 15);

  f = fopen("flag.txt", "r");
  if (f) {
    fgets(flag, 32, f);
    fclose(f);
  }

  f = fopen("password.txt", "r");
  if (f) {
    fscanf(f, "%s", password);
    fclose(f);
  }

  printf("Enter password to get flag: ");
  fflush(stdout);
  my_gets(buffer);
  // dump_memory(buffer, 4);
  if (strcmp(buffer, password) == 0) {
    printf("Password Accepted\nFlag = %s\n", flag);
  } else {
    printf("'%s' is not the password\n", buffer);
  }
  return 0;
}

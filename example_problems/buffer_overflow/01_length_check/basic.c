#include <stdlib.h>
#include <stdio.h>

/*
  Deiberately vulnerable app 1
  This app doesn't check the password, it only checks the length
  Sample input: 12345678
*/

int main(int argc, char *argv[]) {
  FILE *f = fopen("flag.txt", "r");
  char flag[32];
  fgets(flag, 32, f);
  fclose(f);

  char buffer[9];
  printf("Enter password to get flag: ");
  fflush(stdout);
  gets(buffer);
  if (buffer[8] == 0) {
    printf("Password Accepted\nFlag = %s\n", flag);
  } else {
    printf("Wrong password\n");
  }
  return 0;
}

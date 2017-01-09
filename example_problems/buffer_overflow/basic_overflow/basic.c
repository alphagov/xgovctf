#include <stdlib.h>
#include <stdio.h>

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
  gets(buffer);
  if (memcmp(buffer, password, 8) == 0) {
    printf("Password Accepted\nFlag = %s\n", flag);
  } else {
    printf("Wrong password\n");
  }
  return 0;
}

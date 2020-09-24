#include "shifr.h"

char Shifr::key = 'J';

char *Shifr::Encoding(char *str)
{
  int len = strlen(str);
  char *new_str = new char[len];

  for (int i = 0; i < len; i++) {
      new_str[i] = str[i] ^ key;
  }

  return new_str;
}

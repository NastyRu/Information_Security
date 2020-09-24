#ifndef __SHIFR_H
#define __SHIFR_H

#include <iostream>

class Shifr
{
public:
  static char *Encoding(char *str);
private:
  static char key;
};

#endif // __SHIFR_H

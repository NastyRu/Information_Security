#include <iostream>
#include <unistd.h>
#include <limits.h>
#include <fstream>
#include <stdio.h>
using namespace std;

#include "shifr.h"
#include "mac_adress.h"

int main(int argc, char const *argv[]) {
  char pathName[PATH_MAX];
  getwd(pathName);

  char fileName[PATH_MAX] = ".license";

  char *pathToFile = new char[strlen(pathName) + strlen(fileName) + 1 + 1];
  strcpy(pathToFile, pathName);
  strcat(pathToFile, "/");
  strcat(pathToFile, fileName);
  ifstream file(pathToFile);

  char str[100];
  file >> str;

  if (file.is_open() && strcmp(str, Shifr::Encoding(MacAdress::GetMacAdress())) == 0) {
    file.close();
    cout << "Thank you for downloading application!";
  }
  else {
    file.close();
    cout << "No license!";
  }
  return 0;
}

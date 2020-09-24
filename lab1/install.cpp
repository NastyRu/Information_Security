#include <iostream>
#include <unistd.h>
#include <limits.h>
#include <fstream>
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
  ofstream file(pathToFile);

  char *mac_adress = MacAdress::GetMacAdress();
  file << Shifr::Encoding(mac_adress);
  file.close();
  return 0;
}

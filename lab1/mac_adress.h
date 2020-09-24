#ifndef __MAC_ADRESS_H
#define __MAC_ADRESS_H

#include <sys/types.h>
#include <sys/socket.h>
#include <sys/ioctl.h>
#include <sys/sysctl.h>
#include <net/if.h>
#include <net/if_dl.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>

class MacAdress
{
public:
  static char *GetMacAdress();
};

#endif // __MAC_ADRESS_H

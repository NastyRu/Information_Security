#include "mac_adress.h"

char *MacAdress::GetMacAdress()
{
  int	mib[6];
  size_t len;
  char *buf;
  unsigned char	*ptr;
  struct if_msghdr *ifm;
  struct sockaddr_dl *sdl;

  mib[0] = CTL_NET;
  mib[1] = AF_ROUTE;
  mib[2] = 0;
  mib[3] = AF_LINK;
  mib[4] = NET_RT_IFLIST;
  if ((mib[5] = if_nametoindex("en0")) == 0) {
    perror("if_nametoindex error");
    exit(2);
  }

  if (sysctl(mib, 6, NULL, &len, NULL, 0) < 0) {
    perror("sysctl 1 error");
    exit(3);
  }

  if ((buf = (char *)malloc(len)) == NULL) {
    perror("malloc error");
    exit(4);
  }

  if (sysctl(mib, 6, buf, &len, NULL, 0) < 0) {
    perror("sysctl 2 error");
    exit(5);
  }

  ifm = (struct if_msghdr *)buf;
  sdl = (struct sockaddr_dl *)(ifm + 1);
  ptr = (unsigned char *)LLADDR(sdl);

  char *str = new char[PATH_MAX];
  snprintf(str, PATH_MAX, "%02x:%02x:%02x:%02x:%02x:%02x", *ptr, *(ptr+1), *(ptr+2), *(ptr+3), *(ptr+4), *(ptr+5));

  return str;
}

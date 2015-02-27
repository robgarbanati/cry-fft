#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <sys/types.h>
#include <getopt.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <linux/types.h>
#include <math.h>


double b[] =    { 
		0.0005698, -0.00356994, 0.01009062,-0.0158786,  0.0129351,  0.,
		-0.0129351, 0.0158786, -0.01009062, 0.00356994,-0.0005698
		};

double a[] =    {
		1., -7.83048187, 29.49545176, -69.54324339, 113.10358251, -132.2352368,
		112.47629041, -68.77397559,  29.00739557,  -7.65819973, 0.97257529
		};


int main(void)
{
    int i;

    long int tempint;
    for(i=0;i<10;i++)
    {
	tempint = b[i]*1000000000000000;
	printf("b[%d] = %f %ld\n", i, b[i], tempint+1);
    }

    for(i=0;i<10;i++)
    {
	printf("a[%d] = %f\n", i, a[i]);
    }
}

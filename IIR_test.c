#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
/*#include <sys/types.h>*/
/*#include <getopt.h>*/
/*#include <fcntl.h>*/
/*#include <sys/ioctl.h>*/
/*#include <linux/types.h>*/
/*#include <math.h>*/

#define NB  11
#define NA  NB
#define ADC_BUF_SIZE  600
/*#define ADC_BUF_SIZE  13*/

typedef struct
{
    int *array;
    size_t length;
    size_t alloc_size;
} Samples;

void init_array(Samples *a, size_t initialSize)
{
    a->array = (int *)malloc(initialSize * sizeof(int));
    a->length = 0;
    a->alloc_size = initialSize;
}

void insert_array(Samples *a, int element)
{
    if (a->length == a->alloc_size) {
	a->alloc_size *= 2;
	a->array = (int *)realloc(a->array, a->alloc_size * sizeof(int));
    }
    a->array[a->length++] = element;
}

void free_array(Samples *a)
{
    free(a->array);
    a->array = NULL;
    a->length = a->alloc_size = 0;
}


void elliptic_filter(int16_t* x, int64_t* y)
{
    int64_t b[] =   { 
		    56980, -356994, 1009062, -1587860, 1293510,
		    0, -1293510, 1587860, -1009062, 356994, -56980
		    };

    int64_t a[] =   {
		    100000000, -783048187, 2949545176, -6954324339, 11310358251, -13223523680,
		    11247629041, -6877397559, 2900739557, -765819973, 97257529
		    };
    int n, nb, na;
    int64_t bsum, asum, amax, bmax;

    for(n=0;n<ADC_BUF_SIZE;n++)
    {
	bsum = 0;
	asum = 0;
	for(nb=0;nb<NB;nb++)
	{
	    if((n - nb) < 0)
	    {
		bsum += 0;
		/*printf("b[%d] %ld, x[%d] %d, term %d, bsum %ld\n", nb, b[nb], n-nb, 0, 0, bsum);*/
	    }
	    else
	    {
		bsum += (int64_t) b[nb] * (int64_t) x[n - nb] * 100000000;
		/*printf("b[%d] %ld, x[%d] %d, term %ld, bsum %ld\n", nb, b[nb], n-nb, x[n-nb], b[nb]* (int64_t) x[n-nb], bsum);*/
	    }
	}
	for(na=1;na<NA;na++)
	{
	    if((n - na) < 0)
	    {
		asum += 0;
	    }
	    else
	    {
		asum += (int64_t) a[na] * (int64_t) y[n - na];
	    }
	}

	y[n] = (bsum - asum) / a[0];
	/*printf("y[%d] %ld\n", n, y[n]);*/
	if(amax < asum)
	{
	    amax = asum;
	}
	if(bmax < bsum)
	{
	    bmax = bsum;
	}
	/*printf("bsum %ld, asum %ld, y[%d] %ld\n", bsum, asum, n, y[n]);*/
    }
    printf("bmax %ld, amax %ld\n", bmax, amax);
}






/*
 *void init_samples(Samples* samples_ptr)
 *{
 *    FILE* data_fd = fopen("test.txt", "r");
 *    if(data_fd < ((FILE* ) 0))
 *    {
 *        perror("open data.txt");
 *        return;
 *    }
 *
 *    int sample, i=0;
 *    int arraylength;
 *    char buffer[5];
 *
 *    init_array(samples_ptr, 8);
 *    while((fscanf(data_fd, "%s ", buffer)) == 1)
 *    {
 *        sample = atoi(buffer);
 *        insert_array(samples_ptr, sample);
 *    }
 *}
 */



void init_x(int16_t* x)
{
    FILE* data_fd = fopen("test.txt", "r");
    if(data_fd < ((FILE* ) 0))
    {
	perror("open test.txt");
	return;
    }

    int16_t sample, i=0;
    char buffer[5];

    for(i=0;i<ADC_BUF_SIZE;i++)
    {
	if ((fscanf(data_fd, "%s ", buffer)) == 1)
	{
	    sample = (int16_t) atoi(buffer);
	    x[i] = sample;
	    printf("buffer %s, sample %d, x[%d] %d\n", buffer, sample, i, x[i]);
	}
	else
	{
	    puts("size mismatch");
	}
    }
     
    fclose(data_fd);
}



int main(void)
{
    int i;
    int16_t x[ADC_BUF_SIZE];
    int64_t y[ADC_BUF_SIZE];

    init_x(x);
    elliptic_filter(x, y);

    FILE* filtered_fd = fopen("IIR_filtered.txt", "w");

    if(filtered_fd < ((FILE* ) 0))
    {
	perror("open IIR_filtered.txt");
	return;
    }
    puts("opened IIR_filtered.txt!");

    for(i=0;i<ADC_BUF_SIZE;i++)
    {
	/*fprintf(filtered_fd, "%ld\n", y[i]);*/
	fprintf(filtered_fd, "%ld\n", y[i]/100000000);
    }

    fclose(filtered_fd);

}

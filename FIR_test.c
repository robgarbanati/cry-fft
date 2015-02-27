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

#define WINDOW_SIZE 63

#define BGAIN	100000000
#define AGAIN	100000000

typedef struct
{
  int *array;
  size_t used;
  size_t size;
} Samples;

void init_array(Samples *a, size_t initialSize)
{
  a->array = (int *)malloc(initialSize * sizeof(int));
  a->used = 0;
  a->size = initialSize;
}

void insert_array(Samples *a, int element)
{
  if (a->used == a->size) {
    a->size *= 2;
    a->array = (int *)realloc(a->array, a->size * sizeof(int));
  }
  a->array[a->used++] = element;
}

void free_array(Samples *a)
{
  free(a->array);
  a->array = NULL;
  a->used = a->size = 0;
}

void convolve(int* input, Samples* data, int* output, int gain)
{
    int i=0, j=0;
    for(i=0;i<data->used;i++)
    {
	output[i] = 0;
	for(j=-WINDOW_SIZE/2;j<=WINDOW_SIZE/2;j++)
	{
	    /*printf("j %d, i %d\n", j, i);*/
	    // Is index is out of bounds?
	    if(((i + j) < 0) || ((i + j) > data->used)) 
	    {
		output[i] += 0;
	    }
	    else
	    {
		output[i] += input[j+WINDOW_SIZE/2] * data->array[i + j];
		/*printf("in: %d, data: %d, out: %d\n", input[j+WINDOW_SIZE/2], data->array[i + j], output[i]);*/
	    }
	}
	output[i] /= gain;
	/*printf("out: %d\n", output[i]);*/
    }
}

int main()
{
    FILE* data_fd = fopen("test.txt", "r");

    if(data_fd < ((FILE* ) 0))
    {
	perror("open data.txt");
	return;
    }

    int sample, i=0;
    int arraylength;
    char buffer[5];
    Samples samples;
    init_array(&samples, 8);
    while((fscanf(data_fd, "%s ", buffer)) == 1)
    {
	sample = atoi(buffer);
	insert_array(&samples, sample);
    }

    /*
     *for(i=0;i<samples.used;i++)
     *{
     *    printf("%d\n", samples.array[i]);
     *}
     */
#define GAIN	1000000

    int BP_filt[WINDOW_SIZE];
    double float_BP_filt[] = 
    {-0.0042245,  0.00588901, 0.01406446, 0.016524,   0.0118127,  0.00159693,
	-0.00990039,-0.01764996,-0.0180247, -0.01049267, 0.00199501, 0.01415771,
	0.02063134, 0.01834567, 0.00797348,-0.00623109,-0.01818945,-0.02261994,
	-0.01738344,-0.00450418, 0.01062011, 0.02150871, 0.02340492, 0.01536744,
	0.00071191,-0.01441143,-0.02369273,-0.02341662,-0.0140773, -0.00013535,
	0.0119802,  0.01674025, 0.0119802, -0.00013535,-0.0140773, -0.02341662,
	-0.02369273,-0.01441143, 0.00071191, 0.01536744, 0.02340492, 0.02150871,
	0.01062011,-0.00450418,-0.01738344,-0.02261994,-0.01818945,-0.00623109,
	0.00797348, 0.01834567, 0.02063134, 0.01415771, 0.00199501,-0.01049267,
	-0.0180247, -0.01764996,-0.00990039, 0.00159693, 0.0118127,  0.016524,
	0.01406446, 0.00588901,-0.0042245 };

    for(i=0;i<WINDOW_SIZE;i++)
    {
	BP_filt[i] = (int32_t) (float_BP_filt[i]*GAIN);
	/*printf("%d\n", BP_filt[i]);*/
    }





    /*int temparray[] = {1, 1, 1, 1, 1};*/
    /*Samples sample_data = {*/
			    /*temparray,*/
			    /*5,*/
			    /*5*/
			  /*};*/
    int* filtered_data = calloc(samples.used,sizeof(int));

    /*convolve(sample_filt, &sample_data, filtered_data);*/


    convolve(BP_filt, &samples, filtered_data, GAIN);

    int k=0;
    /*
     *for(k=0;k<samples.used;k++)
     *{
     *    printf("filt: %d\n", filtered_data[k]);
     *}
     */

    FILE* filtered_fd = fopen("filtered.txt", "w");

    if(data_fd < ((FILE* ) 0))
    {
	perror("open filtered.txt");
	return;
    }
    puts("opened filtered.txt!");

    for(k=0;k<samples.used;k++)
    {
	fprintf(filtered_fd, "%d\n", filtered_data[k]);
    }



    fclose(data_fd);
    fclose(filtered_fd);
}

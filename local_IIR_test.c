#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <assert.h>

#define CIRCBUF_LENGTH  11
#define NB  CIRCBUF_LENGTH
#define NA  CIRCBUF_LENGTH
#define ADC_BUFFER_SIZE  600
/*#define ADC_BUF_SIZE  13*/
#define GAIN	100000000
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



typedef struct
{
    int64_t array[CIRCBUF_LENGTH];
    uint8_t head;
} CircBuf;

// Grab the element at position, 0-indexed from head
int64_t circbuf_access(CircBuf* buffer, uint8_t position)
{
	uint8_t i;

	assert(position < CIRCBUF_LENGTH);
	i = buffer->head + position;
	if(i >= CIRCBUF_LENGTH)
	{
		i -= CIRCBUF_LENGTH;
	}
	return buffer->array[i];
}

void circbuf_push(CircBuf* buffer, int64_t element)
{
	if(buffer->head == 0)
	{
		buffer->head = CIRCBUF_LENGTH-1;
	}
	else
	{
		buffer->head -= 1;
	}
	buffer->array[buffer->head] = element;
}

void circbuf_init(CircBuf* buffer)
{
	int i;
	buffer->head = 0;
	for(i=0;i<CIRCBUF_LENGTH;i++)
	{
		buffer->array[i] = 0;
	}
}



/*
 *
 *void elliptic_filter(int16_t* x, int64_t* y)
 *{
 *    int64_t b[] =   {
 *                    56980, -356994, 1009062, -1587860, 1293510,
 *                    0, -1293510, 1587860, -1009062, 356994, -56980
 *                    };
 *
 *    int64_t a[] =   {
 *                    100000000, -783048187, 2949545176, -6954324339, 11310358251, -13223523680,
 *                    11247629041, -6877397559, 2900739557, -765819973, 97257529
 *                    };
 *    int n, nb, na;
 *    int64_t bsum, asum, amax, bmax;
 *
 *    for(n=0;n<ADC_BUF_SIZE;n++)
 *    {
 *        bsum = 0;
 *        asum = 0;
 *        for(nb=0;nb<NB;nb++)
 *        {
 *            if((n - nb) < 0)
 *            {
 *                bsum += 0;
 *                [>printf("b[%d] %ld, x[%d] %d, term %d, bsum %ld\n", nb, b[nb], n-nb, 0, 0, bsum);<]
 *            }
 *            else
 *            {
 *                bsum += (int64_t) b[nb] * (int64_t) x[n - nb] * 100000000;
 *                [>printf("b[%d] %ld, x[%d] %d, term %ld, bsum %ld\n", nb, b[nb], n-nb, x[n-nb], b[nb]* (int64_t) x[n-nb], bsum);<]
 *            }
 *        }
 *        for(na=1;na<NA;na++)
 *        {
 *            if((n - na) < 0)
 *            {
 *                asum += 0;
 *            }
 *            else
 *            {
 *                asum += (int64_t) a[na] * (int64_t) y[n - na];
 *            }
 *        }
 *
 *        y[n] = (bsum - asum) / a[0];
 *        [>printf("y[%d] %ld\n", n, y[n]);<]
 *        if(amax < asum)
 *        {
 *            amax = asum;
 *        }
 *        if(bmax < bsum)
 *        {
 *            bmax = bsum;
 *        }
 *        [>printf("bsum %ld, asum %ld, y[%d] %ld\n", bsum, asum, n, y[n]);<]
 *    }
 *    printf("bmax %ld, amax %ld\n", bmax, amax);
 *}
 *
 */


void elliptic_filter(int16_t* x, int16_t* y, int* ymax)
{

    //420 - 1900 baby active zone 8000hz
/*int64_t a[] =  { 1e+08, -5.74067e+08, 1.6666e+09, -3.22597e+09, 4.60196e+09, -5.02751e+09, 4.24896e+09, -2.74612e+09, 1.30408e+09, -4.12122e+08, 6.62576e+07 };*/
/*int64_t b[] =  { 1.77457e+06, -5.37312e+06, 6.35503e+06, -5.86394e+06, 5.31971e+06, 0, -5.31971e+06, 5.86394e+06, -6.35503e+06, 5.37312e+06, -1.77457e+06 };*/


int64_t a[] =  { 1e+08, -2.74003e+08, 6.27055e+08, -9.48357e+08, 1.27886e+09, -1.304e+09, 1.19257e+09, -8.24066e+08, 5.06837e+08, -2.02577e+08, 6.87066e+07 };
int64_t b[] =  { 1.44214e+06, -2.21679e+06, 957900, -1.08721e+06, 2.38572e+06, 0, -2.38572e+06, 1.08721e+06, -957900, 2.21679e+06, -1.44214e+06 };



    int n, nb, na;
    int64_t bsum, asum, amax=0, bmax=0;

    CircBuf ycirc;
    circbuf_init(&ycirc);

    for(n=0;n<ADC_BUFFER_SIZE;n++)
    {
	bsum = 0;
	asum = 0;
	for(nb=0;nb<NB;nb++)
	{
	    if((n - nb) < 0)
	    {
		//				bsum += 0;
		bsum += (int64_t) b[nb] * (int64_t) x[0] * GAIN;
		//				printf("b[%d] %lld, x[%d] %d, term %d, bsum %lld\n", nb, b[nb], n-nb, 0, 0, bsum);
	    }
	    else
	    {
		bsum += (int64_t) b[nb] * (int64_t) x[n - nb] * GAIN;
		//				printf("b[%d] %lld, x[%d] %d, term %lld, bsum %lld\n", nb, b[nb], n-nb, x[n-nb], b[nb]* (int64_t) x[n-nb], bsum);
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
		asum += (int64_t) a[na] * (int64_t) circbuf_access(&ycirc, na-1);
		//				printf("na %d, y[%d] %lld, asum %lld\n", na, n-na, y[n-na], asum);
	    }
	}


	//		y[n] = (int16_t) ((bsum - asum) / a[0] / (GAIN/50));
	y[n] = (int16_t) ((bsum - asum) / a[0] / GAIN);
	circbuf_push(&ycirc, (bsum - asum) / a[0]);
	//		printf("y[%d] %d, ycirc[%d] %lld\n", n, y[n], ycirc.head, circbuf_access(&ycirc, 0));

	if(amax < asum)
	{
	    amax = asum;
	}
	if(bmax < bsum)
	{
	    bmax = bsum;
	}
	if(*ymax < y[n])
	{
	    *ymax = y[n];
	}
	printf("bsum %ld, asum %ld, y[%d] %d\n", bsum, asum, n, y[n]);
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

    for(i=0;i<ADC_BUFFER_SIZE;i++)
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
    int16_t x[ADC_BUFFER_SIZE];
    int16_t y[ADC_BUFFER_SIZE];
    int filt_max;

    init_x(x);
    elliptic_filter(x, y, &filt_max);

    FILE* filtered_fd = fopen("IIR_filtered.txt", "w");

    if(filtered_fd < ((FILE* ) 0))
    {
	perror("open IIR_filtered.txt");
	return;
    }
    puts("opened IIR_filtered.txt!");

    for(i=0;i<ADC_BUFFER_SIZE;i++)
    {
	fprintf(filtered_fd, "%d\n", y[i]);
	/*fprintf(filtered_fd, "%d\n", y[i]/100000000);*/
    }

    fclose(filtered_fd);

}

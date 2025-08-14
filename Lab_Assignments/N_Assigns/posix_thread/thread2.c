#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

#define ARRAY_SIZE 100 // Size of the array

// Structure to pass data to threads
typedef struct
{
    int *array;
    int size;
    long long sum;
    int count;
} ThreadData;

// check if a number is prime
bool is_prime(int num)
{
    if (num <= 1)
        return false;
    for (int i = 2; i * i <= num; i++)
    {
        if (num % i == 0)
            return false;
    }
    return true;
}

// for odd numbers
void *process_odd(void *arg)
{
    ThreadData *data = (ThreadData *)arg;
    data->sum = 0;
    data->count = 0;
    for (int i = 0; i < data->size; i++)
    {
        if (data->array[i] % 2 != 0)
        {
            data->sum += data->array[i];
            data->count++;
        }
    }
    return NULL;
}

// for even numbers
void *process_even(void *arg)
{
    ThreadData *data = (ThreadData *)arg;
    data->sum = 0;
    data->count = 0;
    for (int i = 0; i < data->size; i++)
    {
        if (data->array[i] % 2 == 0)
        {
            data->sum += data->array[i];
            data->count++;
        }
    }
    return NULL;
}

// for prime numbers
void *process_prime(void *arg)
{
    ThreadData *data = (ThreadData *)arg;
    data->sum = 0;
    data->count = 0;
    for (int i = 0; i < data->size; i++)
    {
        if (is_prime(data->array[i]))
        {
            data->sum += data->array[i];
            data->count++;
        }
    }
    return NULL;
}

// generate random array
void generate_array(int *array, int size)
{
    for (int i = 0; i < size; i++)
    {
        array[i] = rand() % 1000 + 1; // rand()
    }
}

int main()
{
    int *array = (int *)malloc(sizeof(int) * ARRAY_SIZE);
    generate_array(array, ARRAY_SIZE);

    pthread_t odd_thread, even_thread, prime_thread;
    ThreadData odd_data = {array, ARRAY_SIZE, 0, 0};
    ThreadData even_data = {array, ARRAY_SIZE, 0, 0};
    ThreadData prime_data = {array, ARRAY_SIZE, 0, 0};

    struct timespec start_time, end_time;

    // With threading
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    pthread_create(&odd_thread, NULL, process_odd, (void *)&odd_data);
    pthread_create(&even_thread, NULL, process_even, (void *)&even_data);
    pthread_create(&prime_thread, NULL, process_prime, (void *)&prime_data);

    pthread_join(odd_thread, NULL);
    pthread_join(even_thread, NULL);
    pthread_join(prime_thread, NULL);

    clock_gettime(CLOCK_MONOTONIC, &end_time);

    double threaded_time = (end_time.tv_sec - start_time.tv_sec) +
                           (end_time.tv_nsec - start_time.tv_nsec) / 1e9;

    printf("With threaading\n");
    if (odd_data.count > 0)
        printf("Average of odd numbers: %.2f\n", (double)odd_data.sum / odd_data.count);
    if (even_data.count > 0)
        printf("Average of even numbers: %.2f\n", (double)even_data.sum / even_data.count);
    if (prime_data.count > 0)
        printf("Average of prime numbers: %.2f\n", (double)prime_data.sum / prime_data.count);
    printf("Time taken (threaded): %.6f seconds\n\n", threaded_time);

    // Without threaading
    long long odd_sum = 0, even_sum = 0, prime_sum = 0;
    int odd_count = 0, even_count = 0, prime_count = 0;

    clock_gettime(CLOCK_MONOTONIC, &start_time);

    for (int i = 0; i < ARRAY_SIZE; i++)
    {
        int val = array[i];
        if (val % 2 == 0)
        {
            even_sum += val;
            even_count++;
        }
        else
        {
            odd_sum += val;
            odd_count++;
        }

        if (is_prime(val))
        {
            prime_sum += val;
            prime_count++;
        }
    }

    clock_gettime(CLOCK_MONOTONIC, &end_time);

    double normal_time = (end_time.tv_sec - start_time.tv_sec) +
                         (end_time.tv_nsec - start_time.tv_nsec) / 1e9;

    printf("Without threaading\n");
    if (odd_count > 0)
        printf("Average of odd numbers: %.2f\n", (double)odd_sum / odd_count);
    if (even_count > 0)
        printf("Average of even numbers: %.2f\n", (double)even_sum / even_count);
    if (prime_count > 0)
        printf("Average of prime numbers: %.2f\n", (double)prime_sum / prime_count);
    printf("Time taken (normal): %.6f seconds\n", normal_time);

    free(array);
    return 0;
}

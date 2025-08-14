#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

#define ARRAY_SIZE 20  // smaller size to keep output readable

typedef struct {
    int *array;
    int size;
    long long sum;
    int count;
} ThreadData;

bool is_prime(int num) {
    if (num <= 1) return false;
    for (int i = 2; i * i <= num; i++) {
        if (num % i == 0) return false;
    }
    return true;
}

void *process_odd(void *arg) {
    ThreadData *data = (ThreadData *)arg;
    data->sum = 0;
    data->count = 0;
    printf("[Odd Thread] Started processing\n");
    for (int i = 0; i < data->size; i++) {
        if (data->array[i] % 2 != 0) {
            data->sum += data->array[i];
            data->count++;
            // printf("[Odd Thread] Adding %d, current sum: %lld\n", data->array[i], data->sum);
        }
    }
    printf("[Odd Thread] Done. Count: %d, Sum: %lld\n", data->count, data->sum);
    return NULL;
}

void *process_even(void *arg) {
    ThreadData *data = (ThreadData *)arg;
    data->sum = 0;
    data->count = 0;
    printf("[Even Thread] Started processing\n");
    for (int i = 0; i < data->size; i++) {
        if (data->array[i] % 2 == 0) {
            data->sum += data->array[i];
            data->count++;
            // printf("[Even Thread] Adding %d, current sum: %lld\n", data->array[i], data->sum);
        }
    }
    printf("[Even Thread] Done. Count: %d, Sum: %lld\n", data->count, data->sum);
    return NULL;
}

void *process_prime(void *arg) {
    ThreadData *data = (ThreadData *)arg;
    data->sum = 0;
    data->count = 0;
    printf("[Prime Thread] Started processing\n");
    for (int i = 0; i < data->size; i++) {
        if (is_prime(data->array[i])) {
            data->sum += data->array[i];
            data->count++;
            // printf("[Prime Thread] Adding %d, current sum: %lld\n", data->array[i], data->sum);
        }
    }
    printf("[Prime Thread] Done. Count: %d, Sum: %lld\n", data->count, data->sum);
    return NULL;
}

void generate_array(int *array, int size) {
    for (int i = 0; i < size; i++) {
        array[i] = rand() % 100 + 1;  
    }
}

double get_time_diff(struct timespec start, struct timespec end) {
    return (end.tv_sec - start.tv_sec) + (end.tv_nsec - start.tv_nsec) / 1e9;
}

void normal_processing(int *array, int size) {
    long long odd_sum = 0, even_sum = 0, prime_sum = 0;
    int odd_count = 0, even_count = 0, prime_count = 0;

    printf("\n[Normal Processing] Started\n");
    for (int i = 0; i < size; i++) {
        int val = array[i];
        if (val % 2 != 0) {
            odd_sum += val;
            odd_count++;
        } else {
            even_sum += val;
            even_count++;
        }
        if (is_prime(val)) {
            prime_sum += val;
            prime_count++;
        }
    }
    printf("[Normal Processing] Done\n");

    if (odd_count > 0)
        printf("Odd average (normal): %.2f\n", (double)odd_sum / odd_count);
    if (even_count > 0)
        printf("Even average (normal): %.2f\n", (double)even_sum / even_count);
    if (prime_count > 0)
        printf("Prime average (normal): %.2f\n", (double)prime_sum / prime_count);
}

int main() {
    srand(time(NULL));

    int *array = (int *)malloc(sizeof(int) * ARRAY_SIZE);
    generate_array(array, ARRAY_SIZE);

    printf("Array: ");
    for (int i = 0; i < ARRAY_SIZE; i++) printf("%d ", array[i]);
    printf("\n");

    pthread_t odd_thread, even_thread, prime_thread;
    ThreadData odd_data = {array, ARRAY_SIZE, 0, 0};
    ThreadData even_data = {array, ARRAY_SIZE, 0, 0};
    ThreadData prime_data = {array, ARRAY_SIZE, 0, 0};

    struct timespec start_time, end_time;

    // Threaded processing
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    pthread_create(&odd_thread, NULL, process_odd, (void *)&odd_data);
    pthread_create(&even_thread, NULL, process_even, (void *)&even_data);
    pthread_create(&prime_thread, NULL, process_prime, (void *)&prime_data);

    pthread_join(odd_thread, NULL);
    pthread_join(even_thread, NULL);
    pthread_join(prime_thread, NULL);

    clock_gettime(CLOCK_MONOTONIC, &end_time);
    double threaded_time = get_time_diff(start_time, end_time);

    printf("\nFinal averages (threaded):\n");
    if (odd_data.count > 0)
        printf("Odd average: %.2f\n", (double)odd_data.sum / odd_data.count);
    if (even_data.count > 0)
        printf("Even average: %.2f\n", (double)even_data.sum / even_data.count);
    if (prime_data.count > 0)
        printf("Prime average: %.2f\n", (double)prime_data.sum / prime_data.count);

    printf("Time taken with threading: %.6f seconds\n", threaded_time);

    // Normal processing
    clock_gettime(CLOCK_MONOTONIC, &start_time);

    normal_processing(array, ARRAY_SIZE);

    clock_gettime(CLOCK_MONOTONIC, &end_time);
    double normal_time = get_time_diff(start_time, end_time);

    printf("Time taken without threading: %.6f seconds\n", normal_time);

    free(array);
    return 0;
}

#include <stdio.h>
#include <stdbool.h>

#define P 5  // Number of processes
#define R 3  // Number of resources

// Function to check if system is in a safe state
bool isSafe(int processes[], int avail[], int max[][R], int allot[][R]) {
    int need[P][R];
    int work[R], finish[P] = {0}, safeSeq[P], count = 0;

    // Calculate Need = Max - Allocation
    for (int i = 0; i < P; i++)
        for (int j = 0; j < R; j++)
            need[i][j] = max[i][j] - allot[i][j];

    // Initialize Work = Available
    for (int i = 0; i < R; i++)
        work[i] = avail[i];

    while (count < P) {
        bool found = false;
        for (int p = 0; p < P; p++) {
            if (!finish[p]) {
                int j;
                for (j = 0; j < R; j++)
                    if (need[p][j] > work[j])
                        break;

                if (j == R) { // If all needs can be satisfied
                    for (int k = 0; k < R; k++)
                        work[k] += allot[p][k];

                    safeSeq[count++] = p;
                    finish[p] = 1;
                    found = true;
                }
            }
        }

        if (!found) {
            printf("System is in UNSAFE state! Deadlock may occur.\n");
            return false;
        }
    }

    printf("System is in SAFE state.\nSafe sequence is: ");
    for (int i = 0; i < P; i++)
        printf("P%d ", safeSeq[i]);
    printf("\n");
    return true;
}

int main() {
    int processes[P] = {0, 1, 2, 3, 4};

    // Available resources
    int avail[R] = {3, 3, 2};

    // Maximum demand of each process
    int max[P][R] = {
        {7, 5, 3},
        {3, 2, 2},
        {9, 0, 2},
        {2, 2, 2},
        {4, 3, 3}
    };

    // Resources allocated to each process
    int allot[P][R] = {
        {0, 1, 0},
        {2, 0, 0},
        {3, 0, 2},
        {2, 1, 1},
        {0, 0, 2}
    };

    isSafe(processes, avail, max, allot);
    return 0;
}


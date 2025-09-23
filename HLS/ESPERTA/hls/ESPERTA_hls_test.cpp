#include "ESPERTA_hls.c"
#include <cstdlib>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


int main(int argc, char **argv) {
  printf("Hello World\n");
  float *data = (float *)malloc(3 * sizeof(float));
  srand(time(NULL)); // Initialize random seed
  for (size_t i = 0; i < 3; i++) {
    data[i] = (float)rand() / RAND_MAX; // Random value between 0 and 1
  }

  float(*input_tensor)[3] = (float(*)[3])data;
  bool(*output_tensor)[6] = (bool(*)[6])malloc(6 * sizeof(bool));

  clock_t start = clock();
  entry(input_tensor, output_tensor);
  clock_t end = clock();
  double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
  printf("Time taken by entry: %f seconds\n", time_spent);

  for (size_t i = 0; i < 6; i++) {
    printf("Output %zu: %x\n", i, (*output_tensor)[i]);
  }

  free(data);
  return 0;
}
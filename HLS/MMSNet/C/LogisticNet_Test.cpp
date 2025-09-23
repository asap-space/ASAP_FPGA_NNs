#include "LogisticNet.c"
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

int main(int argc, char **argv) {
  printf("Hello World\n");
  float *data = (float *)malloc(3 * 32 * 16 * 32 * sizeof(float));
  for (size_t i = 0; i < 3 * 32 * 16 * 32; i++) {
    data[i] = (float)1;
  }

  float(*input_tensor)[1][32][16][32] = (float(*)[1][32][16][32])data;
  float(*output_tensor)[4] = (float(*)[4])malloc(4 * sizeof(float));

  clock_t start = clock();
  entry(input_tensor, output_tensor);
  clock_t end = clock();
  double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
  printf("Time taken by entry: %f seconds\n", time_spent);

  float max = 0;
  uint8_t max_index = 0;
  for (size_t i = 0; i < 4; i++) {
    printf("Output %zu: %f\n", i, (*output_tensor)[i]);
    if ((*output_tensor)[i] > max) {
      max = (*output_tensor)[i];
      max_index = i;
    }
  }
  printf("Predicted: %u - Label: %u\n", max_index, labels[0]);

  free(data);
  return 0;
}
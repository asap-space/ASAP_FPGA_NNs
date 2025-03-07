#include "vaemodel1_hls.cpp"
#include <cstdlib>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


int main(int argc, char **argv) {
  printf("Hello World\n");
  float *data = (float *)malloc(3 * 128 * 256 * sizeof(float));

  float(*input_tensor)[3][128][256] = (float(*)[3][128][256])data;
  float(*output_tensor)[12] = (float(*)[12])malloc(12 * sizeof(float));

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
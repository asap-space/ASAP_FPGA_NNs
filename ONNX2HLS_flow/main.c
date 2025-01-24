#include "HLS_model/LogisticNet.c"
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

float *read_data(const char *filename, size_t *numFloats) {
  FILE *file = fopen(filename, "rb");
  if (file == NULL) {
    perror("Error opening file");
    return NULL;
  }

  fseek(file, 0, SEEK_END);
  long fileSize = ftell(file);
  fseek(file, 0, SEEK_SET);

  *numFloats = fileSize / sizeof(float);
  float *data = (float *)malloc(fileSize);
  if (data == NULL) {
    perror("Error allocating memory");
    fclose(file);
    return NULL;
  }

  size_t result = fread(data, sizeof(float), *numFloats, file);
  if (result != *numFloats) {
    perror("Error reading file");
    free(data);
    fclose(file);
    return NULL;
  }
  fclose(file);

  return data;
}

uint8_t *read_labels(const char *filename, size_t *numLabels) {
  FILE *file = fopen(filename, "rb");
  if (file == NULL) {
    perror("Error opening file");
    return NULL;
  }

  fseek(file, 0, SEEK_END);
  long fileSize = ftell(file);
  fseek(file, 0, SEEK_SET);

  *numLabels = fileSize / sizeof(uint8_t);
  uint8_t *labels = (uint8_t *)malloc(fileSize);
  if (labels == NULL) {
    perror("Error allocating memory");
    fclose(file);
    return NULL;
  }

  size_t result = fread(labels, sizeof(uint8_t), *numLabels, file);
  if (result != *numLabels) {
    perror("Error reading file");
    free(labels);
    fclose(file);
    return NULL;
  }
  fclose(file);

  return labels;
}

int main(int argc, char **argv) {
  printf("Hello World\n");
  size_t numFloats = 0;
  size_t numLabels = 0;
  const char *timestamp = "20171223220000";
  char labels_filename[256];
  char data_filename[256];

  snprintf(labels_filename, sizeof(labels_filename),
           "data_binary/%s/labels_%s.bin", timestamp, timestamp);
  snprintf(data_filename, sizeof(data_filename),
           "data_binary/%s/mms1_dis_dist_fast_%s_0.bin", timestamp, timestamp);

  uint8_t *labels = read_labels(labels_filename, &numLabels);
  float *data = read_data(data_filename, &numFloats);

  if (numFloats != 32 * 16 * 32) {
    fprintf(stderr, "Error: Expected 32x16x32 matrix, but got %zu elements\n",
            numFloats);
    free(data);
    return 1;
  }
  /* If necessary for debug uncomment. This prints the complete data matrix.
  for (size_t i = 0; i < 32; i++) {
      for (size_t j = 0; j < 16; j++) {
          for (size_t k = 0; k < 32; k++) {
              printf("%e ", data[i * 16 * 32 + j * 32 + k]);
          }
          printf("\n");
      }
      printf("\n");
  }
  for (size_t i = 0; i < numLabels; i++) {
    printf("Label %zu: %u\n", i, labels[i]);
  }
  */

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
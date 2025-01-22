import sys, os
from spacepy import pycdf
import numpy as np

DATE = '20171201180000'

def check_file_save(file, numpy_data):
    # Check if the file contains the data in numpy_data
    with open(file, "rb") as file:
        file_data = np.frombuffer(file.read(), dtype=numpy_data.dtype).reshape(numpy_data.shape)

    assert np.array_equal(numpy_data, file_data), "The data in the file does not match the original numpy data"

def write_binary_data(date):
    cdf = pycdf.CDF(f'../data/mms1_fpi_fast_l2_dis-dist_{date}_v3.4.0.cdf')
    for i, numpy_data in enumerate(cdf['mms1_dis_dist_fast']):
        # Save only the values of the numpy data in binary format
        output_file = f'data_binary/mms1_dis_dist_fast_{date}_{i}.bin'
        with open(output_file, "wb") as file:
            file.write(numpy_data.tobytes())
        check_file_save(output_file, numpy_data)
    return cdf['Epoch'][:]

def write_binary_labels(date):
    cdf = pycdf.CDF('../datasets/labels_fpi_fast_dis_dist_201712.cdf')
    label = cdf[f'label_mms1_fpi_fast_dis_dist_{date}']
    # Save the labels in binary format
    output_file = f'data_binary/labels_{date}.bin'
    with open(output_file, "wb") as file:
        file.write(label[:].tobytes())
    check_file_save(output_file, label[:])
    return cdf[f'epoch_mms1_fpi_fast_dis_dist_{date}'][:]


data_epoch = write_binary_data(DATE)
label_epoch = write_binary_labels(DATE)
assert np.array_equal(data_epoch, label_epoch), "Data and label epochs do not match"



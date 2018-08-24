import logging
from glob import glob
from time import time

import numpy as np
from PIL import Image

if __name__ == '__main__':
    start_time = time()

    formatter = logging.Formatter('%(asctime)s : %(name)s :: %(levelname)s : %(message)s')
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    console_handler.setLevel(logging.INFO)
    logger.info('started')

    x_slice_size = 400
    y_slice_size = 400
    input_folder = '../data/images/'
    output_folder = '../output/'
    input_files = input_folder + '*.tif'
    for input_file in glob(input_files):
        base_filename = input_file.replace('\\', '/').replace('.tif', '').replace(input_folder, '')
        image = Image.open(input_file)
        image_array = np.array(image)
        logger.info('%s %s' % (input_file, image_array.shape))
        x_shape = image_array.shape[0]
        y_shape = image_array.shape[1]
        for x_index, x_start in enumerate(range(0, x_shape, x_slice_size)):
            for y_index, y_start in enumerate(range(0, y_shape, y_slice_size)):
                image_slice = image_array[x_start:x_start + x_slice_size, y_start:y_start + y_slice_size, 0:3]
                if image_slice.shape == (x_slice_size, y_slice_size, 3):
                    output_filename = '{}{}.{}.{}.tif'.format(output_folder, base_filename, x_index, y_index)
                    logger.info('writing image section to %s' % output_filename)
                    result = Image.fromarray(image_slice)
                    result.save(output_filename)

    logger.info('done')
    finish_time = time()
    elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
    elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
    logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
    console_handler.close()
    logger.removeHandler(console_handler)

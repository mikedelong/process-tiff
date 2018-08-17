import logging
from glob import glob
from time import time

import matplotlib.pyplot as plt
import tifffile

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
    input_folder = '../data/'
    output_folder = '../output/'
    input_files = input_folder + '*.tif'
    xs = list()
    ys = list()

    for input_file in glob(input_files):
        base_filename = input_file.replace('\\', '/').replace('.tif', '').replace(input_folder, '')
        with tifffile.TiffFile(input_file) as handle:
            metadata = handle.geotiff_metadata
            citation_geokey = metadata['GeogCitationGeoKey']
            model_tie_point = metadata['ModelTiepoint']
            xs.append(model_tie_point[3])
            ys.append(model_tie_point[4])
            logger.info('%s %s %s' % (base_filename, citation_geokey, model_tie_point))

    plt.scatter(xs, ys)
    plt.show()
    logger.info('done')
    finish_time = time()
    elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
    elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
    logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
    console_handler.close()
    logger.removeHandler(console_handler)

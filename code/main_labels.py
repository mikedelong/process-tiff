import logging
from collections import Counter
from json import load
from time import time
from zipfile import ZipFile
from PIL import Image
import numpy as np

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

    with open('settings.json', 'r') as settings_fp:
        settings = load(settings_fp)
        logger.info(settings)
        image_files = settings['image_files']
        output_folder = settings['output_folder']
        x_size = settings['x_size']
        y_size = settings['y_size']
        archive = ZipFile(settings['zipfile'], 'r')
        type_id_counts = Counter()
        type_counts = Counter()
        feature_id_counts = Counter()
        image_id_counts = Counter()
        images_in_files = Counter()

        with archive.open(settings['geojson_file']) as geojson_fp:
            objects = load(geojson_fp)
            logger.info(len(objects))
            features = objects['features']
            logger.info(len(features))
            for index, feature in enumerate(features):
                properties_ = feature['properties']
                image_id = properties_['image_id']
                image_id_counts[image_id] += 1
                type_counts[feature['type']] += 1
                type_id_ = properties_['type_id']
                type_id_counts[type_id_] += 1
                feature_id_counts[properties_['feature_id']] += 1
                if index == 0:
                    logger.info(feature)
                if image_id in image_files:
                    images_in_files[image_id] += 1
                    bounds_imcoords = properties_['bounds_imcoords']
                    [xmin, ymin, xmax, ymax] = [int(item) for item in bounds_imcoords.split(',')]
                    logger.info('bounding box is %s, is %d x %d,  %d total pixels' %
                                (str([xmin, ymin, xmax, ymax]), xmax-xmin, ymax-ymin, (xmax-xmin) * (ymax-ymin)))
                    input_file = settings['image_folder'] + image_id
                    image = Image.open(input_file)
                    image_array = np.array(image)
                    x_mid = (xmin + xmax)//2
                    x_start = max(0, x_mid - x_size//2)
                    x_stop = x_start + x_size
                    if x_stop > image_array.shape[0]:
                        x_stop = image_array.shape[0]-1
                        x_start = x_stop - x_size
                    y_mid = (ymin + ymax)//2
                    y_start = max(0, y_mid - y_size//2)
                    y_stop = y_start + y_size
                    if y_stop > image_array.shape[1]:
                        y_stop = image_array.shape[1]-1
                        y_start = y_stop - y_size
                    logger.info('adjusted bounding box is %s, is %d x %d,  %d total pixels' %
                                (str([x_start, x_start, x_stop, y_stop]), x_stop-x_start,
                                 y_stop-y_start, (x_stop-x_start) * (y_stop-y_start)))
                    image_slice = image_array[x_start:x_stop, y_start:y_stop, 0:3]
                    output_filename = '{}{}.{}.{}.tif'.format(output_folder, image_id.replace('.tif', ''), index,
                                                              type_id_)
                    logger.info('writing image section to %s' % output_filename)
                    result = Image.fromarray(image_slice)
                    result.save(output_filename)

        logger.info(type_id_counts)
        logger.info('type_id count %d' % len(type_id_counts))
        logger.info(image_id_counts)
        logger.info('image_id count: %d' % len(image_id_counts))
        logger.info(images_in_files)
        logger.info('we have %d images in our files' % len(images_in_files))

    logger.info('done')
    finish_time = time()
    elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
    elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
    logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
    console_handler.close()
    logger.removeHandler(console_handler)

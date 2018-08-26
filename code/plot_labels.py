import logging
from collections import Counter
from json import load
from time import time
from zipfile import ZipFile

import matplotlib.pyplot as plt

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

    count = 0
    limit = 65000
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
            keep = set()
            for index, feature in enumerate(features):
                properties_ = feature['properties']
                image_id = properties_['image_id']
                image_id_counts[image_id] += 1
                type_counts[feature['type']] += 1
                type_id_ = properties_['type_id']
                type_id_counts[type_id_] += 1
                feature_id_counts[properties_['feature_id']] += 1
                geometry = feature['geometry']
                coordinates = geometry['coordinates'][0]
                for coordinate in coordinates:
                    keep.add((coordinate[0], coordinate[1]))
                    if len(keep) == limit:
                        keep_list = list(keep)
                        figure, (ax_left, ax_right) = plt.subplots(ncols=2, figsize=(10, 5))
                        xs = [item[0] for item in keep_list]
                        ys = [item[1] for item in keep_list]
                        ax_left.scatter(xs, ys, s=1)
                        ax_right.scatter(ys, xs, s=1)
                        logger.info(index)
                        logger.info(len(features))
                        plt.show()

                        quit()

                if index == 0:
                    logger.info(feature)

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

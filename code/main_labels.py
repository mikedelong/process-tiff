import logging
from collections import Counter
from json import load
from time import time
from zipfile import ZipFile

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
            image_id = feature['properties']['image_id']
            image_id_counts[image_id] += 1
            type_counts[feature['type']] += 1
            type_id_counts[feature['properties']['type_id']] += 1
            feature_id_counts[feature['properties']['feature_id']] += 1
            if index == 0:
                logger.info(feature)
            if image_id in image_files:
                images_in_files[image_id] += 1

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

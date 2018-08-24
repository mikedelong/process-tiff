import logging
from time import time
from zipfile import ZipFile
from json import load

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

    archive = ZipFile(settings['zipfile'], 'r')
    with archive.open(settings['geojson_file']) as geojson_fp:
        objects = load(geojson_fp)
        logger.info(len(objects))
        features = objects['features']
        logger.info(len(features))
        for feature in features:
            if feature == features[0]:
                logger.info(feature)
                type_id = feature['properties']['type_id']
                logger.info(type_id)



    logger.info('done')
    finish_time = time()
    elapsed_hours, elapsed_remainder = divmod(finish_time - start_time, 3600)
    elapsed_minutes, elapsed_seconds = divmod(elapsed_remainder, 60)
    logger.info('Time: {:0>2}:{:0>2}:{:05.2f}'.format(int(elapsed_hours), int(elapsed_minutes), elapsed_seconds))
    console_handler.close()
    logger.removeHandler(console_handler)

import os
import shutil
import random

#default config
ASSET_DIR ='assets'
TMP_ASSET_DIR = 'tmp_assets'
BUTTON_DIR = 'button_images'
IMAGE_SIZE_H = 119
IMAGE_SIZE_W = 106
SCREEN_START_Y = 374
SCREEN_START_X = 300
MARGIN = 2
ALL_ASSET_FILES = [x for x in os.listdir(ASSET_DIR) if x[-3:].lower()=='png']
ASSET_FILES = [x for x in os.listdir(TMP_ASSET_DIR) if x[-3:].lower()=='png']
NUM_TITLES_SIDE = 4
NUM_TITLES_TOTAL = 16

def load_setting(level):
    """Loading setting based on difficulty selection"""

    global ASSET_FILES, SCREEN_START_X, SCREEN_START_Y, NUM_TITLES_SIDE, NUM_TITLES_TOTAL

    if level == 'easy':

        SCREEN_START_Y = 374
        SCREEN_START_X = 300
        NUM_TITLES_SIDE = 4
        NUM_TITLES_TOTAL = 16
        asset_preparation(level)
        ASSET_FILES = [x for x in os.listdir(TMP_ASSET_DIR) if x[-3:].lower()=='png']
        assert len(ASSET_FILES) == 8

    if level == 'medium':

        SCREEN_START_Y = 255
        SCREEN_START_X = 194
        NUM_TITLES_SIDE = 6
        NUM_TITLES_TOTAL = 36

        asset_preparation(level)
        ASSET_FILES = [x for x in os.listdir(TMP_ASSET_DIR) if x[-3:].lower()=='png']
        assert len(ASSET_FILES) == 18

    if level == 'hard':

        SCREEN_START_Y = 136
        SCREEN_START_X = 88
        NUM_TITLES_SIDE = 8
        NUM_TITLES_TOTAL = 64

        asset_preparation(level)
        ASSET_FILES = [x for x in os.listdir(TMP_ASSET_DIR) if x[-3:].lower()=='png']
        assert len(ASSET_FILES) == 32
    
def asset_preparation(level):
    """Temp files cleanup and create"""
    if level == 'easy':
        no_of_files = 8
    elif level == 'medium':
        no_of_files = 18
    elif level == 'hard':
        no_of_files = 32

    for filename in os.listdir(TMP_ASSET_DIR):
        file_path = os.path.join(TMP_ASSET_DIR, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    for file_name in random.sample(ALL_ASSET_FILES, no_of_files):
        shutil.copy(os.path.join(ASSET_DIR, file_name), TMP_ASSET_DIR)
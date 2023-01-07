import os
import random
import game_config as gc

from pygame import image, transform


def available_animals(animals_count):
    return [a for a,c in animals_count.items() if c <2]

class Animal:
    def __init__(self,index,animals_count):
        self.index = index
        self.row = index // gc.NUM_TITLES_SIDE
        self.col = index % gc.NUM_TITLES_SIDE
        self.name = random.choice(available_animals(animals_count))
        animals_count[self.name] += 1

        self.image_path = os.path.join(gc.TMP_ASSET_DIR, self.name)
        self.image = image.load(self.image_path)
        self.image = transform.scale(self.image, (gc.IMAGE_SIZE_W - 2*gc.MARGIN, gc.IMAGE_SIZE_H - 2*gc.MARGIN))
        self.back = image.load('other_assets/back.png')
        self.back = transform.scale(self.back, (gc.IMAGE_SIZE_W - 2*gc.MARGIN, gc.IMAGE_SIZE_H - 2*gc.MARGIN))
        self.skip = False
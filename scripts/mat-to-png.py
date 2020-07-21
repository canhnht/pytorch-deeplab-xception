import os
from PIL import Image
import numpy as np
import scipy.io


def get_paths_from_images(path):
    '''get image path list from image folder'''
    assert os.path.isdir(path), '{:s} is not a valid directory'.format(path)
    images = []
    for dirpath, _, fnames in sorted(os.walk(path)):
        for fname in sorted(fnames):
            img_path = os.path.join(dirpath, fname)
            images.append(img_path)
    assert images, '{:s} has no valid image file'.format(path)
    return images

##################################


INPUT_DIR = '/Users/thanhcanh/Documents/projects/ac-remove-background/DeepLab_v3/data/datasets/SBD/benchmark_RELEASE/dataset/cls'
OUTPUT_DIR = '/Users/thanhcanh/Documents/projects/ac-remove-background/DeepLab_v3/data/datasets/SBD/benchmark_RELEASE/dataset/cls-img'

assert os.path.isdir(
    INPUT_DIR), '{:s} is not a valid directory'.format(INPUT_DIR)
assert os.path.isdir(
    OUTPUT_DIR), '{:s} is not a valid directory'.format(OUTPUT_DIR)

paths = sorted(get_paths_from_images(INPUT_DIR))
print(f'Process {len(paths)} images...')

for input_path in paths:
    print(f'Input: {input_path}')
    _, img_file = os.path.split(input_path)
    img_filename, _ = os.path.splitext(img_file)
    output_path = os.path.join(OUTPUT_DIR, img_filename + '.png')
    if os.path.exists(output_path):
        continue
    f = scipy.io.loadmat(input_path)
    label = f['GTcls']['Segmentation'][0][0]
    image = np.array(label)
    hi = np.max(image)
    lo = np.min(image)
    image = (((image - lo)/(hi-lo))*255).astype(np.uint8)
    img = Image.fromarray(image)
    pixels = img.load()
    for i in range(img.size[0]): # for every pixel:
        for j in range(img.size[1]):
            pixel = img.getpixel((i, j))
            if pixel != 0:
                img.putpixel((i, j), 255)
    img.save(output_path)
    print('==============================================')

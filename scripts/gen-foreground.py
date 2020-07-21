import os
from PIL import Image
import numpy as np
import scipy.io
import cv2


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


ORIGINAL_IMAGE_DIR = '/Users/thanhcanh/Documents/projects/ac-remove-background/DeepLab_v3/data/datasets/SBD/benchmark_RELEASE/dataset/img'
MASK_IMAGE_DIR = '/Users/thanhcanh/Documents/projects/ac-remove-background/DeepLab_v3/data/datasets/SBD/benchmark_RELEASE/dataset/cls-img'
OUTPUT_DIR = '/Users/thanhcanh/Documents/projects/ac-remove-background/DeepLab_v3/data/datasets/SBD/benchmark_RELEASE/dataset/fg-img'

assert os.path.isdir(
    ORIGINAL_IMAGE_DIR), '{:s} is not a valid directory'.format(ORIGINAL_IMAGE_DIR)
assert os.path.isdir(
    MASK_IMAGE_DIR), '{:s} is not a valid directory'.format(MASK_IMAGE_DIR)

original_paths = sorted(get_paths_from_images(ORIGINAL_IMAGE_DIR))
mask_paths = sorted(get_paths_from_images(MASK_IMAGE_DIR))
print(f'Process {len(original_paths)} images...')

for input_path in original_paths:
    print(f'Input: {input_path}')
    _, img_file = os.path.split(input_path)
    img_filename, _ = os.path.splitext(img_file)
    mask_path = os.path.join(MASK_IMAGE_DIR, img_filename + '.png')
    output_path = os.path.join(OUTPUT_DIR, img_filename + '.png')
    if os.path.exists(output_path):
        continue

    pred_mattes = cv2.imread(mask_path)
    for pixel in pred_mattes:
        print('pixellll', pixel)
    print('pred_mattessssssss', pred_mattes.size)
    img = cv2.imread(input_path)
    print('imgggggggg', img.size)
    b, g, r = cv2.split(img)
    print('bbbbbbbbbbbb', b.size)
    # Display each separated channel
    cv2.imshow("Red", r)
    cv2.imshow("Green", g)
    cv2.imshow("Blue", b)
    rmbg_img = cv2.merge(
        (b.astype(int), g.astype(int), r.astype(int), (pred_mattes*255).astype(int)))
    cv2.imshow("rmbg", rmbg_img)
    cv2.waitKey(0)
    # rmbg_img = rmbg_img.astype("uint8")
    # print('rmbg_img', rmbg_img.size)
    # Image.fromarray(rmbg_img).save(output_path)
    # cv2.imwrite(output_path, rmbg_img)
    print('==============================================')

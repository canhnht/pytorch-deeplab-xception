import os
from PIL import Image


IMG_EXTENSIONS = ['.jpg', '.JPG', '.jpeg', '.JPEG', '.png',
                  '.PNG', '.ppm', '.PPM', '.bmp', '.BMP', '.dng', '.DNG']


def is_image_file(filename):
    return any(filename.endswith(extension) for extension in IMG_EXTENSIONS)


def get_paths_from_images(path):
    '''get image path list from image folder'''
    assert os.path.isdir(path), '{:s} is not a valid directory'.format(path)
    images = []
    for dirpath, _, fnames in sorted(os.walk(path)):
        for fname in sorted(fnames):
            if is_image_file(fname):
                img_path = os.path.join(dirpath, fname)
                images.append(img_path)
    assert images, '{:s} has no valid image file'.format(path)
    return images

##################################


INPUT_DIR = '/Volumes/Young Buffalo/datasets/deeplab/VOCdevkit/VOC2012/SegmentationClass'
OUTPUT_DIR = '/Volumes/Young Buffalo/datasets/deeplab/VOCdevkit/VOC2012/removebg'

assert os.path.isdir(
    INPUT_DIR), '{:s} is not a valid directory'.format(INPUT_DIR)
assert os.path.isdir(
    OUTPUT_DIR), '{:s} is not a valid directory'.format(OUTPUT_DIR)

paths = sorted(get_paths_from_images(INPUT_DIR))
print(f'Process {len(paths)} images...')

for input_path in paths:
    print(f'Input: {input_path}')
    _, img_file = os.path.split(input_path)
    output_path = os.path.join(OUTPUT_DIR, img_file)
    img = Image.open(input_path).convert('L')
    pixels = img.load()
    # for i in range(img.size[0]): # for every pixel:
    #     for j in range(img.size[1]):
    #         if pixels[i,j] != (0, 0, 0):
    #             # change to white if not black
    #             pixels[i,j] = (255, 255 ,255)
    for i in range(img.size[0]): # for every pixel:
        for j in range(img.size[1]):
            pixel = img.getpixel((i, j))
            if pixel != 0:
                img.putpixel((i, j), 255)
    img.save(output_path)
    print('==============================================')

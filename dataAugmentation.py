import os
import sys
import glob
import shutil
from keras.preprocessing.image import (ImageDataGenerator, array_to_img,
                                       img_to_array, load_img)


def ignoreFiles(_, __): pass

numImagesGenerate = 19  # Number of images to be generated from the original

datagen = ImageDataGenerator(
    rotation_range=1,
    brightness_range=[1.5, 0.5],
    horizontal_flip=False,
    fill_mode='nearest')

# Check input arguments
if len(sys.argv) != 3:
    print("Error: One source and one destination folders are expected")
    exit()
if not os.path.isdir(sys.argv[1]):
    print("Error: The specified source folder does not exist")
    exit()
source = sys.argv[1]
dest = sys.argv[2]

# Copy folder structure to dest
if os.path.isdir(dest):
    shutil.rmtree(dest)
shutil.copytree(source, dest, copy_function=ignoreFiles)

# Find the number of files to augment
numImagesOriginal = 0
for subdir, dirs, images in os.walk(source):
    for image in images:
        numImagesOriginal += 1

# Apply the data augmentation to every image keeping the same structure
numImagesTotal = numImagesOriginal * (numImagesGenerate + 1)
numImagesProcessed = 0
for subdir, dirs, images in os.walk(source):
    for image in images:
        pathImageIn = subdir + "/" + image
        pathImageOut = subdir[subdir.find("/")+1:] + "/" + image

        img = load_img(pathImageIn)     # PIL image
        x = img_to_array(img)           # Numpy array with shape (3, x, y)
        x = x.reshape((1,) + x.shape)   # Numpy array with shape (1, 3, x, y)

        i = 0
        for batch in datagen.flow(x, batch_size=1,
                                  save_to_dir=dest, save_prefix=pathImageOut,
                                  save_format='jpeg'):
            if i > numImagesGenerate:
                break
            i += 1

        # Copy the original file as well
        shutil.copyfile(pathImageIn, dest + "/" + pathImageOut)

        # Print progress info
        numImagesProcessed += numImagesGenerate + 1
        print("Processed {}/{} images ({:4.2f} %)".format(numImagesProcessed,
              numImagesTotal, numImagesProcessed*100/numImagesTotal))

import os
import sys
import shutil
from keras.preprocessing.image import (ImageDataGenerator, array_to_img,
                                       img_to_array, load_img)


'''
Batch augment images

This script takes an input directory containing images and applies data
augmentation to generate new images with subtle modifications in a new output
directory while keeping the original folder structure. The original images are
also copied.

# Arguments
    -source path: Input directory containing the original images.
    -destination path: Output directory to be created containig the new
        images.
    -number of images: Number of new images to generate per original image.
'''


def ignoreFiles(_, __): pass

datagen = ImageDataGenerator(
    rotation_range=1,
    brightness_range=[1.5, 0.5],
    horizontal_flip=False,
    fill_mode='nearest')

# Check input arguments
if len(sys.argv) != 4:
    print("Error: Arguments must be source path, destination path and number"
          "of images to generate ")
    exit()
if not os.path.isdir(sys.argv[1]):
    print("Error: The specified source folder does not exist")
    exit()
if not sys.argv[3].isdigit():
    print("Error: The number of images to generate must be an integer")
    exit()
source = sys.argv[1]
dest = sys.argv[2]
num_images_generate = int(sys.argv[3])

# Copy folder structure to dest
if os.path.isdir(dest):
    shutil.rmtree(dest)
shutil.copytree(source, dest, copy_function=ignoreFiles)

# Find the number of files to augment
num_images_original = 0
for source_dir_path, sub_dirs, images in os.walk(source):
    for image in images:
        num_images_original += 1

# Apply the data augmentation to every image keeping the same structure
num_images_total = num_images_original * (num_images_generate + 1)
num_images_processed = 0
for source_dir_path, sub_dirs, images in os.walk(source):
    for image in images:
        image_in = os.path.join(source_dir_path, image)

        img = load_img(image_in)        # PIL image
        x = img_to_array(img)           # Numpy array with shape (3, x, y)
        x = x.reshape((1,) + x.shape)   # Numpy array with shape (1, 3, x, y)

        dest_sub_dir_tail = os.path.split(source_dir_path)[1]
        dest_sub_dir = os.path.join(dest, dest_sub_dir_tail)
        i = 0
        for batch in datagen.flow(x, batch_size=1,
                                  save_to_dir=dest_sub_dir,
                                  save_prefix=image.replace(".jpg", ""),
                                  save_format='jpg'
                                  ):
            i += 1
            if i >= num_images_generate:
                break

        # Copy the original file as well
        image_out = os.path.join(dest_sub_dir, image)
        shutil.copyfile(image_in, image_out)

        # Print progress info
        num_images_processed += num_images_generate + 1
        print("Processed {}/{} images ({:4.2f} %)".format(num_images_processed,
              num_images_total, num_images_processed*100/num_images_total),
              end='\r')
print("")

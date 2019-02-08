import os
import sys
import shutil
import subprocess


'''
Batch resize images

This script takes an input directory containing images and resizes them to the
specified size while keeping the original folder structure.

# Arguments
    -source path: Input directory containing the original images.
    -destination path: Output directory to be created containig the resized
        images.
    -width: The width in pixels to which the images must be resized.
    -(Optional) height: The width in pixels to which the images must be
        resized. If no height value is provided the width will will applied
        to both dimensions.
'''


def ignoreFiles(_, __): pass

# Check input arguments
if not 4 <= len(sys.argv) <= 5:
    print("Error: Arguments must be source path, destination path, width (and\
          optionally height)")
    exit()
if not os.path.isdir(sys.argv[1]):
    print("Error: The specified source folder does not exist")
    exit()
if not sys.argv[3].isdigit():
    print("Error: The width must be an integer")
    exit()
source = sys.argv[1]
dest = sys.argv[2]
width = sys.argv[3]
if len(sys.argv) == 5 and sys.argv[4].isdigit():
    height = sys.argv[4]
else:
    height = width

# Copy folder structure to dest
if os.path.isdir(dest):
    shutil.rmtree(dest)
shutil.copytree(source, dest, copy_function=ignoreFiles)

# Find the number of files to convert
num_images_total = 0
for source_dir_path, sub_dirs, images in os.walk(source):
    for image in images:
        num_images_total += 1

# Resize all images in subfolders
dims = "" + width + "x" + height + "!"
num_images_processed = 0
for source_dir_path, sub_dirs, images in os.walk(source):
    for image in images:
        image_in = os.path.join(source_dir_path, image)
        image_out = os.path.join(source_dir_path.replace(source, dest), image)
        subprocess.call(["convert", image_in, "-resize", dims, image_out])
        # Print progress info
        num_images_processed += 1
        print("Processed {}/{} images ({:4.2f} %)".format(num_images_processed,
              num_images_total, num_images_processed*100/num_images_total),
              end="\r")
print("")

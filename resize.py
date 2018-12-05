import os
import sys
import glob
import shutil
import subprocess


def ignoreFiles(_, __): pass

# Check input arguments
if len(sys.argv) != 5:
    print("Error: Arguments must be source path, destination path, width and\
          height")
    exit()
if not os.path.isdir(sys.argv[1]):
    print("Error: The specified source folder does not exist")
    exit()
if not sys.argv[3].isdigit() or not sys.argv[4].isdigit():
    print("Error: The width and height must be integers")
    exit()
source = sys.argv[1]
dest = sys.argv[2]
width = sys.argv[3]
height = sys.argv[4]

# Copy folder structure to dest
if os.path.isdir(dest):
    shutil.rmtree(dest)
shutil.copytree(source, dest, copy_function=ignoreFiles)

# Find the number of files to convert
numImagesTotal = 0
for subdir, dirs, images in os.walk(source):
    for image in images:
        numImagesTotal += 1

# Resize all images in subfolders
dims = "" + width + "x" + height + "!"
numImagesProcessed = 0
for subdir, dirs, images in os.walk(source):
    for image in images:
        imageIn = os.path.join(subdir, image)
        imageOut = os.path.join(subdir.replace(source, dest), image)
        subprocess.call(["convert", imageIn, "-resize", dims, imageOut])
        # Print progress info
        numImagesProcessed += 1
        print("Processed {}/{} images ({:4.2f} %)".format(numImagesProcessed,
              numImagesTotal, numImagesProcessed*100/numImagesTotal))

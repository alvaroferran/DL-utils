import os
import sys
import shutil
import random


'''
Sort files into "train", "dev" and "test" sets.

This script takes an input directory containing images classified into
different subfolders and sorts them into a new output directory.

# Arguments
    -source path: Input directory containing the classified images.
    -destination path: Output directory to be created containig the sorted
        sets.
    -(Optional) training set percentage: Percentage of files to be sorted into
        the "train" set, the remainder being split equally between the "dev"
        and "test" sets. This value must be an integer between 50 and 100. If
        no value is provided a value of 80 will be used.

# Visual explanation

    - input folder              -output folder
        -class1                     -train
        -...                            -class1
        -classN                         -...
                                        -classN
                                    -dev
                                        -class1
                                        -...
                                        -classN
                                    -test
                                        -class1
                                        -...
                                        -classN

'''


def ignoreFiles(_, __): pass

# Check input arguments
if not 3 <= len(sys.argv) <= 4:
    print("Error: Arguments must be source path and destination path "
          "(and optionally training set percentage")
    exit()
if not os.path.isdir(sys.argv[1]):
    print("Error: The specified source folder does not exist")
    exit()
source = sys.argv[1]
dest = sys.argv[2]

# Define set percentages
arg = sys.argv
if len(arg) == 4 and arg[3].isdigit() and 50 <= int(arg[3]) < 100:
        train_set_percent = int(arg[3])
else:
    train_set_percent = 80
dev_set_percent = (100-train_set_percent)//2
test_set_percent = dev_set_percent
percentages = {"train": train_set_percent,
               "dev": dev_set_percent,
               "test": test_set_percent}

# Create dest directory
if os.path.isdir(dest):
    shutil.rmtree(dest)
os.mkdir(dest)

# Create sets with the correct folder structure
sets = ["train", "dev", "test"]
for set_name in sets:
    dest_sub_dir = os.path.join(dest, set_name)
    shutil.copytree(source, dest_sub_dir, copy_function=ignoreFiles)

# Find the number of files to convert
num_images_total = 0
for source_dir_path, sub_dirs, images in os.walk(source):
    for image in images:
        num_images_total += 1

# Copy all images to the correct set subfolders
random.seed(1)  # Fixed seed to ensure the sets are the same between executions
num_images_processed = 0
num_dirs_walked = 0
for source_dir_path, sub_dirs, images in os.walk(source):
    if num_dirs_walked > 0:    # Ignore the first "root" directory
        # Order and shuffle the images to have a random list for each class
        images.sort()
        random.shuffle(images)
        num_images_class = len(images)
        for set_name in sets:
            # Create the correct output sub directory path
            source_sub_dir_tail = os.path.split(source_dir_path)[1]
            dest_sub_dir = os.path.join(dest, set_name)
            dest_sub_dir = os.path.join(dest_sub_dir, source_sub_dir_tail)
            # Calculate the number of images for each set (truncated)
            num_images_set = num_images_class * percentages[set_name] // 100
            for i in range(num_images_set):
                # Copy the images (all elements get shifted after pop)
                image_in = os.path.join(source_dir_path, images[0])
                image_out = os.path.join(dest_sub_dir, images[0])
                shutil.copyfile(image_in, image_out)
                images.pop(0)
                # Print progress info
                num_images_processed += 1
                print("Processed {}/{} images ({:4.2f} %)".format(
                    num_images_processed, num_images_total,
                    num_images_processed*100/num_images_total), end='\r')
        # Add any remaining images due to the truncation to the training set
        dest_sub_dir = os.path.join(dest, "train")
        dest_sub_dir = os.path.join(dest_sub_dir, source_sub_dir_tail)
        for i in range(len(images)):
            image_in = os.path.join(source_dir_path, images[0])
            image_out = os.path.join(dest_sub_dir, images[0])
            shutil.copyfile(image_in, image_out)
            images.pop(0)
            # Print progress info
            num_images_processed += 1
            print("Processed {}/{} images ({:4.2f} %)".format(
                num_images_processed, num_images_total,
                num_images_processed*100/num_images_total), end='\r')
    num_dirs_walked += 1
print("")

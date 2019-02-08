#  Deep Learning utilities

The purpose of this set of helper scripts is to ease the manipulation and setup of image datasets for Deep Learning projects.
The following utilities have been implemented:


### resizeImages.py: 
Batch resize images

This script takes an input directory containing images and resizes them to the
specified size while keeping the original folder structure.

Arguments:
1. source path: Input directory containing the original images.

2. destination path: Output directory to be created containig the resized images.

3. width: The width in pixels to which the images must be resized.

4. (Optional) height: The width in pixels to which the images must be resized. If no height value is provided the width will will applied to both dimensions.



### augmentData.py:
Batch augment images

This script takes an input directory containing images and applies data
augmentation to generate new images with subtle modifications in a new output
directory while keeping the original folder structure. The original images are
also copied.

Arguments:
1. source path: Input directory containing the original images.

2. destination path: Output directory to be created containig the new images.

3. number of images: Number of new images to generate per original image.



### createSets.py:
Sort files into "train", "dev" and "test" sets.

This script takes an input directory containing images classified into
different subfolders and sorts them into a new output directory.

Arguments:
1. source path: Input directory containing the classified images.
    
2. destination path: Output directory to be created containig the sorted sets.

3. (Optional) training set percentage: Percentage of files to be sorted into the "train" set, the remainder being split equally between the "dev" and "test" sets. This value must be an integer between 50 and 100. If no value is provided a value of 80 will be used.

Visual explanation:

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


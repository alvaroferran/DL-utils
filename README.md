#  Data Augmentation

This script leverages the power of Keras and Tensorflow to augment the image dataset to be used in neural networks. The first thing to do is install both frameworks with

    pip3 install keras tensorflow

The source and destination paths are passed by command line parameters, which of course means that the source folder must be created and contain the images to be augmented. The destination directory is created by the program, and will contain the same internal folder structure as the first one, so that the augmented images fall into the correct categories.

The script only uses small rotations and different lightings as the basis for augmentation, but this is easily changed in the datagen block, as well as the number of extra images to be created

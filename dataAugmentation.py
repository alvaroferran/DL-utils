from keras.preprocessing.image import (ImageDataGenerator, array_to_img,
                                       img_to_array, load_img)
import glob
import os

pathIn = "train/busy/"
pathOut = "augmented"
numImages = 20

datagen = ImageDataGenerator(
    rotation_range=1,
    brightness_range=[1.5, 0.5],
    horizontal_flip=False,
    fill_mode='nearest')

# Create folder if missing
if not os.path.isdir(pathOut + "/" + pathIn):
    os.makedirs(pathOut + "/" + pathIn)

for image in glob.glob(pathIn + '*.jpg'):
    img = load_img(image)  # PIL image
    x = img_to_array(img)  # Numpy array with shape (3, 150, 150)
    x = x.reshape((1,) + x.shape)  # Numpy array with shape (1, 3, 150, 150)
    print(image)

    i = 0
    for batch in datagen.flow(x, batch_size=1,
                              save_to_dir=pathOut, save_prefix=image,
                              save_format='jpeg'):
        if i > numImages:
            break
        i += 1

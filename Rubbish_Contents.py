"""
Script to train image recognition model to determine how full a rubbish bin is.

Use:
- Change train_path and valid_path to the directory of the training and validation images 
- In train_batches and valid_batches change the classes to the image classes that you are training on
- Change the save location of the model to what is desired

Packages:
Python 3.7
numpy = 1.18.1
keras = 2.2.4
tensorflow = 1.13
matplotlib = 3.1.2
pillow 7.0.0
"""


import numpy as np
import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers import Activation
from keras.layers.core import Dense,Flatten
from keras.optimizers import Adam, SGD
from keras.metrics import categorical_crossentropy
from keras.preprocessing.image import ImageDataGenerator
from keras.layers.normalization import BatchNormalization
from keras.layers.convolutional import *
from matplotlib import pyplot as plt
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

train_path = 'C:/Users/domin/Pictures/rubbish-train/Train'
valid_path = 'C:/Users/domin/Pictures/rubbish-train/Valid'

'''
Load images using a generator to save on computing power, must specify correct target size (224,224)
to be able to load into the VGG19 model. Generator automatically resizes.
Specify names of classes and batch size. Batch size can be changed to optimise model performance.
Higher batch size requires more computing power (rule of thumb - batch size * steps per epoch = number of images per class)
'''

train_batches = ImageDataGenerator().flow_from_directory(train_path, target_size=(224,224),classes=['Empty', 'Full', 'Half-Full', 'No_Bin'], batch_size=14)
valid_batches = ImageDataGenerator().flow_from_directory(valid_path, target_size=(224,224),classes=['Empty', 'Full', 'Half-Full', 'No_Bin'], batch_size=10)

'''
Load in VGG19 model and initialise a sequential model.
Copy all layers from VGG19 model to sequential model except last dense layer.
Freeze layers in new model so the weights aren't changed.
Add new dense layer with the no. of classes specified (4 in this case)
Compile model with loss function and optimiser. Learning rate can be altered to optimise model,
start with lr of 0.001 and change by multiples of 10 up and down to optimise how the model learns.
Too high of a learning rate will lead to over-fitting.
Evaluate model with generator specifing no. of epochs and steps per epoch.
When optimising do a small number of epochs untill you can see the model is learning (val_accuracy increasing over time and val_loss decreasing)
'''

vgg19_model = keras.applications.vgg19.VGG19()
model = Sequential()
for layer in vgg19_model.layers:
    model.add(layer)
model.layers.pop()
for layer in model.layers:
    layer.trainable = False
model.add(Dense(4, activation='softmax'))
model.compile(Adam(lr=.05), loss = 'categorical_crossentropy', metrics=['accuracy'])
history = model.fit_generator(train_batches, epochs=7 , steps_per_epoch=100, validation_data=valid_batches, validation_steps=25, verbose=2)

model.save("C:/Users/domin/OneDrive/Desktop/modelrubbish.h5")
model.save_weights("C:/Users/domin/OneDrive/Desktop/model1rubbishw.h5")
model_json = model.to_json()
with open("C:/Users/domin/OneDrive/Desktop/modelrubbish.json","w") as json_file:
	json_file.write(model_json)

acc = history.history['acc']
val_acc = history.history['val_acc']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'b', label='Training acc')
plt.plot(epochs, val_acc, 'r', label='Validation acc')
plt.title('Training and validation accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()

#Use to display the images in a batch with their labels (un-comment the three lines following the method to see this)

def plots(ims, figsize=(12,6), rows=1, interp=False, titles=None):
    if type(ims[0]) is np.ndarray:
        ims = np.array(ims).astype(np.uint8)
        if (ims.shape[-1] != 3):
            ims = ims.transpose((0,2,3,1))
    f = plt.figure(figsize=figsize)
    cols = len(ims)//rows if len(ims) % 2 == 0 else len(ims)//rows + 1
    for i in range(len(ims)):
        sp = f.add_subplot(rows, cols, i+1)
        sp.axis('Off')
        if titles is not None:
            sp.set_title(titles[i], fontsize=16)
        plt.imshow(ims[i], interpolation=None if interp else 'none')

#imgs, labels = next(test_batches)
#plots(imgs,titles=labels)

#plt.show()

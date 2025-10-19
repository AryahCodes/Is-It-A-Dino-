import matplotlib.pyplot as plt
import numpy as np
import PIL
import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import pathlib
import os


#Questions to learn from
#"What does 'epochs' mean?"
#"How do I load images in Keras?"
#"Why do we need train/test split?"
#"What's the difference between Conv2D and Dense layers?"
#"What's a good optimizer to use?"

batch_size = 32
img_height = 224
img_width = 224

#I want to load data from processed into datasets
train_ds = tf.keras.utils.image_dataset_from_directory(
  "/Users/aryahb/IsItADino/is-it-a-dino/data/processed/train",
  labels='inferred',
  image_size=(img_height, img_width),  
  batch_size=batch_size)

test_ds = tf.keras.utils.image_dataset_from_directory(
  "/Users/aryahb/IsItADino/is-it-a-dino/data/processed/test",
  labels='inferred',
  image_size=(img_height, img_width),  
  batch_size=batch_size)

class_names = train_ds.class_names
# plt.figure(figsize=(10, 10))
# for images, labels in train_ds.take(1):
#   for i in range(9):
#     ax = plt.subplot(3, 3, i + 1)
#     plt.imshow(images[i].numpy().astype("uint8"))
#     plt.title(class_names[labels[i]])
#     plt.axis("off")
# plt.show()

#make sure data is split.
AUTOTUNE = tf.data.AUTOTUNE
#train_ds.cache keeps data in ram. So its easier to retrive for more epochs.
#prefetch makes it so it will overlap work. When GPU is training the 
#tensorflow can load and perpare batch N+1 in background.
#AUTOTUNE lets tensorflow pick the optimal number of batches.
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

#Standardize data so make range be [0,1].
normalization_layer = layers.Rescaling(1./255)

#Make simple model
num_classes = len(class_names)

#When building a model the model can overfit. A way to maybe fix that is
#By using dropout layers. or data agumentation

#data agumentation means 
#random transformations that yield believable-looking images
data_augmentation = keras.Sequential(
  [
    layers.RandomFlip("horizontal",
                      input_shape=(img_height,
                                  img_width,
                                  3)),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1),
  ]
)

#Add droplets layers too.
#When adding to a layer it randomly drops off a number of output units
#from the layer during the trianing process.
#  layers.Dropout(0.2),

#builds model
model = Sequential([
  data_augmentation,
  layers.Rescaling(1./255),  # Your images are 224×224
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Dropout(0.2),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Dropout(0.3),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Dropout(0.4),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(1, activation='sigmoid')  # Changed for binary classification!
])

#We use binary because we are doing yes or no. 2 options
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

model.summary()

#When training a model you can have funcitons to do 
#special things automatically. Like stop early if it stoped improving 
#After 5 epochs. Use when training takes too long or you are experimenting 
#with epochs.

#Lets add a call back
early_stop = EarlyStopping(
    monitor='val_loss',
    patience=2,             # stop if no improvement for 2 epochs
    restore_best_weights=True
)

checkpoint = ModelCheckpoint(
    'models/best_dino.keras',  # save the best model (lowest val_loss)
    monitor='val_loss',
    save_best_only=True
)

history = model.fit(
    train_ds,
    validation_data=test_ds,
    epochs=30,               # can go high; early stop will handle it
    callbacks=[early_stop, checkpoint]
)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

#Loss when training on train data
loss = history.history['loss']
# Loss when EVALUATING on validation/test data (not training on it!)
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

# ✅ Save model and copy to Drive
os.makedirs('models', exist_ok=True)
model.save('models/dinosaur_classifier.keras')

#Ran on colab so this might show an error in an IDE like vs code.
!cp models/dinosaur_classifier.keras /content/drive/MyDrive/IsItADino/
print("☁️ Copied model to Google Drive folder: MyDrive/IsItADino/")

#Overfitting is a big problem.
#use data agumentation to fix it. Generate more training data
#by agumenting exsisting examples using random transformations.
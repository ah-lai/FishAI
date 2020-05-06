# Class of the acticture of CNN 
import keras
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D , Flatten
from keras.preprocessing.image import ImageDataGenerator
from keras.applications import VGG16

# Define Variables 
train_dir = "pre-process/train"
val_dir = "pre-process/valid"

batch_size_training=20
num_class = 5


# we need switch the RGB

# Create Data Aug objects
trn_gen = ImageDataGenerator(rotation_range=25, width_shift_range=0.1,
	height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
	horizontal_flip=True, fill_mode="nearest")

val_gen = ImageDataGenerator()

trn_data = trn_gen.flow_from_directory(train_dir, target_size=(224, 224),
    batch_size=batch_size_training,
    class_mode='categorical')

val_data = val_gen.flow_from_directory(val_dir,target_size=(224,224),    
    batch_size=batch_size_training,
    class_mode='categorical')

# Create Model
model=Sequential()
model.add(VGG16(include_top=False,pooling='avg',weights='imagenet',))
model.add(Dense(num_class,activation="softmax"))
# Transfer Learning  - Freeze layers from pre-trained model
model.layers[0].trainable= False

# Compile model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Setup training variables 
steps_per_epoch_training = len(trn_data)
steps_per_epoch_validation = len(val_data)
num_epochs = 20

# Fit Model
fit_history = model.fit_generator(
    trn_data,
    steps_per_epoch=steps_per_epoch_training,
    epochs=num_epochs,
    validation_data=val_data,
    validation_steps=steps_per_epoch_validation,
    verbose=1,
)

#Save
model.save("model.h5")
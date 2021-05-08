from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.inception_v3 import preprocess_input
from keras.applications.inception_v3 import decode_predictions
from keras.models import model_from_json 
import numpy as np
import tensorflow as tf

# initialise class names

class_names = ['benign', 'malignant', 'normal']

# load in the model

json_file = open(r'model.json','r')
loaded_model_json = json_file.read()
json_file.close()

# use Keras model_from_json to make a loaded model

loaded_model = model_from_json(loaded_model_json)
print(loaded_model)

# load weights into new model

loaded_model.load_weights(r"model.h5")
print("Loaded Model from disk")

loaded_model.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

loaded_model.summary()

def getPrediction(filename):

    model = loaded_model
    image = load_img('uploads/'+filename, target_size=(150, 150))

    img_array = img_to_array(image)
    img_array = img_array / 255.0
    img_array = tf.expand_dims(img_array, 0) # Create a batch

    predictions = model.predict(img_array)
    score = tf.nn.softmax(predictions[0])

    print(
        "This image most likely belongs to {} with a {:.2f} percent confidence."
        .format(class_names[np.argmax(score)], 100 * np.max(score))
    )

    final_prediction = class_names[np.argmax(score)]
    confidence_score = 100 * np.max(score)

    return (final_prediction, confidence_score)
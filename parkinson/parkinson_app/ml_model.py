import numpy as np
import keras
from keras.models import Sequential
from keras.models import model_from_json
import os
import pathlib

cwd = pathlib.Path().absolute()

# loading model from json file and create model
json_file = open(str(cwd)+'/parkinson_app/static/parkinson_app/model_data/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)

# load weights into new model
loaded_model.load_weights(str(cwd)+'/parkinson_app/static/parkinson_app/model_data/model-weights.h5')

def predict_class(jitter_per, jitter_abs, jitter_ddp, mdvp_ppq, mdvp_rap, mdvp_shimmer, mdvp_shimmer_db, shimmer_apq3, shimmer_apq5, mvp_avq, shimmer_dda, rpde, d2, nhr, spread2, ppe):
    # Creating a vector array for feeding into the Neural Network
    test_values = [[jitter_per, jitter_abs, jitter_ddp, mdvp_ppq, mdvp_rap, mdvp_shimmer, mdvp_shimmer_db, shimmer_apq3, shimmer_apq5, mvp_avq, shimmer_dda, rpde, d2, nhr, spread2, ppe]]
    
    #Compiling the loaded model 
    loaded_model.compile(loss = 'categorical_crossentropy', optimizer='adamax', metrics=['accuracy'])
    
    # This function will predict the class for the new given values
    result = loaded_model.predict_classes(test_values, verbose=1)

    # status 1 = sick, 0 = healthy
    return result
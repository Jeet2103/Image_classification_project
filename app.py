import numpy as np
import os
import sys
import re
import glob
from keras.applications.imagenet_utils import preprocess_input , decode_predictions
from keras.models import load_model
from keras.preprocessing import image
from flask import Flask, redirect, url_for, request,render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)

model_path = 'vgg19.h5'
model = load_model(model_path)
model.make_predict_function()

#Preprocessing function
def model_predict(img_path, model):
    img = image.load_img(img_path,target_size = (224,224))
    x = image.img_to_array(img)
    x = np.expand_dims(x,axis = 0)
    x= preprocess_input(x)
    preds = model.predict(x)
    return preds
@app.route('/',methods = ['GET'])
def index():
    return render_template('index.html')

@app.route('/predict', methods =['GET','POST'])
def upload():
    if request.method == "POST":
        ## Get the file from the POST
        f = request.files['file']
        ## Save the file to uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath,'uploads',secure_filename(f.filename)
        )
        f.save(file_path)
        ## Here we make you prediction
        pred = model_predict(file_path, model)
        ## Decode the prediction 
        pred_class =  decode_predictions(pred,top = 1)
        result = str(pred_class[0][0][1])
        return result
    return None
        

if __name__ == '__main__':
    app.run(debug=True)

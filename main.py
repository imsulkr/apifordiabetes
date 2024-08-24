# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import json


app = FastAPI() 

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers=["*"]
    )

class model_input(BaseModel):
    Pregnancies : int
    Glucose : int
    BloodPressure : int
    SkinThickness: int
    Insulin : int
    BMI : float
    DiabetesPedigreeFunction : float
    Age : int 
    
    
#loading the saved model
try:
    diabetes_model = pickle.load(open('diabities.sav', 'rb'))
except FileNotFoundError:
    print("Model file not found. Ensure the file path is correct.")
except Exception as e:
    print(f"An error occurred while loading the model: {e}")
#creating api

@app.post('/diabetes_prediction')
def diabetes_pred(input_parameters : model_input):
    input_data = input_parameters.json()
    input_dictionary = json.loads(input_data)  
    preg = input_dictionary["Pregnancies"]
    glu = input_dictionary["Glucose"]  
    bp = input_dictionary["BloodPressure"]  
    skin = input_dictionary["SkinThickness"]  
    insulin = input_dictionary["Insulin"]  
    bmi = input_dictionary["BMI"]  
    dpf = input_dictionary["DiabetesPedigreeFunction"]  
    age = input_dictionary["Age"]  

    input_list = [preg,glu,bp,skin,insulin,bmi,dpf,age]
    # Check if model is loaded before making prediction
    if 'diabetes_model' not in globals():
        return "Model is not loaded. Check the model loading code."
    prediction =diabetes_model.predict([input_list])
    if prediction[0] == 0:
        return 'The person is not Diabetic'
    else:
        return 'The person is Diabetic'

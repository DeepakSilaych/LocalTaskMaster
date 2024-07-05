import pandas as pd
import numpy as np
import pywt
import tensorflow as tf
from tensorflow.keras.models import load_model
import os
from connections import awsstation, hourwiseprediction, fetchstationdata

import logging

logger = logging.getLogger(__name__)

def dwt_decomposition(data, wavelet='db7', level=3):
    coeffs = pywt.wavedec(data, wavelet, level=level)
    cA3, cD3, cD2, cD1 = coeffs
    only_A3_signal = pywt.waverec([cA3, np.zeros_like(cD3), np.zeros_like(cD2), np.zeros_like(cD1)], wavelet)
    only_D3_signal = pywt.waverec([np.zeros_like(cA3), cD3, np.zeros_like(cD2), np.zeros_like(cD1)], wavelet, mode='constant')
    only_D2_signal = pywt.waverec([np.zeros_like(cA3), np.zeros_like(cD3), cD2, np.zeros_like(cD1)], wavelet)
    only_D1_signal = pywt.waverec([np.zeros_like(cA3), np.zeros_like(cD3), np.zeros_like(cD2), cD1], wavelet)
    return only_A3_signal[:len(data)], only_D3_signal[:len(data)], only_D2_signal[:len(data)], only_D1_signal[:len(data)]

def predict_hourly():
    now = pd.Timestamp.now(tz='Asia/Kolkata')

    # Define parameters
    n_steps_in = 3
    num_hours = 24

    # Loop through each station
    for station in awsstation():
        stationname = station['name']
        temp = {}
        
        # fetch all station data in latest to oldest order
        stationdata = fetchstationdata({'station': station['station_id']})
        print(stationdata)
        stationdata = [data['rainfall'] for data in stationdata]
        
        #convert 15min data to hourly data by adding every 4 data
        stationdata_hourly = [sum(stationdata[i:i+4]) for i in range(0, len(stationdata), 4)] 
        values = np.array(stationdata_hourly).reshape(-1, 1)
        n_features = values.shape[1]
    
        # Prepare the input and output sequences
        n_samples = len(values) - n_steps_in + 1
        X_test = np.zeros((n_samples, n_steps_in, n_features))
        # y = np.zeros((n_samples, n_steps_out))
    
        for i in range(n_samples):
            X_test[i] = values[i:i + n_steps_in]
    
    
        # Apply DWT to each sample
        X_test_A3 = np.zeros_like(X_test)
        X_test_D3 = np.zeros_like(X_test)
        
    
        for i in range(len(X_test)):
            for j in range(n_features):
                data = X_test[i, :, j]
                only_A3_signal, only_D3_signal, _, _ = dwt_decomposition(data, wavelet='db7', level=3)
                X_test_A3[i, :, j] = only_A3_signal
                X_test_D3[i, :, j] = only_D3_signal
                
    
        # Load the models for this station
        model_A3_path = os.path.join('./models/hourly_models', stationname, f'{stationname}_cA3_LSTM.h5')
        model_D3_path = os.path.join('./models/hourly_models', stationname, f'{stationname}_cD3_LSTM.h5')

        network_A3 = load_model(model_A3_path)
        network_D3 = load_model(model_D3_path)
    
        # Predict for multiple hours for A3
        predictions_all_hours_A3 = []
        y_predicted_A3_test = network_A3.predict(X_test_A3)
        predictions_all_hours_A3.append(y_predicted_A3_test)
    
        # Initialize appended_data with the initial test data and the first hour prediction
        X_test_flattened_A3 = X_test_A3.reshape(-1, X_test_A3.shape[1])
        appended_data_A3 = np.concatenate((X_test_flattened_A3, y_predicted_A3_test), axis=1)

        # Predict the second hour
        X_test_new_A3 = np.delete(appended_data_A3, 0, axis=1)
        X_test_new_reshaped_A3 = np.reshape(X_test_new_A3, (X_test_new_A3.shape[0], X_test_new_A3.shape[1], 1))
        y_predicted_A3_test_2_hour_lead = network_A3.predict(X_test_new_reshaped_A3)
        predictions_all_hours_A3.append(y_predicted_A3_test_2_hour_lead)
        appended_data_A3 = np.concatenate((appended_data_A3, y_predicted_A3_test_2_hour_lead), axis=1)

        for hour in range(3, num_hours + 1):
            # For the current hour onwards, delete the first (hour - 1) columns
            X_test_new_A3 = np.delete(appended_data_A3, slice(0, hour - 1), axis=1)
            X_test_new_reshaped_A3 = np.reshape(X_test_new_A3, (X_test_new_A3.shape[0], X_test_new_A3.shape[1], 1))
            y_predicted_next_hour_A3 = network_A3.predict(X_test_new_reshaped_A3)
            appended_data_A3 = np.concatenate((appended_data_A3, y_predicted_next_hour_A3), axis=1)
            predictions_all_hours_A3.append(y_predicted_next_hour_A3)


        # Predict for multiple hours for D3
        predictions_all_hours_D3 = []
        y_predicted_D3_test = network_D3.predict(X_test_D3)
        predictions_all_hours_D3.append(y_predicted_D3_test)
    
        # Initialize appended_data with the initial test data and the first hour prediction
        X_test_flattened_D3 = X_test_D3.reshape(-1, X_test_D3.shape[1])
        appended_data_D3 = np.concatenate((X_test_flattened_D3, y_predicted_D3_test), axis=1)

        # Predict the second hour
        X_test_new_D3 = np.delete(appended_data_D3, 0, axis=1)
        X_test_new_reshaped_D3 = np.reshape(X_test_new_D3, (X_test_new_D3.shape[0], X_test_new_D3.shape[1], 1))
        y_predicted_D3_test_2_hour_lead = network_D3.predict(X_test_new_reshaped_D3)
        predictions_all_hours_D3.append(y_predicted_D3_test_2_hour_lead)
        appended_data_D3 = np.concatenate((appended_data_D3, y_predicted_D3_test_2_hour_lead), axis=1)

        for hour in range(3, num_hours + 1):
            # For the current hour onwards, delete the first (hour - 1) columns
            X_test_new_D3 = np.delete(appended_data_D3, slice(0, hour - 1), axis=1)
            X_test_new_reshaped_D3 = np.reshape(X_test_new_D3, (X_test_new_D3.shape[0], X_test_new_D3.shape[1], 1))
            y_predicted_next_hour_D3 = network_D3.predict(X_test_new_reshaped_D3)
            appended_data_D3 = np.concatenate((appended_data_D3, y_predicted_next_hour_D3), axis=1)
            predictions_all_hours_D3.append(y_predicted_next_hour_D3)
    
        predictions_all_hours_array_D3 = np.array(predictions_all_hours_D3)
        

        for hour in range(num_hours):
            cA3_pred = predictions_all_hours_A3[hour].flatten()
            cD3_pred = predictions_all_hours_D3[hour].flatten()
            cDoverall_pred = (cA3_pred + cD3_pred)

            temp [str(now + pd.Timedelta(hours=hour+1))] = cDoverall_pred.tolist()[0]

        print ("-----------------------------------",temp.values())
        hourwiseprediction(
            {
                'station': station['station_id'],
                'hr_24_rainfall': temp.values()
            }
        )

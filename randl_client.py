import requests
import json
import pandas as pd
import numpy as np
import datetime
from dateutil import parser
from datetime import timedelta
import sys
import math
import ast
from io import StringIO


class Randl:    
    def __init__(self):        
        self.url_base = "http://seismic-ai.com:8011/randl/"
        #self.url_base = "http://127.0.0.1:8000/randl/"
        
        self.bulletin_start = '2024-05-01T00:00:00'
        self.bulletin_end = '2024-05-11T00:00:00' 
        self.bulletin_n_stations= '100'
        self.bulletin_n_events= '1' 
        self.bulletin_drop_fraction = '0.2'
        self.bulletin_seed = '555'
        
        self.window_start = '2024-05-10 18:43:15.431390'
        self.window_length = '1800'
        self.window_min_phases_needed= '5'
        self.window_exclude_associated_phases= 'False'
        #self.window_exclude_duplicate_stations= 'True'
        self.window_step_size = 1
        
        #TODO finish setters for dml variables
        self.dml_models = ['pwave']
        self.dml_sampling = ['full']
        self.dml_num_samples = '10'
        self.dml_arids = ['None'] # Update this to something cleaner/more robust
        self.dml_pwave_modelpath = 'None'
        self.dml_exclude_duplicate_stations= 'True'
        self.dml_baz_modelpath = 'None'
        
        #TODO cleanup beamsearch call
        self.beam_width = '5'
        self.beam_max_dist = '5000'
        self.beam_max_time = '500'
        self.beam_sequence_dist = '500'
        self.beam_sequence_timedist = '500'
        

    def validate_datetime_bulletin(self, timestamp):
        try:
            time = parser.parse(timestamp)
        except:
            print("Invalid date format")
        return time.strftime('%Y-%m-%dT%H:%M:%S')
    
    def validate_datetime(self, timestamp):
        try:
            time = parser.parse(timestamp)
        except:
            print("Invalid date format")
        return time.strftime('%Y-%m-%d %H:%M:%S.%f')
    
    
    def set_bulletin_start(self, starttime):
        try: 
            time = self.validate_datetime_bulletin(starttime)
        except:
            return
        self.bulletin_start = time   
        
    def set_bulletin_end(self, starttime):
        try: 
            time = self.validate_datetime_bulletin(starttime)
        except:
            return
        self.bulletin_end = time
        
    def set_bulletin_n_stations(self, n):
        if type(n) is int:
            self.bulletin_n_stations = str(n)
        else:
            print("Int required")
            
    def set_bulletin_n_events(self, n):
        if type(n) is int:
            self.bulletin_n_events = str(n)
        else:
            print("Int required")
            
    def set_bulletin_drop_fraction(self, n):
        if type(n) is float:
            self.bulletin_drop_fraction = str(n)
        else:
            print("Float required")
            
    def set_bulletin_seed(self, n):
        if type(n) is int:
            self.bulletin_seed = str(n)
        else:
            print("Int required") 
                    
    def set_window_start(self, starttime):
        try: 
            time = self.validate_datetime(starttime)
        except:
            return
        self.window_start = time
        
    def set_window_length(self, length):
        if type(length) is int:
            self.window_length = str(length)
        else:
            print("Int required")
            
    def set_window_phases_required(self, phases):
        if type(phases) is int:
            self.window_min_phases_needed = str(phases)
        else:
            print("Int required")
            
    def set_window_exclude_associated_phases(self, b):
        if type(b) is bool:
            self.window_exclude_associated_phases = str(b)
        else:
            print("Boolean required")
            
    def set_dml_exclude_duplicate_stations(self, b):
        if type(b) is bool:
            self.dml_exclude_duplicate_stations = str(b)
        else:
            print("Boolean required")
            
    def set_dml_num_samples(self, b):
        if type(b) is int:
            self.dml_num_samples = str(b)
        else:
            print("Int required")    
    
    # add input checking
    def set_dml_models(self, models):
        self.dml_models = models
    # add input checking    
    def set_dml_sampling(self, sampling):
        self.dml_sampling = sampling
    def set_dml_arids(self, arids):
        list_arids = []
        for arid in arids:
            list_arids.append(str(arid))
        self.dml_arids = list_arids        
    def set_dml_pwave_model(self, path):
        if type(path) is str:
            self.dml_pwave_modelpath = path
        else:
            print("String required")
    def set_dml_baz_model(self, path):
        if type(path) is str:
            self.dml_baz_modelpath = path
        else:
            print("String required")
        
    def set_beamwidth(self, width):
        if type(width) is int and width > 0:
            self.beam_width = str(width)
        else:
            print("Positive int required")
            
    def set_beam_maxdist(self, dist):
        if type(dist) is int and dist > 0:
            self.beam_max_dist = str(dist)
        else:
            print("Positive int required")
    
    def set_beam_maxtime(self, time):
        if type(time) is int and time > 0:
            self.beam_max_time = str(time)
        else:
            print("Positive int required")
            
            
    def set_beam_sequencedist(self, dist):
        if type(dist) is int and dist > 0:
            self.beam_sequence_dist = str(dist)
        else:
            print("Positive int required")
            
    def set_beam_sequencetimedist(self, time):
        if type(time) is int and time > 0:
            self.beam_sequence_timedist = str(time)
        else:
            print("Positive int required")

            
    def create_bulletin(self):
        
        req = {'n_stations': self.bulletin_n_stations ,"n_events":self.bulletin_n_events,
            "drop_fraction": self.bulletin_drop_fraction, 
            "datetime_start": self.bulletin_start,
            "datetime_end":self.bulletin_end,
              "seed": self.bulletin_seed }

        url = self.url_base + 'create_bulletin'
        headers = {"accept": "application/json",
            "Content-Type": "application/json"}

        response = requests.post(url, headers=headers, data=json.dumps(req))

        # Check the response
        if response.status_code == 200:
            print("Success")
        else:
            print("Error:", response.status_code, response.text)
            return None         
        
        bulletin = pd.read_json(StringIO(response.json()["result"]))
        rename_dic = {"STA_LAT":"LAT_STA", "STA_LON":"LON_STA","TIME":"TIME_ARRIV"}
        bulletin.rename(rename_dic, axis='columns', inplace=True)
        bulletin['TIME_ARRIV'] = bulletin.TIME_ARRIV.astype(str)
        bulletin['ORIG_TIME'] = bulletin.ORIG_TIME.astype(str)
        #bulletin['STA'] = bulletin.STA.astype(str)
        bulletin["BACK_AZIMUTH"]=0
        bulletin = bulletin.loc[bulletin.IPHASE == "P", :]
        bulletin.reset_index(drop=True, inplace=True)

        return bulletin
    
    
    def window_catalog(self, bulletin):    
        bulletin_dic = bulletin.to_dict()

        req = {'window_length': self.window_length ,"min_phases_needed":self.window_min_phases_needed,
                "exclude_associated_phases": self.window_exclude_associated_phases, "step_size": self.window_step_size ,
                "start_time":self.window_start, "catalog": bulletin_dic }

        url = self.url_base + 'window'
        headers = {"accept": "application/json",
            "Content-Type": "application/json"}

        response = requests.post(url, headers=headers, data=json.dumps(req))

        if response.status_code == 200:
            print("Success")
        else:
            print("Error:", response.status_code, response.text)
            return None
        window = pd.read_json(StringIO(response.json()["result"]))
        window['ORIG_TIME'] = window.ORIG_TIME.astype(str)    
        return window
        
    def dml_prediction(self, window):
        window_dict = window.to_dict()
        req = {"models": self.dml_models, "sampling": self.dml_sampling, "num_samples": self.dml_num_samples, 
               "arids": self.dml_arids, "pwave_model": self.dml_pwave_modelpath, "baz_model": self.dml_baz_modelpath, 
               "exclude_duplicate_stations": self.dml_exclude_duplicate_stations, "catalog": window_dict }

        url = self.url_base + "dml_handler"

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, data=json.dumps(req))
        if response.status_code == 200:
            print("Success")
        else:
            # If the request failed, print the error details
            print("Error:", response.status_code, response.text)
            return None
            
        return pd.read_json(StringIO(response.json()["result"]))     
    
    
    def beamsearch(self, window, dml_predictions):
        window_dict = window.to_dict()
        dml_dict = dml_predictions.to_dict()

        req = {"dml_predictions": dml_dict, "window": window_dict, "beam_width": self.beam_width, "max_dist": self.beam_max_dist,
              "max_time": self.beam_max_time, "sequence_dist": self.beam_sequence_dist, "sequence_time": self.beam_sequence_timedist,
               "pwave_model": self.dml_pwave_modelpath, "baz_model": self.dml_baz_modelpath, "base_url": self.url_base}


        url = self.url_base + "beamsearch"

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        response = requests.post(url, headers=headers, data=json.dumps(req))
        if response.status_code == 200:
            print("Success")
        else:
            # If the request failed, print the error details
            print("Error:", response.status_code, response.text)
            
        return response.json()["result"]

            
    def __repr__ (self):
        return "URL:" + self.url_base + "\n\n-Bulletin-\nStart:\t\t" + self.bulletin_start + "\nEnd:\t\t" + self.bulletin_end \
    + "\nStations:\t" + self.bulletin_n_stations + "\nEvents:\t\t" + self.bulletin_n_events \
    + "\nDrop fraction:\t" + self.bulletin_drop_fraction + "\nSeed:\t" + self.bulletin_seed + "\n\n-Window-\nStart:\t\t\t" + self.window_start \
    + "\nLength:\t\t\t" + self.window_length + "\nMin_phases:\t\t" + self.window_min_phases_needed \
    + "\nExclude associated:\t" + self.window_exclude_associated_phases +"\n\n-DML-\nModels:\t\t" + str(self.dml_models) \
    + "\nSampling:\t" + str(self.dml_sampling) + "\nNum_samples:\t" + str(self.dml_num_samples) \
    + "\nArids:\t\t" + str(self.dml_arids) + "\nPwave_model:\t" + str(self.dml_pwave_modelpath) \
    + "\nBaz_model:\t" + str(self.dml_baz_modelpath) + "\nExclude stations:\t" + self.dml_exclude_duplicate_stations \
    + "\n\n-Beamsearch-\nBeam width:\t" + self.beam_width + "\nMax dist:\t" + self.beam_max_dist \
    + "\nMax time:\t" + self.beam_max_time + "\nSequence dist:\t" + self.beam_sequence_dist + "\nSequence time:\t" + self.beam_sequence_timedist


# -*- coding: utf-8 -*-
"""
Created on Mon Nov  4 09:24:02 2019

@author: rfernandezjimenez
"""

import os  
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_Options

import time
import numpy as np
import pandas as pd
from tqdm import tqdm

import matplotlib.pyplot as plt
import seaborn as sns
sns.set() # pyplot functions with seaborn layout

#%%

class Kaggle():
    def __init__(self):
        chrome_options = chrome_Options()  
        chrome_options.add_argument("--headless")  
        chrome_options.binary_location = '/Program Files (x86)/Google/Chrome/Application/chrome.exe'
        self.driver_chrome = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"), options=chrome_options)
        self.driver_chrome.set_window_size(1600, 800)
        
    def Close_driver(self):
        self.driver_chrome.close()
        
    def Get_scores(self, url):
        self.driver_chrome.get(url)
        
        # Find the "load more scores" button
        load_more_button = self.driver_chrome.find_element_by_class_name('competition-leaderboard__load-more-count')
        load_more_button.click()
        
        # Wait for load all the entries
        time.sleep(10)
        # Get the scores
        print('Reading scores....')
        score_classes = self.driver_chrome.find_elements_by_class_name('competition-leaderboard__td-score')
        print('Processing scores....')
        self.scores = [score.text for score in tqdm(score_classes)]
        self.scores = [np.float(i) for i in self.scores]
        self.scores = np.array(self.scores)
    
    def Save_backup_scores(self, filename = ''):
        df_scores = pd.DataFrame({'Position':np.arange(1, len(self.scores)+1),
                                  'Score':self.scores})
        df_scores.to_csv(filename, index = False)
    
    def Load_backup_scores(self, filename = ''):
        df_scores = pd.read_csv(filename)
        self.scores = df_scores.Score
        
    def Represent_my_score(self, my_score):
        # The possition depends if its a crescent or decrescent score
        if np.sum(np.diff(self.scores)) > 0:
            next_to_me = np.min(np.where(my_score < self.scores))
        else:
            next_to_me = np.min(np.where(my_score > self.scores))
            
        score_next_to_me = self.scores[next_to_me]
        score_previous_to_me = self.scores[next_to_me-1]
            
        '''
        (In the crescent scores way)
        Now, we define how much is the distance from our positions
        For example, our score is 1.2 and we are between position 122 and 123.
        The relative scores are x122 = 1.19999... and x123 = 1.25
        Then, if we want to be realistics, we must set our position more closer to x122 than x123
        We do it with an imaginary line that starts at score122 (0%) and ends in score123 (100%), whose 
            lenght is (score123-score122)
        In the other hand, we have that our score is (our_score - score122) greather than score122, then 
            our position is (our_score - score122)/(score123-score122)*100% greather than x122, ergo
            our_position = x122 + (our_score - score122)/(score123-score122) <= x123
        '''
        my_position = (next_to_me-1) + (my_score - score_previous_to_me)/(score_next_to_me - score_previous_to_me)
        
        plt.plot(self.scores)
        plt.scatter(x = my_position, y = my_score, color = 'red')
        plt.text(x = my_position - 0.075*len(self.scores), y = my_score, s = 'Me!', color = 'red')
        plt.ylabel('Score')
        plt.xlabel('Position')
        plt.show()

#%%
# Example
kaggle_class = Kaggle()

url = 'https://www.kaggle.com/c/ashrae-energy-prediction/leaderboard'
kaggle_class.Get_scores(url)

#%%
# Plot score
kaggle_class.Represent_my_score(my_score = 2)

#%%
# Save backup
kaggle_class.Save_backup_scores(filename = 'energy-prediction.csv')

#%%
# Load backup
kaggle_class.Load_backup_scores(filename = 'energy-prediction.csv')





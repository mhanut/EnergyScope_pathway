#s!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  26 2022

@author: rixhonx
"""


print("General imports")
import numpy as np
import os,sys
from os import system
import pandas as pd

pylibPath = os.path.abspath("../pylib")    # WARNING ! pwd is where the MAIN file was launched !!!

if pylibPath not in sys.path:
    sys.path.insert(0, pylibPath)

def fill_df(output_dir, df_learning, nb_batch):
    df_temp = pd.DataFrame(columns=df_learning.columns)
    n_epoch_batch = 0
    for i in range(1,nb_batch+1):
        df_obs = pd.read_csv(output_dir+'batch{}/observation.txt'.format(i), header = None, sep = ' ').reset_index(drop=True)
        df_act = pd.read_csv(output_dir+'batch{}/action.txt'.format(i), header = None, sep = ' ').reset_index(drop=True)
        df_rew = pd.read_csv(output_dir+'batch{}/reward.txt'.format(i), header = None, sep = ' ').reset_index(drop=True)
        df_cost = pd.read_csv(output_dir+'batch{}/cost.txt'.format(i), header = None, sep = ' ').reset_index(drop=True)

        df_temp = pd.concat([df_obs,df_cost.iloc[:,1:],df_act.iloc[:,2:],df_rew.iloc[:,1:]],axis=1, join='inner')
        df_temp['batch'] = i
        df_temp['episode'] = n_epoch_batch + df_act.iloc[:,0]
        df_temp.columns = df_learning.columns
        if i!=1:
            df_learning = pd.concat([df_learning,df_temp])
        else:
            df_learning = df_temp
        n_epoch_batch += df_act.iloc[-1,0]
    return df_learning

def updated_status_2050(df_learning):
    ep_success = df_learning['episode'].loc[df_learning['status_2050']=='Success']
    ep_failure = df_learning['episode'].loc[df_learning['status_2050']=='Failure']
    ep_failure_imp = df_learning['episode'].loc[df_learning['status_2050']=='Failure_imp']

    df_learning['status_2050'].loc[df_learning['episode'].isin(ep_success)] = 'Success'
    df_learning['status_2050'].loc[df_learning['episode'].isin(ep_failure)] = 'Failure'
    df_learning['status_2050'].loc[df_learning['episode'].isin(ep_failure_imp)] = 'Failure_imp'
    
    df_learning = df_learning.dropna()
    
    return df_learning
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 12:41:05 2023

@author: a863900
"""

import streamlit as st
from tkinter import Tk
import sys
import os
import pathlib
###########################################################################
from tkinter import *
from tkinter import filedialog as fd
###########################################################################

from asammdf import MDF, Signal
import mdfreader
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from pytz import timezone
import pytz
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
##########################################################################


st.header("DATA INFORMATIONS")





exp1=st.expander("Path & Data Details", expanded=True)
with exp1:
    
        st.metric(label="Data Volume", value=st.session_state["TotalPathSize"])
        st.text(st.session_state["Mydir"])
        col1,col2=st.columns(2)
        col1.metric(label="Logs_Caps", value=st.session_state["i1"])
        col2.metric(label="Logs_Continus", value=st.session_state["i2"])
        
        
        if  st.session_state["CapsHS"]!=[]:
            NameHS=['CapsLogs_HS']
            CapsHS=pd.DataFrame(st.session_state["CapsHS"])
            CapsHS.columns=NameHS
            HSfile=len(CapsHS)
            col1.metric(label="CapsHS", value=HSfile)
    
        
    
    
    
exp2=st.expander("CapsLogs_HS",expanded=False)    
with exp2:        
        st.dataframe(st.session_state["CapsHS"])    
    
    
#exp3= st.container("Parameters list")
#with exp3:
exp3_1=st.expander("Parameters list_Logs Continus",expanded=False)    
with exp3_1:
    #shdfC=AgGrid(st.session_state["dfC"],key="2",data_return_mode = 'FILTERED')
    gob = GridOptionsBuilder.from_dataframe(st.session_state["dfC"])
    for column in st.session_state["dfC"].columns:
        gob.configure_column(column, filter=True)
    gridOptions = gob.build()
    
    shdfC=AgGrid(st.session_state["dfC"], gridOptions=gridOptions, update_mode=GridUpdateMode.MODEL_CHANGED)
    st.write(shdfC,use_container_width=True)
        
exp3_2=st.expander("Parameters list_Logs Caps",expanded=False)
with exp3_2:    
    #shdfL=AgGrid(st.session_state['dfL'],data_return_mode = 'FILTERED')
    gob = GridOptionsBuilder.from_dataframe(st.session_state['dfL'])
    for column in st.session_state['dfL'].columns:
        gob.configure_column(column, filter=True)
    gridOptions = gob.build()
    
    shdfL=AgGrid(st.session_state['dfL'], gridOptions=gridOptions, update_mode=GridUpdateMode.MODEL_CHANGED)
    st.write(shdfL,use_container_width=True)
    
    
        
        
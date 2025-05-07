# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 14:58:58 2023

@author: a863900
"""

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype)
import plotly.express as px
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import numpy as np
import plotly
#from plotly.offline import iplot, init_notebook_mode,iplot_mpl
#init_notebook_mode()  #connected = True 
import sys
from PIL import Image
import requests
from io import BytesIO
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from st_clickable_images import clickable_images
from st_click_detector import click_detector
import base64
from pyxlsb import open_workbook as open_xlsb
import folium
from streamlit_option_menu import option_menu
#import datapane as dp
import os
import gc
import tables
#from streamlit_folium import st_folium
import plotly.figure_factory as ff



def dB_Export():
    
    Mydir=st.session_state["Mydir"] 
    
    df=st.session_state["Global_Tags"]
    time= pd.to_datetime(df.index)
    df.index=time
    df1=st.session_state["Param_Gen"]
    df1.index = pd.to_datetime(df1.index)
    df1.index=df1.index.tz_localize(None)
    
    
    
    left, right = df.align(df1, join="outer", axis=0)
    dB_HDF = pd.merge(left, right, how='outer', on=None,
                        left_index=True, right_index=True)
    
    dB_HDF=dB_HDF.infer_objects().dtypes
    Folder=st.session_state["Folder"]
    Folder
    os.chdir(Folder)
    basename = os.path.basename(Folder)
    
    
    name=(basename + ".h5")    
    
    
    store = pd.HDFStore(name)
    store['dB_HDF'] = dB_HDF
    
    store.close()
    
    #dB_HDF.to_hdf(name, key='dB', mode='w')


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    try:
        df['Time_TAG']=df.index.strftime('%Y-%m-%d %H:%M:%S')
    except:
        pass
    #df['Time_TAG'].strftime('%Y-%m-%d %H:%M:%S')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.close()
    processed_data = output.getvalue()
    return processed_data



def graph(df1: pd.DataFrame) -> pd.DataFrame:
    
    
    with modification_container:
        st.dataframe(df1)
        df_xlsx = to_excel(df1)
        st.download_button(label='📥 Download Current Result',
                                     data=df_xlsx ,
                                     file_name= 'df_test.xlsx')
    
    
        
    with container_Fig:
        
        groups = df1.groupby(['TAG_Type','Classification', pd.cut(df1.IVehicleSpeed, [-0.1, 30, 50, 70,90,110,130,150])])
        df2=groups.size().unstack()
        df2=df2.reset_index(level=[0,1])
        df2.columns=["TAG_Type","TAG_Event","0_30","30_50","50_70","70_90","90_110","110_130","130_150"]
    
        
        
        Fct=[]
        Evt=[]
        Range=[]
        Data=[]
        
        Vcol=['0_30','30_50',"50_70","70_90","90_110","110_130","130_150"]   #df4
        
        for col in Vcol:
            for idx in df2.index:
                
                Fct.append(df2['TAG_Type'][idx])
                Evt.append(df2['TAG_Event'][idx])
                Range.append(col)
                val=df2[col][idx]
                Data.append(val)
                
        df3 = pd.DataFrame({'Speed':  Range,
                       'Fonction':   Fct,
                       'Evenement': Evt,
                       'Values':    Data })

        df3=df3[df3.Evenement!=""]
        
        
        fig = px.sunburst(df3, path=['Fonction','Evenement','Speed'],values='Values',title='Répartition des évènements par classes de vitesse')
        fig.update_layout(margin = dict(t=30, l=30, r=30, b=30))
        
        st.plotly_chart(fig, use_container_width=True)
        
        
    
    
    
       
       
    with container_MAP:
           
           
           
           dfMAP=df1.rename(columns={"LATITUDE_GPS": "lat", "LONGITUDE_GPS": "lon"})
           ValidPT=dfMAP[dfMAP['lat'].notnull()] 
           ValidPT=ValidPT[ValidPT['lon'].notnull()]
           
           st.map(ValidPT)
          



def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
   
    
   """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
   
   global N
   global n 
   global df1
   with modification_container:
   #cont2=st.container() 
       modify = st.checkbox("Add filters")
       N=[]
       n=[]



    
       if not modify:
            
            df=st.session_state["Global_Tags"]
            
            df1=df.copy()
            
            
            graph(df1)
            return (df)
            
            
            
        
       df = df.copy()
    
        # Try to convert datetimes into a standard format (datetime, no timezone)
       for col in df.columns:
            if is_object_dtype(df[col]):
                try:
                    df[col] = pd.to_datetime(df[col])
                except Exception:
                    pass
    
            if is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.tz_localize(None)

   #modification_container = st.container()
   
   
   #with modification_container:
       to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
       for column in to_filter_columns:
            left, right = st.columns((1, 20))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]
                    
        
             
               
        #st.session_state["df1"]= df
   df1=df.copy()
        #graph(df1)              #graph(cpt1)
        #with cont2:
   graph(df1)
        
        
##################################################################################################      
#Construction Pages Events
###########################################################################################        


   

st.sidebar.button("dB_Export",on_click=dB_Export) #, on_click=Update





modification_container = st.container()        
container_Graph = st.container()
container_Fig=st.container()
container_Fig1=st.container()
container_MAP=st.expander("MAP")



cpt1=[]
df=st.session_state["Global_Tags"]
df1=df.copy()
COL_Filt2 = ['Support_Essai', 'Type_Essai', 'Calibration','TAG_Type', 'Classification', 'Item', 'stringValueNewComment', 'Criticity',
             'IVehicleSpeed', 'LATITUDE_GPS', 'LONGITUDE_GPS','Capsule']
df1=df1[COL_Filt2]


#df1=pd.DataFrame(df1)
#fig2 = plt.subplots()
filter_dataframe(df)


    

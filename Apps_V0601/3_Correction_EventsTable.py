# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 14:52:09 2024

@author: a863900
"""
import pandas as pd
import streamlit as st
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
#import streamlit_modal


def Update():
    st.session_state["Global_Tags"]=df_corrected.copy()
    st.session_state["df"]=df_corrected.copy()
    st.session_state["df1"]=df_corrected.copy()
    #df=st.session_state["Global_Tags"].copy()
   
def main():
    #global grid_table
    global df_corrected
    
    
    df=st.session_state["Global_Tags"]

    if "df" not in st.session_state:
        st.session_state["df"] = df


    df1=df

    if "df1" not in st.session_state:
        st.session_state["df1"] = df
    

    try:
        df1.index = df.index.strftime('%Y-%m-%d %H:%M:%S')
    except:
        pass
    
    df_corrected=st.data_editor(
        st.session_state["df1"],
        key="df_editor",
        num_rows="dynamic" 
    )
    
    st.sidebar.button("Update", on_click=Update)

    


if __name__ == "__main__":
    main()   
 

 
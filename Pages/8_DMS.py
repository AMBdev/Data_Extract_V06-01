# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 16:41:00 2023

@author: a863900
"""
#import sys
import os
import folium
import streamlit as st
import seaborn as sns
from sklearn.ensemble import IsolationForest
from scipy.stats import *
from scipy.spatial.distance import cdist
from streamlit_folium import st_folium
import plotly.express as px
import pandas as pd
from datetime import datetime
from time import strftime
from humanfriendly import format_timespan

#from streamlit.scriptrunner import get_script_run_ctx as get_report_ctx
#from streamlit.scriptrunner.script_run_context import get_script_run_ctx
#import streamlit.report_thread as ReportThread
#from streamlit import ReportThread
#from streamlit.report_thread import get_report_ctx

st.header("Pertinence des alertes")
st.title("Fonction DMS")


df=st.session_state["Param_Gen"]
Global_Tags=st.session_state["Global_Tags"]
Global_Tags1=Global_Tags[Global_Tags['TAG_Type']=='Default-DDAW-SAFETY_COACH']
Global_Tags1
Param=['LATITUDE_GPS','LONGITUDE_GPS','IVehicleSpeed','IACC_Status','V_x_LCA_ActivationStateForLSS','ILKA_ActivationState']#,'ILKA_StatusDisplay_v2'
Param_red=['LATITUDE_GPS','LONGITUDE_GPS','IVehicleSpeed']

try:
    df1=df[Param]
except:
    try:
        df1=df[Param_red]
    except:
        pass
        
df1=df1.resample('1s').first()

try:

    map_dict = {0: "LCA_Off", 1: "Autosteer_Active", 2: "LCA_Active", 3: "Temporary_Cancel", 4: "Cancel", 5: "Safe_State",
                6: "LCA_Desactivated_by_HOD"}
    df1['V_x_LCA_ActivationStateForLSS'] = df1['V_x_LCA_ActivationStateForLSS'].map(map_dict)
except:
    pass



for idx in df1:
    df1['Distance']=(df1['IVehicleSpeed']+df1['IVehicleSpeed'].shift(1))/2/3.6
    Total_dist=df1['Distance'].sum()

dist="%3.1f %s" %(Total_dist / 1000, 'Km')
Total_Parcours=dist
st.write('Total Parcours: ',Total_Parcours)




def dist_unit(dist):  
            
        
        if dist < 1000:
           dist= "%3.1f %s" %(dist, 'm')
                   
        else:
            
            dist="%3.1f %s" %(dist / 1000, 'Km')  
        
                   
        lsdist.append(dist)



#df1
try:
    ###########################Trait données ACC ################################
    ACC_Dist=df1.groupby('IACC_Status', group_keys=True)[['Distance']].sum()
    ACC_Dist['Distance']=ACC_Dist['Distance'].astype(int)
    ACC_Dist['Distance']=pd.to_numeric(ACC_Dist['Distance'])
    
    ##############################################################################
    #Affichage unité distance ACC
    ##############################################################################
    
    lsdist=[]
    T_ACC=[]
    
    
    
    for dist in ACC_Dist['Distance'] :
       
       dist_unit(dist)
    
    
    ACC_Dist['Distance']=lsdist
    #ACC_Dist
    
    grp_ACC=df1.groupby('IACC_Status', group_keys=True).groups
    
    
    for grp in grp_ACC:
               
        L=len(grp_ACC[grp])
        L=format_timespan(L,'hh:mm:ss')
        #T_grp= len(grp)
        T_ACC.append(L)
    
    
    ACC_Dist['Duration']=T_ACC
    
    st.write("Caractérisation usage ACC:")
    ACC_Dist
    
    
except:
    
    st.write("Pas de données CAN ACC")
    

try:
####################################Trait données LCA ###################################
    LC_dist=df1.groupby('V_x_LCA_ActivationStateForLSS', group_keys=True)[['Distance']].sum()
    LC_dist['Distance']=LC_dist['Distance'].astype(int)
    LC_dist['Distance']=pd.to_numeric(LC_dist['Distance'])
    
    #LC_dist
    lsdist=[]
    T_LCA=[]
    
    
    for dist in LC_dist['Distance'] :
       
       dist_unit(dist)
    
    
    LC_dist['Distance']=lsdist
    #ACC_Dist
    
    grp_LCA=df1.groupby('V_x_LCA_ActivationStateForLSS', group_keys=True).groups
    
    
    for grp in grp_LCA:
               
        L=len(grp_LCA[grp])
        L=format_timespan(L,'hh:mm:ss')
        #T_grp= len(grp)
        T_LCA.append(L)
    
    
    LC_dist['Duration']=T_LCA
    
    st.write("Caractérisation usage LC:")
     
    
    LC_dist

except:
    
    st.write("Pas de données CAN LC")
    
    





try:
    ############Trait données LKA ###########################################################
    
    LKA_dist=df1.groupby('ILKA_ActivationState', group_keys=True)[['Distance']].sum()
    
    lsdist=[]
    
    for dist in LKA_dist['Distance'] :
       
       dist_unit(dist)
    
    LKA_dist['Distance']=lsdist
    st.write("Caractérisation usage LKA:")    
    LKA_dist

except:
    
    st.write("Pas de données CAN LKA")
    


#Acc_stat = df1['IACC_Status'].unique()
#Acc_stat_dict={i: Acc_stat[i] for i in range(len(Acc_stat))}


#list_colors = ["#00FF00","#12FF00","#24FF00","#35FF00","#47FF00","#58FF00","#6AFF00","#7CFF00",
    #"#8DFF00","#9FFF00","#B0FF00","#C2FF00","#D4FF00","#E5FF00","#F7FF00","#FFF600","#FFE400","#FFD300",
    #"#FFC100","#FFAF00","#FF9E00","#FF8C00","#FF7B00","#FF6900","#FF5700","#FF4600","#FF3400","#FF2300","#FF1100","#FF0000"]
#color_dict = {i: list_colors[i] for i in range(len(list_colors))}


#df1['group'] = df1['IACC_Status'].ne(df1['IACC_Status'].shift())
#df1=df1.groupby('group')


#s = df1.IACC_Status.ne(df1.IACC_Status..ngroups
#result = [ y for _ , y in df.groupby(s)]
#result
#test1[0].shift()

#test1#for grp1 in grp_ACCreg:
    #tcr1=pDataFrame(grp1[1])
    #tcr1

#m = df['Val1'].shift() > df['Val1']

  

Trace1=[]
ParamLoc=['LATITUDE_GPS','LONGITUDE_GPS']

Trajet1=df1[ParamLoc]


#l=len(Trajet)
#l
#Trajet=Trajet[500:520]
#Trajet1=Trajet.resample('1s').first()
#Trajet1.index=pd.DatetimeIndex(Trajet1.index)
#Trajet1
#Trajet
#for col in Trajet.columns:
    #Trajet1[col]=Trajet1[col].interpolate(limit_direction='both')
#Trajet1
#Trajet=Trajet.loc[Trajet['LONGITUDE_GPS'].shift(1)-Trajet['LONGITUDE_GPS'] >0.01]:
    #Trajet['LONGITUDE_GPS'].shift(1)==np.nan
    #Trajet1=Trajet.loc[Trajet['LONGITUDE_GPS'].shift() != Trajet['LONGITUDE_GPS']]
#Trajet1
#plot.figure(figsize=(12,6))#(data=Trajet1,x='LONGITUDE_GPS')
cont1=st.expander("Qualité trace initiale", expanded=False)
with cont1:
    col1,col2=st.columns(2)
    data=Trajet1
#df = px.data.tips()
#df
    with col1:
        fig = px.box(data['LATITUDE_GPS'])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig2 = px.box(data['LONGITUDE_GPS'])
        st.plotly_chart(fig2, use_container_width=True)
    
    

#st.plotly_chart(fig, use_container_width=True)

#ax = sns.boxplot(data=Trajet1,x='LONGITUDE_GPS')
#st.plotly_chart(ax, use_container_width=True)


data=Trajet1#['LONGITUDE_GPS']

def DMS_Export():
    
    #Mydir=st.session_state["Mydir"] 
      
    
    #dB_HDF=dB_HDF.infer_objects().dtypes
    Folder=st.session_state["Folder"]
    Folder
    os.chdir(Folder)
    basename = os.path.basename(Folder)
    
    
    name=("DMS_"+ basename + ".h5")    
    
    
    store = pd.HDFStore(name)
    store['Total_Parcours'] = Total_Parcours
    store['ACC_Dist'] = ACC_Dist
    store['LC_dist'] = LC_dist    
    store['LKA_dist'] = LKA_dist
    store.close()











def Trace_LC():
    
    dict_color={'Cancel':'red','LCA_Active':'mediumtgreen','LCA_Off':'black','Safe_State':'gray','Temporary_Cancel':'ligtgray'}

    Traj3['group'] = Traj3['V_x_LCA_ActivationStateForLSS'].ne(Traj3['V_x_LCA_ActivationStateForLSS'].shift())
    filter=Traj3['group']==True
    #df1
    tcr2=Traj3.loc[filter]
    #tcr2
    
    idx=pd.DataFrame(tcr2.index)
    stat=tcr2['V_x_LCA_ActivationStateForLSS'].values
    idx['V_x_LCA_ActivationStateForLSS']=stat
    #idx
    for i in range(0,len(idx)-1):
        name=idx['V_x_LCA_ActivationStateForLSS'].iloc[i]
        #name
        t_start=idx[0].iloc[i]
        #'t_start: ',t_start
        t_end=idx[0].iloc[i+1]
        #'t_end: ',t_end
        filter=(Traj3.index>=t_start) & (Traj3.index<t_end)
        tcr3=Traj3.loc[filter]
        
        try:
            routeLC = folium.plugins.PolyLineOffset(tcr3[ParamLoc],tooltip = name,color=dict_color[(name)],offset=-1 ).add_to(fg1)
        except:
            pass

def Trace_ACC():

    
    
    dict_color={'ACC_OFF':'lightgray','ACC_driver_override':'red','ACC_in_stop':'gray','ACC_regulation':'green','ACC_suspended':'orange','ACC_waiting':'lightgreen'}

    Traj3['group'] = Traj3['IACC_Status'].ne(Traj3['IACC_Status'].shift())
    filter=Traj3['group']==True
    #df1
    tcr2=Traj3.loc[filter]
    #tcr2
    
    idx=pd.DataFrame(tcr2.index)
    stat=tcr2['IACC_Status'].values
    idx['IACC_Status']=stat
    #idx
    for i in range(0,len(idx)-1):
        name=idx['IACC_Status'].iloc[i]
        #name
        t_start=idx[0].iloc[i]
        #'t_start: ',t_start
        t_end=idx[0].iloc[i+1]
        #'t_end: ',t_end
        filter=(Traj3.index>=t_start) & (Traj3.index<t_end)
        tcr3=Traj3.loc[filter]
        
        try:
            route = folium.plugins.PolyLineOffset(tcr3[ParamLoc],tooltip = name,color=dict_color[(name)],offset=1).add_to(fg)
        except:
            pass
    


def Epur_data1():

    Q1 = tcr1['LATITUDE_GPS'].quantile(0.25)
    Q3 = tcr1['LATITUDE_GPS'].quantile(0.75)
    IQR = Q3 - Q1    #IQR is interquartile range. 
    
    filter = (tcr1['LATITUDE_GPS'] >= Q1 - 1.5* IQR) & (tcr1['LATITUDE_GPS'] <= Q3 + 1.5 *IQR)
    Traj4=tcr1.loc[filter]
    
    ########################################################
    #Epuration des données Long
    ###############################################
    Q1 = Traj4['LONGITUDE_GPS'].quantile(0.25)
    Q3 = Traj4['LONGITUDE_GPS'].quantile(0.75)
    IQR = Q3 - Q1    #IQR is interquartile range. 
         
    filter = (Traj4['LONGITUDE_GPS'] >= Q1 - 1.5* IQR) & (Traj4['LONGITUDE_GPS'] <= Q3 + 1.5 *IQR)
    Traj5=Traj4.loc[filter]
    
    try:
           route = folium.plugins.PolyLineOffset(Traj5[ParamLoc],tooltip = "itinéraire", show=True).add_to(trip)
    except:
        pass



################################################♀
#Epuration des données Lat
###############################################

def Epur_data():
    
    global tcr1
    global Traj3

    Q1 = trc['LATITUDE_GPS'].quantile(0.25)
    Q3 = trc['LATITUDE_GPS'].quantile(0.75)
    IQR = Q3 - Q1    #IQR is interquartile range. 
    
    filter = (trc['LATITUDE_GPS'] >= Q1 - 1.5* IQR) & (trc['LATITUDE_GPS'] <= Q3 + 1.5 *IQR)
    Traj2=trc.loc[filter]
    
    ########################################################
    #Epuration des données Long
    ###############################################
    Q1 = Traj2['LONGITUDE_GPS'].quantile(0.25)
    Q3 = Traj2['LONGITUDE_GPS'].quantile(0.75)
    IQR = Q3 - Q1    #IQR is interquartile range. 
    
    filter = (Traj2['LONGITUDE_GPS'] >= Q1 - 1.5* IQR) & (Traj2['LONGITUDE_GPS'] <= Q3 + 1.5 *IQR)
    Traj3=Traj2.loc[filter]
    #Traj3
    try:
        Trace_ACC()
    except:
        pass
    
    try:
        Trace_LC()
    except:
        pass
    
    grouped1=Traj3.groupby(pd.Grouper(freq="5min"))
    #grouped1.ngroups
    
    for grp1 in grouped1:
        tcr1=pd.DataFrame(grp1[1]) 
        #tcr1
    
        Epur_data1()
        #Trace_ACC1()
    try:
           route2 = folium.PolyLine(Traj3[ParamLoc],tooltip = "itinéraire").add_to(carte2)
    except:
               pass
    #return Carte2
    
        
        
        
    
    
    
    
    
    
    





Traj0=df1[df1['LATITUDE_GPS'].notnull()]
Traj0=Traj0[Traj0['LONGITUDE_GPS'].notnull()]
#st.write('Traj0')
#Traj0
#Traj4
pt0=len(Traj0)/2
lat0=Traj0['LATITUDE_GPS'].iloc[int(pt0)]
lon0=Traj0['LONGITUDE_GPS'].iloc[int(pt0)]


Carte1 = folium.Map(location=[lat0,lon0],zoom_start = 9)
Carte1.add_child(folium.LatLngPopup())




##############################################################################################################
##########"Points sur carte
#############################################################################################################

Point_color={'FALSE-POSITIVE_Not-relevant-warning':'lightred',"FALSE-NEGATIVE_No-warning":'orange','TRUE-POSITIVE_Relevant-warning':'lightgreen',"IHM-issue":'yellow',"Others":'gray'}
#gpP=Global_Tags1.groupby(by=['Item']).groups

for grp_name, df_grp in Global_Tags1.groupby('Item'):
  feature_group = folium.FeatureGroup(grp_name)
  for row in df_grp.itertuples():
    folium.Marker(location=[row.LATITUDE_GPS,row.LONGITUDE_GPS],icon=folium.Icon(color=Point_color[(grp_name)]),popup=row.stringValueNewComment).add_to(feature_group)
  feature_group.add_to(Carte1)


##############################################################################################################
##########Tracé Carte
##############################################################################################################
trip= folium.FeatureGroup(name="Trajet_Total", show=True).add_to(Carte1)
fg = folium.FeatureGroup(name="ACC_Usage", show=False).add_to(Carte1)
fg1=folium.FeatureGroup(name="LCA_Usage", show=False).add_to(Carte1)

folium.LayerControl().add_to(Carte1)




carte2=folium.Map(location=[lat0,lon0],zoom_start =6)
carte2.add_child(folium.LatLngPopup())


Mydate= pd.to_datetime(Traj0.index, unit='s')
Mydate=Mydate.tz_localize(None)

Traj0=Traj0.set_index(Mydate, drop=True)


st.sidebar.button("Save_Result DMS",on_click=DMS_Export)      






def main():
    
    global trc
    global tcr1
    global i
    global Traj3
    
    
    
    
    Traj3=pd.DataFrame()
    
    grouped=Traj0.groupby(pd.Grouper(freq="d"))
    #grouped.ngroups
    for grp in grouped:
        
        trc=pd.DataFrame(grp[1])
        #tcr1=pd.DataFrame()
        #trc
        
        Epur_data()
        
        
        
        
        
        
            
                
               
    return Carte1
    

    
       

if __name__ == "__main__":
    main()

st_folium(Carte1, width=600)
#Trace initiale##############
#st_folium(carte2, width=725)
##############################
       

#Iso_Forest=IsolationForest(contamination=0.2,random_state=40)
#outliers_labels=Iso_Forest.fit_predict(data)
#data['Outliers']=outliers_labels
#outliers=data[data['Outliers']==-1]
#goodPoints = data[data['Outliers']==1]
#outliers
#Trajet2=Trajet1[~Trajet1.isin(outliers)].dropna()
#Trace=Trajet2[['LATITUDE_GPS','LONGITUDE_GPS']]
#Trace1=goodPoints[['LATITUDE_GPS','LONGITUDE_GPS']]
#Trace1=Trace1[0:100000]
#l3=len(Trajet1)
#l4=len(outliers)

#lat0=Trajet2['LATITUDE_GPS'].iloc[0]
#lon0=Trajet2['LONGITUDE_GPS'].iloc[0]
#l1=Trajet2['LONGITUDE_GPS'].idxmin()
#l2=Trajet['LATITUDE_GPS'].min
#L1=Trajet['LONGITUDE_GPS'].max
#L2=Trajet['LONGITUDE_GPS'].min
#st.write(l1)
#l2
#L1
#L2
#l3
#l4
#goodPoints

#Trace2=Trace1
#Trace2['groups'] = (Trace2.index.to_series().diff().dt.seconds > 10).cumsum()

#list_of_dfs = []
#for ct, data in Trace2.groupby('groups'):
    #list_of_dfs.append(data)

#list_of_dfs 

#♣Trace1
#Traj3






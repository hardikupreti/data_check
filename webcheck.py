import streamlit as st
import pandas as pd
import logging as lg
import requests
from datetime import *


lg.basicConfig(filename='data_check.log', format="%(asctime)s::%(levelname)s::%(lineno)d::%(message)s",
               filemode='w',force=True)

logger = lg.getLogger()

logger.setLevel(lg.INFO)

reference_file_path = r'https://raw.githubusercontent.com/hardikupreti/data_check/main/actual_reference_data.csv'
# can handle data form url or local path
# df_out = pd.DataFrame(['starting logs\n-------------------------------------------------------'])
lis = []
def checkcsvfile_voltages(dataframe):
    df_refpath = pd.read_csv(reference_file_path,encoding = 'unicode_escape',index_col=0)
    voltages = df['VDDD'].unique()
    voltage_ref = df_refpath['VDDD'].unique()
    if set(voltages)==set(voltage_ref):
        return True,voltages,voltage_ref
    else:
        return False,voltages,voltage_ref

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(sep = '\t',date_format='%Y-%m-%d %H:%M:%S').encode('utf-8')

def timefunc():
    return datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
t = timefunc()

uploaded_file = st.file_uploader("Select a CSV File",type = ['csv'])
if uploaded_file is not None:

    lis.append(f'{t}::File Uploaded Successfully!')
    df = pd.read_csv(uploaded_file,encoding='unicode_escape')

if st.button('Check Uploaded File'):
    lis.append(f'{t}::Checking data')
    result,volts,voltsref = checkcsvfile_voltages(df)
    if result:
        lis.append(f'{t}::VOLTAGE CHECK : PASSED')
        lis.append(f'{t}::the voltage values used are : {volts}')
        df_out = pd.DataFrame(lis)
        st.write(df_out)
        # df_out.to_csv('final_log.log', header=False, index=False)
        csv = convert_df(df_out)
        st.download_button(
            label="Download Result Datalog",
            data=csv,
            file_name='datalog_final.log',
            mime='text/csv',
        )

    else:
        lis.append(f'{t}::VOLTAGE CHECK: FAILED')
        lis.append(f'{t}::The voltages in the master file are : {voltsref}')
        lis.append(f'{t}::The voltages used in the given file are {volts}')
        df_out = pd.DataFrame(lis)
        st.write(df_out)
        # df_out.to_csv('final_log.log', header=False, index=False)
        csv = convert_df(df_out)
        st.download_button(
            label="Download Result Datalog",
            data=csv,
            file_name='datalog_final.log',
            mime='text/csv',
        )





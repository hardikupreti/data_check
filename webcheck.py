import streamlit as st
import pandas as pd
import logging as lg

lg.basicConfig(filename='data_check.log', format="%(asctime)s::%(levelname)s::%(lineno)d::%(message)s",
               filemode='w',force=True)

logger = lg.getLogger()

logger.setLevel(lg.INFO)

reference_file_path = r'C:\Users\upretihardik\Desktop\actual_reference_data.csv'

def checkcsvfile_voltages(dataframe):
    df_refpath = pd.read_csv(reference_file_path,encoding = 'unicode_escape')
    voltages = df['VDDD'].unique()
    voltage_ref = df_refpath['VDDD'].unique()
    if set(voltages)==set(voltage_ref):
        return True,voltages,voltage_ref
    else:
        return False,voltages,voltage_ref


uploaded_file = st.file_uploader("Select a CSV File",type = ['csv'])
if uploaded_file is not None:

    logger.info('File Uploaded Successfully!')
    df = pd.read_csv(uploaded_file,encoding='unicode_escape')

if st.button('Check Uploaded File'):
    logger.info('Checking data')
    result,volts,voltsref = checkcsvfile_voltages(df)
    if result:
        logger.info('VOLTAGE CHECK : PASSED')
        logger.info(f'the voltage values used are : {volts}')
    else:
        logger.warning('VOLTAGE CHECK: FAILED')
        logger.info(f'The voltages in the master file are : {voltsref}')
        logger.info(f'The voltages used in the given file are {volts}')



import pandas as pd
import oracledb
from tabulate import tabulate
import random
import re
import webbrowser
import warnings

warnings.filterwarnings('ignore', 'Unverified HTTPS request')
# Forecasting Models for 3 Regions
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error

# Missing Values imputations for 3 regions

from datetime import datetime, timedelta

#SCRE
username = 'svcGOCUI'
password = 'DELL2023support#'
host = 'gocplorlvpr18.amer.dell.com'
port = '1521'
service_name = 'gooap_rw_oud_tls.prd.amer.dell.com'


def Retrive_VectorData(region):
    if region == "ALL":
        region = ('APJ','DAO','EMEA')
    else:
        region = f"('{region}')"
    

    excel_name="Input_Order_Incoming_Data.xlsx"
    dsn = oracledb.makedsn(host, port, service_name=service_name)
    try :
        
        connection = oracledb.connect(user=username, password=password, dsn=dsn)   
        print("Connected to Oracle Database")
        cursor = connection.cursor()
        # query = '''SELECT t.owner || '.' || t.table_name AS Table_Name,c.column_name as Column_Name FROM all_tables t 
        # JOIN all_tab_columns c ON t.table_name = c.table_name  ORDER BY t.table_name, c.column_name'''
 
        query = f'''select a.region, to_char(a.processdate_utc,'yyyymmdd') processday,to_char(a.processdate_utc,'hh24') as processday_hour,
a.order_count,b.fiscalyear,b.fiscalquarter,b.fiscalmonth,b.fiscalweek,to_char(a.processdate_utc,'Day') as DayNum
  from work.tb_orderprocess_effectiveness a,work.tb_fiscalcalendar b
where to_char(a.processdate_utc,'yyyymmdd') between b.startdate and b.enddate
   and a.functionname = 'Order Incoming'
   and datatype = 'NEW'
   and vendor = 'ALL'
   AND REGION in {region}
order by a.processdate_utc asc'''
    

        cursor.execute(query)
 
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        data = pd.DataFrame(rows,columns=column_names)

        return data
    except Exception as e:
       print(f"An error occurred: {e}")
    finally:
        if connection:
            connection.close()
            print("Connection closed")



# region = 'apj'
# region = region.upper()
# data = Retrive_VectorData(region)

def Process_Dates(data,region):
    # Convert PROCESSDAY to proper date format
    data["PROCESSDAY"] = pd.to_datetime(data["PROCESSDAY"], format="%Y%m%d")
    
    data["PROCESSDAY_HOUR"] = data["PROCESSDAY_HOUR"].astype(int)
    # Create a new column combining PROCESSDAY and PROCESSDAY_HOUR
    data["DateTime"] = data["PROCESSDAY"] + pd.to_timedelta(data["PROCESSDAY_HOUR"], unit="h")

    # Drop the index column
    #data = data.reset_index(drop=True)

    #df= data.drop(columns=['PROCESSDAY', 'PROCESSDAY'])
    df=data

    # Separate dataframes for each region

    df = df[df["REGION"] == region]

    # Assuming df is your original DataFrame with all regions
    df = df[df["REGION"] == region]
    return df

# Define a function for imputation
def perform_imputation(df):
    try:
        # Convert DateTime column to datetime format
        df["DateTime"] = pd.to_datetime(df["DateTime"])
        
        # Generate 1-hour intervals
        start_date = df["DateTime"].min()
        end_date = df["DateTime"].max()
        hour_intervals = pd.date_range(start=start_date, end=end_date, freq="H")

        # Create a new DataFrame with intervals
        interval_df = pd.DataFrame({"DateTime": hour_intervals})

        # Merge interval_df with original data
        merged_df = pd.merge(interval_df, df, on="DateTime", how="left")

        # Fill missing data based on available data
        merged_df["REGION"].fillna(method="ffill", inplace=True)
        merged_df["FISCALYEAR"].fillna(method="ffill", inplace=True)
        merged_df["FISCALQUARTER"].fillna(method="ffill", inplace=True)
        merged_df["FISCALMONTH"].fillna(method="ffill", inplace=True)
        merged_df["FISCALWEEK"].fillna(method="ffill", inplace=True)
        merged_df["DAYNUM"].fillna(method="ffill", inplace=True)

        # Perform imputation for ORDER_COUNT using DAYNUM
        daynum_order_count_avg = merged_df.groupby("DAYNUM")["ORDER_COUNT"].mean()
        merged_df["ORDER_COUNT"].fillna(merged_df["DAYNUM"].map(daynum_order_count_avg), inplace=True)

        # Fill remaining columns based on data & time columns
        merged_df["PROCESSDAY_HOUR"].fillna(merged_df["DateTime"].dt.hour, inplace=True)

        
        return merged_df
    except Exception as e:
       print(f"An error occurred: {e}")


# Define a function to select specific columns from a DataFrame
def select_columns(df, columns):
    return df[columns].reset_index(drop=True)


# # Define the columns to select
# selected_columns = ["DateTime", "ORDER_COUNT"]

# # Assuming emea_df, dao_df, and apj_df are your DataFrames for the EMEA, DAO, and APJ regions respectively
# # Apply the function to each DataFrame
# data_df = select_columns(imputed_df, selected_columns)

def process_region_DT(X_train,y_train,X_test,y_test,region_name,future_df):
    # Decision Tree Regressor
    dt_model = DecisionTreeRegressor(random_state=42)
    dt_model.fit(X_train, y_train)
    dt_predictions = dt_model.predict(X_test)
    dt_mse = mean_squared_error(y_test, dt_predictions)
    # print(f'{region_name} - Decision Tree MSE: {dt_mse}')

    # Combine actual and forecasted values into DataFrames for comparison
    actual_vs_forecasted_dt = pd.DataFrame({'Actual': y_test, 'Forecasted_DT': dt_predictions})

    # Predict the next 100 future values using each model
    future_predictions_dt = dt_model.predict(future_df)

    return actual_vs_forecasted_dt,future_predictions_dt;

def process_region_RF(X_train,y_train,X_test,y_test,region_name,future_df):
    # Random Forest Regressor
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_predictions = rf_model.predict(X_test)
    rf_mse = mean_squared_error(y_test, rf_predictions)
    # print(f'{region_name} - Random Forest MSE: {rf_mse}')

    # Combine actual and forecasted values into DataFrames for comparison
    actual_vs_forecasted_rf = pd.DataFrame({'Actual': y_test, 'Forecasted_RF': rf_predictions})

    # Predict the next 100 future values using each model
    # future_predictions_dt = dt_model.predict(future_df)
    future_predictions_rf = rf_model.predict(future_df)
    return actual_vs_forecasted_rf,future_predictions_rf

def process_region_GBM(X_train,y_train,X_test,y_test,region_name,future_df):
    # Gradient Boosting Regressor
    gbm_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    gbm_model.fit(X_train, y_train)
    gbm_predictions = gbm_model.predict(X_test)
    gbm_mse = mean_squared_error(y_test, gbm_predictions)
    # print(f'{region_name} - GBM MSE: {gbm_mse}')

    # Combine actual and forecasted values into DataFrames for comparison
    
    actual_vs_forecasted_gbm = pd.DataFrame({'Actual': y_test, 'Forecasted_GBM': gbm_predictions})

    # Predict the next 100 future values using each model
    future_predictions_gbm = gbm_model.predict(future_df)

    return actual_vs_forecasted_gbm,future_predictions_gbm

def process_region_SVM(X_train,y_train,X_test,y_test,region_name,future_df):
    # Support Vector Machine Regressor
    svm_model = SVR(kernel='rbf')
    svm_model.fit(X_train, y_train)
    svm_predictions = svm_model.predict(X_test)
    svm_mse = mean_squared_error(y_test, svm_predictions)
    # print(f'{region_name} - SVM MSE: {svm_mse}')

    # Combine actual and forecasted values into DataFrames for comparison

    actual_vs_forecasted_svm = pd.DataFrame({'Actual': y_test, 'Forecasted_SVM': svm_predictions})

    # Predict the next 100 future values using each model
    # future_predictions_dt = dt_model.predict(future_df)
    # future_predictions_rf = rf_model.predict(future_df)
    # future_predictions_gbm = gbm_model.predict(future_df)
    future_predictions_svm = svm_model.predict(future_df)

    return actual_vs_forecasted_svm, future_predictions_svm

def process_region(data, region_name,model_name,noOfSamples):
    try:
        # Feature engineering for seasonality
        data['hour'] = data.index.hour
        data['dayofweek'] = data.index.dayofweek
        data['month'] = data.index.month

        # Prepare features and target with seasonality
        X = data[['hour', 'dayofweek', 'month']]  # Add more features as needed
        y = data['ORDER_COUNT']

        # Split the data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    
        # Extend the datetime index for the next 100 future values with 1-hour interval
        last_timestamp = data.index[-1]
        # future_dates = pd.date_range(start=last_timestamp, periods=167, freq='H')[1:]
        future_dates = pd.date_range(start=last_timestamp, periods=noOfSamples, freq='H')[1:]
        # Create a DataFrame for future dates and engineer seasonality features
        future_df = pd.DataFrame(index=future_dates)
        future_df['hour'] = future_df.index.hour
        future_df['dayofweek'] = future_df.index.dayofweek
        future_df['month'] = future_df.index.month

        future_predictions_df = pd.DataFrame({
            'DateTime': future_dates
        })
        
        # Set the DateTime as the index
        future_predictions_df.set_index('DateTime', inplace=True)
        all_dfs = {}
        # Create a DataFrame for the future predictions
        for model in model_name:
            name = 'Forecasted_'+ model
            method_name  = 'process_region_' + model
            method = globals()[method_name]

            actual_vs_forecasted, future_predictions = method(X_train,y_train,X_test,y_test,region_name,future_df)
            future_predictions_df[name] = future_predictions
            # Append the actual_vs_forecasted DataFrame to the dictionary with the model name as the key
            all_dfs[name] = actual_vs_forecasted
            
        combined_results_df = pd.DataFrame()

        # for i, (model, df) in enumerate(all_dfs.items()):
        #     if i == 0:
        #         combined_results_df = pd.concat([combined_results_df, df], axis=1)
        #     else:
        #         combined_results_df = pd.concat([combined_results_df, df[[model]]], axis=1)

        # combined_results_df = pd.concat([combined_results_df, future_predictions_df], axis=1)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        # print(future_predictions_df)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

        return future_predictions_df
    except Exception as e:
       print(f"An error occurred: {e}")

def OIF_Individual(data,region,model_name,noOfSamples):
    df = Process_Dates(data=data,region=region)
    imputed_df = perform_imputation(df=df)

    # print(f"Imputed data for {region} saved")

    selected_columns = ["DateTime", "ORDER_COUNT"]
    data_df = select_columns(imputed_df, selected_columns)

    # Load your datasets
    data_df = pd.DataFrame(data_df)
    data_df['DateTime'] = pd.to_datetime(data_df['DateTime'])
    data_df.set_index('DateTime', inplace=True)

    final = process_region(data_df, region,model_name=model_name,noOfSamples=noOfSamples)
    return final


def OIF(region,model_name,noOfSamples):
   
    region = region.upper()
    model_name = model_name.upper()
    if model_name == 'ALL':
        model_name = ['DT','RF','GBM','SVM']
    elif model_name == 'DECISIONTREE': 
        model_name = ['DT']
    elif model_name == 'RANDOMFOREST': 
        model_name = ['RF']
    elif model_name == 'GBM':
        model_name = ['GBM']
    elif model_name == 'SVM':
        model_name = ['SVM']
   
    data = Retrive_VectorData(region)

    if region == "ALL":
        regions = ['DAO', 'EMEA', 'APJ']
        
        DF_ALL =[]
        for reg in regions:
            df = OIF_Individual(data=data,region=reg,model_name=model_name,noOfSamples=noOfSamples)
            DF_ALL.append(df)

        return DF_ALL
    else:
        return OIF_Individual(data=data,region=region,model_name=model_name,noOfSamples=noOfSamples)
        

    
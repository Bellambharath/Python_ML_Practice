import pandas as pd
import cx_Oracle
from tabulate import tabulate
import json
import requests
import os
from transformers import pipeline, Conversation
import re
import webbrowser
import xml.etree.ElementTree as ET
from lxml import etree
from bs4 import BeautifulSoup



# GE2-CIS database connection details
username = 'MWMGR'
password = 'Saynotoclown$$$1'
dsn = cx_Oracle.makedsn('ausul2trsdb02.us.dell.com', '1521', service_name='wwg2s.sit.amer.dell.com')

#GE2-GTM database connection details
username1 = 'glogowner'
password1 = 'glogowner_12345'
dsn1 = cx_Oracle.makedsn('gtmnlorrsitdb02.us.dell.com', '1521', service_name='gtm2s.sit.amer.dell.com')

def connect_to_GE2CIS():
    try:
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
        print("Connected to GE2-CIS Database")
        return connection
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Oracle error code: {error.code}")
        print(f"Oracle error message: {error.message}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
def connect_to_GE2GTM():
    try:
        connection = cx_Oracle.connect(user=username1, password=password1, dsn=dsn1)
        print("Connected to GE2-GTM Database")
        return connection
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Oracle error code: {error.code}")
        print(f"Oracle error message: {error.message}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None




#running query 
def execute_query(connection, query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        if rows:
            table = tabulate(rows, headers=column_names, tablefmt="pretty")
            print(table)
        else:
            print("No results found.")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Oracle error code: {error.code}")
        print(f"Oracle error message: {error.message}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()

def get_order_details(connection, order_number):
    query = """
    SELECT * FROM ORDER_INFO WHERE order_number = :order_number
    """
    try:
        cursor = connection.cursor()
        cursor.execute(query, {'order_number': order_number})
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        
        if rows:
            order_details = []
            for row in rows:
                order_detail = {column_names[i]: row[i] for i in range(len(column_names))}
                order_details.append(order_detail)
            
            for detail in order_details:
                for key, value in detail.items():
                    print(f"{key}: {value}")
                print("\n---\n")
        else:
            print("No results found.")
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        print(f"Oracle error code: {error.code}")
        print(f"Oracle error message: {error.message}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()

def OMS_order_Screening(connection, business_lookup_key):
    query = """
    SELECT MESSAGE_TYPE FROM transaction_log WHERE business_lookup_key = :business_lookup_key
    """
    cursor = connection.cursor()
    cursor.execute(query, {'business_lookup_key': business_lookup_key})
    # Initialize a list to store rows that meet the condition
    matching_rows = []
    # Fetch the result
    result = cursor.fetchall()
    result_str =""
    # Check if the result is not None
    if result:
        for row in result :
            res = row[0]  # Assuming the result is a single column
            # Use the result in an if-else condition
            if res == 'OMS_INBOUND':
                result_str=res
                print(result_str)
                matching_rows.append(result_str)
                
        print(matching_rows)
        # Process the matching rows if any
        if matching_rows:
            print(result_str)
            for match in matching_rows:
                print('Your order is in Trade')

                for rows in result :
                    res = rows[0]
                    if res == 'CIS_OUTBOUND_OMEGA' :
                        query1 = "SELECT original_msg FROM transaction_log  WHERE message_type = '"+res+"' AND business_lookup_key = '"+business_lookup_key+"'"
                        #print(query1)
                        data = pd.read_sql_query(query1, connection)
                        #print(data)
                        for col in data.select_dtypes(include=['object']).columns:
                            data[col] = data[col].apply(lambda x: x.read() if hasattr(x, 'read') else x)
                        retrieving_data(data)
                   
        else:
            print('Order not reach trade yet')

    
def retrieving_data(data):
    xml_str=data['ORIGINAL_MSG'][0]
    xml_str = xml_str.strip()
    #print(xml_str)
    tag='result'       
    bs = BeautifulSoup(xml_str, 'xml')
    res = bs.find(tag)
    if res:
        #print(res)
        res_content = res.get_text().strip()
        print('Status : ' + res_content)
        if res_content == 'HOLD':
            tag1 = 'ReasonCode'
            res1 = bs.find(tag1)
            reasoncode = res1.get_text().strip()
            print('Reason code : ' + reasoncode)
        #return res_content 
    else:
        print("tag not found")


def is_sql_query(user_input):
    # Basic check for common SQL keywords
    sql_keywords = ["SELECT", "INSERT", "UPDATE", "DELETE", "FROM", "WHERE", "JOIN", "CREATE", "DROP", "ALTER"]
    return any(keyword in user_input.upper().split() for keyword in sql_keywords)

def main():
    connection = connect_to_GE2CIS()
    connection1 = connect_to_GE2GTM()
    if not connection:
        return
    
    try:
        nlp = pipeline("question-answering")
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return
    
    general_context = "I am an AI chatbot designed to assist with order information and general queries."

    try:
        while True:
            user_input = input("You : ").strip()
            if user_input.lower() == 'exit':
                break

            if user_input.lower().startswith('order '):
                order_number = user_input.split()[1]
                OMS_order_Screening(connection, order_number)
                #get_order_details(connection, order_number)
            elif is_sql_query(user_input):
                execute_query(connection, user_input)
            
            else:
                context = general_context
                try:
                    result = nlp(question=user_input, context=context)
                    print(f"Bot: {result['answer']}")
                except Exception as e:
                    print(f"An error occurred while processing the question: {e}")
    finally:
        if connection:
            connection.close()
            print("Connection closed")

if __name__ == "__main__":
    main()


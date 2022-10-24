""" ******************** Pacemaker cluster monitoring status ******************** """

############################## Server Section ##############################

#!/usr/bin/python3

"""
Import libraries
"""
from termcolor import colored
from email.message import EmailMessage
from multiprocessing import Process
import matplotlib.pyplot as plt
import numpy as np
import time as tm
import mysql.connector
import logging
import socket
import smtplib
import re
import os


#-----------------------------------------------------------------------------------------
"""
establishing the connection
"""
def Connect_to_mysql():
    try:
        global cnx
        cnx = mysql.connector.connect(user = 'root', password = 'a1800', host = '127.0.0.1')
    except Exception as err:
        print("[-] I Can Not Connect To MySQL Database !! :(", str(err))  
        exit()
    else:    
        global cursor
        cursor = cnx.cursor()
        
#-----------------------------------------------------------------------------------------
"""
Create a database to store the values taken
"""
def Create_database():
    database_name = "Pacemaker"

    cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(database_name))
    cursor.execute("USE {}".format(database_name)) 

#-----------------------------------------------------------------------------------------
"""
Create a table in the database
"""
def Create_table() -> str:  
    table_name = "Status"

    sql = """CREATE TABLE IF NOT EXISTS %s (ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Date_And_Time VARCHAR(25) NOT NULL, Status INT NOT NULL);""" % (table_name)
    
    cursor.execute(sql)
    return table_name

#-----------------------------------------------------------------------------------------
"""
Insert the values into the MySQL database
"""
def Insert_values(table_name:str, date_and_time:str, int_val_message_status:int):
    cursor.execute("INSERT INTO {} (Date_And_Time, Status) VALUES (\"%s\", \"%s\")".format(table_name) 
    % (date_and_time, int_val_message_status))
    
    cnx.commit()

#-----------------------------------------------------------------------------------------
"""
Show service status graphically
"""
def Visualize_data(message_status:int, date_and_time:str):   
    Values_msg = np.array([]) 
    Values_msg = np.append(Values_msg, message_status)

    date_and_time_output   = re.findall("..:.*", date_and_time)
    final_result_date_time =  ''.join(date_and_time_output)

    Values_date_time = np.array([])
    Values_date_time = np.append(Values_date_time, final_result_date_time)

    plt.bar(Values_date_time, Values_msg, label = "Status")
    plt.title("Status Pacemaker Service")
    plt.xlabel('Date and time')
    plt.ylabel('Status')

#-----------------------------------------------------------------------------------------
"""
Send email if the service is interrupted
"""
def Send_email(date_and_time:str):
    EMAIL_HOST          = 'smtp.gmail.com'
    EMAIL_HOST_USER     = 'amirmohammadrezvaninia@gmail.com'
    EMAIL_HOST_PASSWORD = 'mbtzvraxgoamjuof'
    EMAIL_PORT_SSL      = 465

    msg = EmailMessage()
    msg['Subject'] = 'Monitoring Cluster Linux => Severity: High'
    msg['From']    = EMAIL_HOST_USER
    msg['To']      = 'amirtestone@gmail.com'
    msg.set_content('Pacemaker service is down at this time: {} '.format(date_and_time))

    with open('resolve.txt', 'r') as f:
        file_data = f.read()

    msg.add_attachment(file_data, subtype = 'txt', filename = 'resolve.txt')

    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT_SSL) as server:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(msg)

#-----------------------------------------------------------------------------------------
"""
Create a log to review events
"""
def Create_log():
    logging.basicConfig(filename = 'msg.log', filemode = 'a', 
    format = '%(asctime)s-%(filename)s-%(message)s')
    
    logging.error('Pacemaker service is down !!')

#-----------------------------------------------------------------------------------------
"""
Get values form target node
"""
def Get_values():
    for count in range(0,5,1):
        date_and_time  = target.recv(1024).decode('utf-8') 
        message_status = target.recv(1024).decode('utf-8')

        int_val_message_status = int(message_status)

        print(f">>> Date And Time: { date_and_time }")
        print(f">>> Status Service Pacemaker: { int_val_message_status }")
        
        #Execution of the function of pouring values into MySQL
        P1 = Process(target = Insert_values, args = (table_name, date_and_time, int_val_message_status,))
        P1.start()
        P1.join()
        
        #Execute function visualize data
        # P2 = Process(target = Visualize_data, args = (message_status,))
        # P2.start()
        # P2.join()

        Visualize_data(message_status, date_and_time)


        if int_val_message_status == 1:
            print(colored(f"\n[+] Service Is Up And Running :)", 'green'))
        else:
            print(colored(f"\n[-] Service Is Down :(", 'red'))

            #Execute function send mail
            # P3 = Process(target = Send_email, args = (date_and_time,))
            # P3.start()
            # P3.join()

            P4 = Process(target = Create_log)
            P4.start()
            P4.join()


        print('\n*********************************************')

#-----------------------------------------------------------------------------------------
"""
This function for listening incoming connections and established connections created
"""
def Server():
    #Variables used in established connections
    global s
    global ip
    global target

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("192.168.60.1", 54321))
        s.listen(5)
        print(colored("[+] Listening For Incoming Connections", 'green'))

        target, ip = s.accept()
        print(colored("[+] Connection Established From: %s" % str(ip), 'blue'))

    except Exception as err:
        print("[-] I Can Not Listening For Incoming Connections !! :(", str(err))  
        exit()

#-----------------------------------------------------------------------------------------

Connect_to_mysql()
Create_database()
table_name = Create_table()


Server()
Get_values()

cnx.close()

plt.show()


s.close()










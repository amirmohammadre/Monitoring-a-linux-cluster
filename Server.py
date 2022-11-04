""" ******************** Pacemaker cluster monitoring status ******************** """

############################## Server Section ##############################

#!/usr/bin/python3

"""
Import libraries
"""
from turtle import color
from termcolor import colored
from email.message import EmailMessage
from multiprocessing import Process
import matplotlib.pyplot as plt
import numpy as np
import time as tm
import mysql.connector
import customtkinter
import threading
import tkinter
import logging
import socket
import smtplib
import re
import os

#-----------------------------------------------------------------------------------------


#Change plot size in Matplotlib
plt.rcParams['figure.figsize'] = (12, 7)

#-----------------------------------------------------------------------------------------


customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")  

app = customtkinter.CTk()  
app.geometry("1000x600")
app.title("Monitoring Status Pacemaker Service")
app.resizable(False, False)


label_frame = customtkinter.CTkFrame(master = app, 
                                    border_width = 0.5, border_color = '#FFFFFF',
                                    width= 900)

label_frame.pack(pady=30)

#-----------------------------------------------------------------------------------------


def button_event():

    inputValue_ip     = entry_ip.get()
    inputValue_port   = entry_port.get()
    

    int_val_port      = int(inputValue_port) 


    Connect_to_mysql()

    Create_database()

    table_name = Create_table()


    # Pro_Server = Process(target = Server, args = (inputValue_ip, int_val_port, ))
    # Pro_Get_val = Process(target = Get_values, args = (table_name, ))
    
    
    # Pro_Server.start()
    # Pro_Get_val.start()


    # Pro_Server.join()
    # Pro_Get_val.join()

    # threading.Thread(target = Server, args = (inputValue_ip, int_val_port,)).start()
    # threading.Thread(target = Get_values, args = (table_name,)).start()
    

    log.insert(tkinter.END, " [*] Starting ... \n")    


    Server(inputValue_ip, int_val_port, table_name)





    plt.show()


    s.close()
    
  
                
    # Get_values(table_name)


    # cnx.close()

    # plt.show()


    # s.close()
    
    # log.insert(tkinter.END, "\n Ending ...")    


#-----------------------------------------------------------------------------------------

entry_ip = customtkinter.CTkEntry(master= label_frame, 
                              width = 400, 
                              height = 40, 
                              placeholder_text="IP Address",
                              border_width = 1, text_color = "silver")
entry_ip.grid(row = 0, column = 0, padx =10, pady =10)


entry_port = customtkinter.CTkEntry(master= label_frame, 
                              width = 400, 
                              height = 40, 
                              placeholder_text="Port",
                              border_width = 1, text_color = "silver")
entry_port.grid(row = 1, column = 0, padx =10, pady = 10)


button = customtkinter.CTkButton(app,
                                corner_radius = 30,
                                height = 50,
                                hover_color = "#5837D0",
                                text_font=('Tahoma', 12),
                                text="Run Monitoring", command=button_event)

button.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)


#-----------------------------------------------------------------------------------------


text_frame = customtkinter.CTkFrame(master = app)
text_frame.pack(pady = 40)

 
log = customtkinter.CTkTextbox(text_frame)
log.grid(row = 0, column = 0)
log.configure(width = 850, height = 340, border_width = 1, border_color = '#808080')  



#-----------------------------------------------------------------------------------------
"""
establishing the connection with MySQL Database
"""
def Connect_to_mysql():

    try:
   
        global cnx
        cnx = mysql.connector.connect(user = 'root', password = 'a1800', host = '127.0.0.1')
   
    except Exception as err:
        log.insert(tkinter.END, "\n [-] I Can Not Connect To MySQL Database !! :(", str(err))  
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
def Visualize_data(int_val_message_status:int, date_and_time:str):   

    Values_msg = np.array([]) 
    Values_msg = np.append(Values_msg, int_val_message_status)


    date_and_time_output   = re.findall("..:.*", date_and_time)
    final_result_date_time =  ''.join(date_and_time_output)


    Values_date_time = np.array([])
    Values_date_time = np.append(Values_date_time, final_result_date_time)


    plt.bar(Values_date_time, Values_msg, label = "Status")
    plt.scatter(Values_date_time, Values_msg)


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


    with open('help.png', 'rb') as f:
        file_data = f.read()


    msg.add_attachment(file_data, maintype = 'image', subtype = 'png', filename = 'help.png')


    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT_SSL) as server:
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        server.send_message(msg)

#-----------------------------------------------------------------------------------------
"""
Create a log to review events
"""
def Create_log(date_and_time:str):
 
    logging.basicConfig(filename = 'msg.log', filemode = 'a', 
    format = '%(filename)s-%(message)s')
    
    logging.error(f' {date_and_time} [-] Pacemaker service is down !! ')

#-----------------------------------------------------------------------------------------
"""
Get values form target node
"""
def Get_values(table_name:str, target:str):

    def mainloop():    

        while True:

            num = 0

            for count in range(0,10,1):

                date_and_time  = target.recv(1024).decode('utf-8').strip() 
                message_status = target.recv(1024).decode('utf-8').strip()
                
                
                #Change the message_status variable from string to integer
                int_val_message_status = int(message_status)

                
                log.insert(tkinter.END, f"\n >>> Date And Time: { date_and_time }")
                log.insert(tkinter.END, f"\n >>> Status Service Pacemaker: { int_val_message_status }")

                
                #Execution of the function of pouring values into MySQL
                # P1 = Process(target = Insert_values, args = (table_name, date_and_time, int_val_message_status,))
                # P1.start()
                # P1.join()
                
                threading.Thread(target = Insert_values, args = (table_name, date_and_time, int_val_message_status, )).start()


                #Execute function visualize data
                # P2 = Process(target = Visualize_data, args = (message_status,))
                # P2.start()
                # P2.join()

                threading.Thread(target = Visualize_data, args = (int_val_message_status, date_and_time, )).start()
                

                # Visualize_data(int_val_message_status, date_and_time)


                if int_val_message_status == 1:
                
                    log.insert(tkinter.END, f"\n [+] Service Is Up And Running :)")
                
                else:

                    log.insert(tkinter.END, f"\n [-] Service Is Down :(")


                    #Execute function send mail
                    threading.Thread(target = Send_email, args = (date_and_time, )).start()
                    
                    
                    #Execute log creation function
                    threading.Thread(target = Create_log, args = (date_and_time, )).start()




                    #Execute function send mail
                    # P_send_mail = Process(target = Send_email, args = (date_and_time,))

                    #Execute log creation function
                    # P_create_log = Process(target = Create_log, args = (date_and_time,))

                    # P_send_mail.start()
                    # P_create_log.start()

                    # P_send_mail.join()
                    # P_create_log.join()


                log.insert(tkinter.END, '\n *****************************************************************')
                
                num += 1

            
            if num == 10:
                break
            

            cnx.close()
            
            log.insert(tkinter.END, "\nEnding ...")    




                 
    threading.Thread(target = mainloop).start()
    

    

#-----------------------------------------------------------------------------------------
"""
This function for listening incoming connections and established connections created
"""
def Server(inputValue_ip:str, int_val_port:int, table_name:str):
    

    #Variables used in established connections
    global s
    global ip
    global target


    try:
        def mainloop():     

            while True:   
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((inputValue_ip, int_val_port))
                s.listen(5)


                log.insert(tkinter.END, "\n [+] Listening For Incoming Connections")
            

                target, ip = s.accept()
                log.insert(tkinter.END, "\n [+] Connection Established From: %s" % str(ip))
                log.insert(tkinter.END, '\n -----------------------------------------------------------------------------------------------')
                
                threading.Thread(target = Get_values, args = (table_name, target,)).start()

                


        threading.Thread(target = mainloop).start()



    except Exception as err:
    
        log.insert(tkinter.END, "[-] I Can Not Listening For Incoming Connections !! :( %s" % str(err))  
        exit()

#-----------------------------------------------------------------------------------------




app.mainloop()











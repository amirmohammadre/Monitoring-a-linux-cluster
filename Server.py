""" ******************** Pacemaker cluster monitoring status ******************** """

############################## Server Section ##############################

#!/usr/bin/python3

"""
Import libraries
"""
from termcolor import colored
from email.message import EmailMessage
from multiprocessing import Process
from pylab import plot, show, xlabel, ylabel
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
app.geometry("1000x690")
app.title("Monitoring Application")
app.resizable(False, False)


#-----------------------------------------------------------------------------------------
"""
Program title section and theme color change
"""

frame_title = customtkinter.CTkFrame(master = app, 
                                    border_width = 1, border_color = '#FFFFFF',
                                    width= 800, height = 40)

frame_title.pack(pady = 8)


lb_title = customtkinter.CTkLabel(master = frame_title, text="Monitoring Status Pacemaker Service", 
                                text_font = ('Tahoma', 17))
lb_title.place(relx=0.5, rely=0.5, anchor = tkinter.CENTER)


frame_themes = customtkinter.CTkFrame(master = app, 
                                    border_width = 0.5, border_color = '#FFFFFF',
                                    height = 20)

frame_themes.pack(pady = 5)


lb_themes = customtkinter.CTkLabel(master = frame_themes, text="Color Themes : ", 
                                text_font = ('Tahoma', 10))
lb_themes.grid(row = 0, column = 0, padx = 10, pady = 10)


def optionmenu_callback(choice):
    customtkinter.set_appearance_mode(choice)


combobox = customtkinter.CTkOptionMenu(master = frame_themes,
                                       values = ["dark", "light"],
                                       command = optionmenu_callback)


combobox.grid(row = 0, column = 1, padx = 10, pady = 10)

combobox.set("dark")  


#-----------------------------------------------------------------------------------------
"""
Functions of the buttons
"""

def program_exit():

    app.quit()



def Display_graph():

    # saving the figure
    plt.savefig("status_graph.png")


    plt.show()



def button_event():

    inputValue_ip     = entry_ip.get()
    inputValue_port   = entry_port.get()
    

    int_val_port      = int(inputValue_port) 


    Connect_to_mysql()

    Create_database()

    table_name = Create_table()

    
    log.insert(tkinter.END, " [*] Starting ... \n")    


    #Execute Server function
    threading.Thread(target = Server, args = (inputValue_ip, int_val_port, table_name, )).start()

    
    s.close()


#-----------------------------------------------------------------------------------------
"""
section get ip address and port machine
"""

frame_ip_and_port = customtkinter.CTkFrame(master = app, 
                                    border_width = 0.5, border_color = '#FFFFFF',
                                    width= 900)

frame_ip_and_port.pack(pady=10)


entry_ip = customtkinter.CTkEntry(master = frame_ip_and_port, 
                              width = 600, 
                              height = 40, 
                              placeholder_text = "IP Address",
                              border_width = 1, text_color = "silver")
entry_ip.grid(row = 0, column = 0, padx = 10, pady = 10)


entry_port = customtkinter.CTkEntry(master = frame_ip_and_port, 
                              width = 600, 
                              height = 40, 
                              placeholder_text = "Port",
                              border_width = 1, text_color = "silver")
entry_port.grid(row = 1, column = 0, padx =10, pady = 10)


#-----------------------------------------------------------------------------------------


button_frame = customtkinter.CTkFrame(master = app)
button_frame.pack(pady = 0.01)


button_monitor = customtkinter.CTkButton(button_frame,
                                corner_radius = 30,
                                height = 50,
                                hover_color = "#5837D0",
                                text_font=('Tahoma', 12),
                                text="Run Monitoring", command = button_event)

button_monitor.grid(row = 2, column = 0, padx = 10, pady = 10)


button_graph = customtkinter.CTkButton(button_frame,
                                corner_radius = 30,
                                height = 50,
                                hover_color = "#5837D0",
                                text_font=('Tahoma', 12),
                                text="Show Graph", command = Display_graph)

button_graph.grid(row = 2, column = 1, padx = 10, pady = 10)


button_exit = customtkinter.CTkButton(button_frame,
                                corner_radius = 30,
                                height = 50,
                                hover_color = "#5837D0",
                                text_font=('Tahoma', 12),
                                text="Quit", command = program_exit)

button_exit.grid(row = 2, column = 2, padx = 10, pady = 10)


#-----------------------------------------------------------------------------------------
"""
Logs display window
"""

text_frame = customtkinter.CTkFrame(master = app)
text_frame.pack(pady = 10)

 
log = customtkinter.CTkTextbox(text_frame)
log.grid(row = 0, column = 0)
log.configure(width = 850, height = 340, border_width = 1, border_color = '#808080')  


# create CTk scrollbar
ctk_textbox_scrollbar = customtkinter.CTkScrollbar(text_frame, command=log.yview)
ctk_textbox_scrollbar.grid(row=0, column=1, sticky="ns")

ctk_textbox_scrollbar.configure(corner_radius = 20)


# connect textbox scroll event to CTk scrollbar
log.configure(yscrollcommand=ctk_textbox_scrollbar.set)


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
                threading.Thread(target = Insert_values, args = (table_name, date_and_time, int_val_message_status, )).start()


                #Execute function visualize data
                threading.Thread(target = Visualize_data, args = (int_val_message_status, date_and_time, )).start()
                

                if int_val_message_status == 1:
                
                    log.insert(tkinter.END, f"\n [+] Service Is Up And Running :)")
                
                else:

                    log.insert(tkinter.END, f"\n [-] Service Is Down :(")



                    #Execute function send mail
                    threading.Thread(target = Send_email, args = (date_and_time, )).start()
                    
                    
                    #Execute log creation function
                    threading.Thread(target = Create_log, args = (date_and_time, )).start()



                log.insert(tkinter.END, '\n *****************************************************************')
                
                num += 1

            
            if num == 10:
                break
            


            cnx.close()
            


        log.insert(tkinter.END, "\n \n [*] Done ")



      
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
                log.insert(tkinter.END, '\n -------------------------------------------------------------------------------------------------\n')
                
                threading.Thread(target = Get_values, args = (table_name, target, )).start()


        

        threading.Thread(target = mainloop).start()
        
        

    except Exception as err:
    
        log.insert(tkinter.END, "[-] I Can Not Listening For Incoming Connections !! :( %s" % str(err))  
        
        exit()

    
#-----------------------------------------------------------------------------------------









app.mainloop()













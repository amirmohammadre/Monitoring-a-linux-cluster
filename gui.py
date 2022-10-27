import customtkinter
import tkinter

customtkinter.set_appearance_mode("System")  
customtkinter.set_default_color_theme("blue")  

app = customtkinter.CTk()  
app.geometry("1000x600")
app.title("Monitoring Status Pacemaker Service")
app.resizable(False, False)

#------------------------------------------------------------------

label_frame = customtkinter.CTkFrame(master = app, 
                                    border_width = 0.5, border_color = '#FFFFFF',
                                    width= 900)

label_frame.pack(pady=30)


#------------------------------------------------------------------

def button_event():
    inputValue_ip = entry_ip.get()
    print(inputValue_ip)

    inputValue_port = entry_port.get()
    print(inputValue_port)

    log.insert(tkinter.END, "\nthis is a test")


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
                                text="Run", command=button_event)

button.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

#-------------------------------------------------------------------


text_frame = customtkinter.CTkFrame(master = app)
text_frame.pack(pady = 40)

 
log = customtkinter.CTkTextbox(text_frame)
log.grid(row = 0, column = 0)
log.configure(width = 850, height = 340, border_width = 1, border_color = '#808080')  



app.mainloop()

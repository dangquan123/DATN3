import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendacerealtime-23cfc-default-rtdb.firebaseio.com/',
    'storageBucket':'faceattendacerealtime-23cfc.appspot.com'
})

bucket = storage.bucket()

ref = db.reference(f'laplich1/thu2')
ref.child("1-2").set("nghi hoc")

def msg_box():

    fileName = entry.get()
    blobs = bucket.blob(f'file/{fileName}')
    blobs.download_to_filename("dowloadFile/" + fileName)
    print("Dowload thành công! ")
    messagebox.showinfo("tb", "Dowload thành công!")

main_window = tk.Tk()
main_window.geometry("800x600+200+100")
main_window.title("dowload file from fisebase")
main_window.config(bg='#CC9999')
def label(text, x, y):
    # tao widget lable de hien thi huong dan
    lable = tk.Label(main_window, text=text)
    lable.place(x=x, y=y)
    lable.config(font=("Arial", 10), justify="left", foreground="#009966")
def entry(width, x, y):
    entry = tk.Entry(main_window, width=35)
    entry.place(x=x, y=y)
def button(text, x, y, command):
    button = tk.Button(main_window, text=text, command=command, activebackground="black",
                            activeforeground="white",  fg="#009966",
                            font=('Helvetica bold', 15))
    button.place(x=x, y=y)

def comboboxd(choices, value_defound, x, y):

    combobox = ttk.Combobox(main_window, values=choices,foreground='#000022', background='black', width=7)
    combobox.set(value_defound)
    combobox.place(x=x, y=y)
    selected_item = combobox.get()
    return selected_item

choices = ['thu2','thu3', 'thu4', 'thu5', 'thu6', 'thu7', 'cn']
value_defound = "thu2"
value_com = comboboxd(choices, value_defound, 50, 70)

print(f"Selected item: {value_com}")

main_window.mainloop()
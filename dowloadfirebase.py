import tkinter as tk
from tkinter import messagebox
from firebase_admin import credentials
from firebase_admin import storage
import firebase_admin
# kết nối với firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendacerealtime-23cfc-default-rtdb.firebaseio.com/',
    'storageBucket':'faceattendacerealtime-23cfc.appspot.com'
})
bucket = storage.bucket()
def msg_box():

    fileName = entry.get()
    blobs = bucket.blob(f'file/{fileName}')
    blobs.download_to_filename("dowloadFile/" + fileName)
    print("Dowload thành công! ")
    messagebox.showinfo("tb", "Dowload thành công!")

main_window = tk.Tk()
main_window.geometry("400x300+500+200")
main_window.title("dowload file from fisebase")
main_window.config(bg='#CC9999')

# tao widget lable de hien thi huong dan
lable = tk.Label(main_window, text="nhập tên file")
lable.place(x=50, y=50)
lable.config(font=("Arial", 10), justify="left", foreground="#009966")

# tạo widget entry nhập liệu
entry = tk.Entry(main_window, width=35)
entry.place(x=150, y=50)

# tạo nút nhấn
button = tk.Button(main_window, text="Dowload", command=msg_box, activebackground="black",
                        activeforeground="white",  fg="#009966",
                        font=('Helvetica bold', 15))
button.place(x=200, y=120)


main_window.mainloop()
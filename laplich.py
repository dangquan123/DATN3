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


def msg_box():
    print(f"Selected item: {value_com_thu.get()},{value_com_h_in.get()},{value_com_h_out.get()}, "
          f"{value_com_p_in.get()},{value_com_p_out.get()}{entry_u.get()}")
    try:
        ref = db.reference(f'lap lich/{value_com_thu.get()}')
        ref.child(f"{value_com_h_in.get()},{value_com_p_out.get()}-{value_com_h_out.get()},{value_com_p_out.get()}").set(f"{entry_u.get()}.txt")
    except:
        messagebox.showwarning("thông báo!", "lỗi firbase!")

    messagebox.showinfo("thông báo!", "đã lập lịch thành công!")
def dowload():
    fileName = entry_D.get()
    try:
        blobs = bucket.blob(f'file/{fileName}')
        blobs.download_to_filename("dowloadFile/" + fileName)
    except:
        messagebox.showinfo("tb", "lỗi!(nhập sai file hoặc wifi có vấn đề")
    else:
        messagebox.showinfo("tb", "Dowload thành công!")
        print("dowload thành công")


main_window = tk.Tk()
main_window.geometry("800x600+200+100")
main_window.title("Đồ án tốt nghiệp")
main_window.config(bg='#CC9999')

def label(text, x, y, fontize=10):
    label = tk.Label(main_window, text=text, background="#CC9999")
    label.place(x=x, y=y)
    label.config(font=("Arial", fontize), justify="left", foreground="black", border=0)

def entry(width, x, y):
    entry = tk.Entry(main_window, width=width, border=4)
    entry.place(x=x, y=y)
    return entry  # Thêm dòng này để có thể sử dụng entry ở phạm vi toàn cục

def button(text, x, y, width, height, command):
    button = tk.Button(main_window, text=text, command=command, activebackground="black",
                            activeforeground="white", fg="#009966", background="#CC9999", foreground="green",
                            font=('Helvetica bold', 20), width=width, height=height, border=5)
    button.place(x=x, y=y)

def comboboxd(choices, value_defound, x, y):
    combobox = ttk.Combobox(main_window, values=choices, foreground='#000022', background="lightblue",
                            width=7, justify="center")
    combobox.set(value_defound)
    combobox.place(x=x, y=y)
    return combobox

choices = ['thu2','thu3', 'thu4', 'thu5', 'thu6', 'thu7', 'cn']
choices1 = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']
choices2 = ['00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24'
            ,'25','26','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45','46',
            '47','48','49','50','51','52','53','54','55','56','57','58','59','60']

value_defound1 = '7'
value_defound2 = '00'
value_defound = "thu2"

entry_h=100
value_com_thu = comboboxd(choices, value_defound, 50, entry_h)
value_com_h_in = comboboxd(choices1, value_defound1, 200, entry_h)
value_com_h_out = comboboxd(choices1, value_defound1, 200, entry_h+50)
value_com_p_in = comboboxd(choices2, value_defound2, 350, entry_h+50)
value_com_p_out = comboboxd(choices2, value_defound2, 350, entry_h)

bnt = button("ok", 500, 140,10,2 ,msg_box)

entry_u = entry(30, 500, entry_h)

label_h = 70
label("LAPLICH", 50, 30)
label("chọn thứ", 50, label_h)
label("(start)", 150, 100)
label("(end)", 150, 150)
label(":", 300, 100)
label(":", 300, 150)
label("chọn giờ", 200, label_h)
label("chọn phút", 350, label_h)

label("file danh sách", 500, label_h)

label("DOWLOAD", 70, 260)

label("ĐỒ ÁN TỐT NGHIỆP - ĐẶNG HỒNG QUÂN - LÊ XUÂN SƠN", 130, 510, 15)

entry_D = entry(30, 70, 290)
bnt_D = button("dowload", 270, 290, 7,0, dowload)


main_window.mainloop()

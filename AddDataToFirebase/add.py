import os.path
import tkinter as tk
import cv2
from PIL import Image, ImageTk
import util
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendacerealtime-23cfc-default-rtdb.firebaseio.com/',
    'storageBucket': 'faceattendacerealtime-23cfc.appspot.com'
})

class App:
    def __init__(self):
        self.ref = db.reference('Students')
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+50+100")
        #
        # self.login_button_main_window = util.get_button(self.main_window, 'login', 'green', self.login)
        # self.login_button_main_window.place(x=750, y=200)
        #
        # self.logout_button_main_window = util.get_button(self.main_window, 'logout', 'red', self.logout)
        # self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'GET DATA', 'green',
                                                                    self.register_new_user, fg='white')
        self.register_new_user_button_main_window.place(x=750, y=250)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        self.most_recent_capture_arr = frame
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)
    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+50+60")

        self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window, 'Try again', 'red', self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.id = util.get_entry_text(self.register_new_user_window)
        self.id.place(x=870, y=60)

        self.id_label = util.get_text_label(self.register_new_user_window, 'ID: ')
        self.id_label.place(x=730, y=60)

        self.name = util.get_entry_text(self.register_new_user_window)
        self.name.place(x=870, y=170)

        self.name_label = util.get_text_label(self.register_new_user_window, 'Name: ')
        self.name_label.place(x=730, y=170)

        # self.total_attendance = util.get_entry_text(self.register_new_user_window)
        # self.total_attendance.place(x=870, y=140)

        # self.total_attendance_label = util.get_text_label(self.register_new_user_window, 'Total: ')
        # self.total_attendance_label.place(x=730, y=140)
        #
        # self.fist_attendance_time = util.get_entry_text(self.register_new_user_window)
        # self.fist_attendance_time .place(x=870, y=190)
        #
        # self.fist_attendance_time_label  = util.get_text_label(self.register_new_user_window, 'fistTime: ')
        # self.fist_attendance_time_label.place(x=730, y=190)
        #
        # self.last_attendance_time = util.get_entry_text(self.register_new_user_window)
        # self.last_attendance_time.place(x=870, y=240)
        #
        # self.last_attendance_time_label = util.get_text_label(self.register_new_user_window, 'lastTime: ')
        # self.last_attendance_time_label.place(x=730, y=240)
    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        id = str(self.id.get(1.0, "end-1c"))
        name = str(self.name.get(1.0, "end-1c"))
        total = 0
        fistTime = '0'
        lastTime = '0'
        img = cv2.resize(self.most_recent_capture_arr, (216,216))
        self.ref.child(id).set({'name': name, 'total_attendance': total, 'fist_attendance_time': fistTime, 'last_attendance_time': lastTime})
        cv2.imwrite("../images/" + id + '.jpg', img)

        # Chuyển đổi hình ảnh thành bytes
        _, img_encoded = cv2.imencode('.jpg', img)
        img_bytes = img_encoded.tobytes()
        # gửi hình ảnh lên firebase
        bucket = storage.bucket()
        blob = bucket.blob("database/{}.jpg".format(id))
        blob.upload_from_string(img_bytes, content_type='image/jpeg')

        self.register_new_user_window.destroy()

if __name__ == "__main__":
    app = App()
    app.start()

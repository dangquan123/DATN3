
import cv2
import face_recognition
import cvzone
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime
from ultralytics import YOLO
import math

# ngưỡng sác xuất nhận dạng, phát hiện ảnh giả
confidence = 0.75

soSanhLayAnh = 0.47
flag_diemdanh = 0
idClears = []
idCheck = []
totalCheck = []

# kết nối với firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendacerealtime-23cfc-default-rtdb.firebaseio.com/',
    'storageBucket':'faceattendacerealtime-23cfc.appspot.com'
})

# tạo đối tượng để sử dụng kho lưu trữ trên firebase
bucket = storage.bucket()

# lấy hình ảnh từ camera
cap = cv2.VideoCapture(0)
cap.set(1, 1280)
cap.set(2, 720)

# lấy dữ liệu đã mã hóa từ file

# print("đang lấy dữ liệu mã hóa ...")
# file = open('EncodeFile.p', 'rb')
# encodeListKnownWithIds = pickle.load(file)
# file.close()
# encodeListKnown, studentIds = encodeListKnownWithIds
# print("đã lấy dữ liệu mã hóa xong")


# tạo đối tượng phân biệt real fake
model = YOLO("best.pt")
classNames = ["fake", "real"]

# hàm thêm vào file excel
def join(id, tendanhsach):

    danhsach = f"./danhsach/{tendanhsach}"
    listClass = []
    list_id = []
    lines = []

    #lấy danh sách để điểm danh những học sinh có trong danh sách, còn không có thì không điểm danh
    with open(danhsach, "r") as f:
        for line in f.readlines():
            line = line[0:-1]
            line.strip()
            listClass.append(line)

    if id in listClass:
        # gửi dữ liệu lên database
        ref = db.reference(f'Students/{id}')
        studentInfo['total_attendance'] += 1
        ref.child("total_attendance").set(studentInfo['total_attendance'])

        if studentInfo['total_attendance'] == 1:
            fistTime = datetime.now()
            fistTime = fistTime.strftime('%H:%M:%S %d/%m/%Y')
            ref.child('fist_attendance_time').set(fistTime)
        else:
            lastTime = datetime.now()
            lastTime = lastTime.strftime('%H:%M:%S %d/%m/%Y')
            ref.child('last_attendance_time').set(lastTime)

        print(f'{id}, {studentInfo["total_attendance"]}, {studentInfo["fist_attendance_time"]},{studentInfo["last_attendance_time"]}\n')

        # thêm vào file excel
        with open(fileNames, 'r+') as file:
            for j in file.readlines():
                lines.append(j)
                entry = j.split(',')
                list_id.append(entry[0])
            #nếu id không có trong danh sách thì thêm vào, có thì thay thế bằng dữ liệu mới
            if id not in list_id:
                file.writelines(f'{id},{studentInfo["name"]}, {studentInfo["total_attendance"]}, {studentInfo["fist_attendance_time"]},{studentInfo["last_attendance_time"]}')
            else:
                for i, line in enumerate(list_id):
                    if id == line:
                        with open(fileNames, 'w') as f:
                            lines[i] = f'{id}, {studentInfo["total_attendance"]}, {studentInfo["fist_attendance_time"]}, {studentInfo["last_attendance_time"]}\n'
                            f.writelines(lines)
    else:
        print(f"{id} không có trong danh sách\n")
# kiểm tra những id dị biệt
def check_total(file_name_check):

    idCheck = []
    totalCheck = []
    selected_numbers = []
    index_id = []
    value_idCheck_suspicion = []
    total_difference = []

    with open(file_name_check, "r") as f:
        for i in f.readlines():
            list_line = i.split(",")
            idCheck.append(int(list_line[0].strip()))
            totalCheck.append(int((list_line[1]).strip()))
    # 4 người trở lên mới check
    if len(idCheck) < 2:
        return

    numbers = list(totalCheck)
    numbers.sort()
    min_difference = 0

    for i in range(len(numbers) - 1):
        current_difference = numbers[i + 1] - numbers[i]
        total_difference.append(current_difference)

    for i in range(len(numbers) - 1):
        current_difference = numbers[i + 1] - numbers[i]
        if current_difference > min_difference:
            tong = sum(total_difference)
            trung_binh = tong / len(total_difference)
            if current_difference > trung_binh + 50:
                min_difference = current_difference
                selected_numbers = numbers[i]

    if not selected_numbers:
        return

    index_value = numbers.index(selected_numbers)
    for i in range(index_value + 1):
         for index, value in enumerate(totalCheck):
             if value == numbers[i]:
                 if index not in index_id:
                    index_id.append(index)

    idCheck_suspicion = index_id
    for i in idCheck_suspicion:
        value_idCheck_suspicion.append(idCheck[i])

    value = [value_idCheck_suspicion, idCheck]
    return(value)


while True:

    thu_tieng_viet = ["thu2", "thu3", "thu4", "thu5", "thu6", "thu7", "cn"]
    current_daytime = datetime.now()
    current_daytime = thu_tieng_viet[current_daytime.weekday()]
    ref_lichhoc = db.reference(f'lap lich/{current_daytime}')
    get = ref_lichhoc.get()

    typeTime = ["%H", "%M", "%S", "%H.%M"]
    # current_time = float(datetime.now().strftime(typeTime[1]))
    current_time = float(datetime.now().strftime(f"{typeTime[0]}.{typeTime[1]}"))
    print(f"hôm nay là: {current_daytime}----real time: {current_time}")
    if get:
        for gio, tendanhsach in get.items():

            try:
                gio = gio.split("-")
                gio_bat_dau = round(float(gio[0].replace(",", ".")), 2)
                gio_ket_thuc = round(float(gio[1].replace(",",".")), 2)
            except Exception as e:
                print(f"loi xay ra {e}")
            print(f"gio bat dau{gio_bat_dau}, gio ket thuc {gio_ket_thuc}")
            if (gio_bat_dau < current_time < gio_ket_thuc):

                blobs = bucket.blob(f'danhsach/{tendanhsach}')
                blobs.download_to_filename("danhsach/" + tendanhsach)
                print("Dowload thành công! ")

                # mã hóa các khuôn mặt có trong danh sách từ firebase
                idTrongDanhSach = []
                with open(f"danhsach/{tendanhsach}", 'r') as f:
                    for line in f.readlines():
                        line = line.replace("\n", "")
                        line.strip()
                        idTrongDanhSach.append(line)

                imgList = []
                studentIds = []
                encodeList = []
                file_names = []
                file_names_output = []

                bucket = storage.bucket()
                blobs = bucket.list_blobs(prefix="database/")
                for blob in blobs:
                    file_names.append(blob.name)

                print("\n\nbắt đầu mã hóa ...")
                for file_name in file_names:

                    file_name = file_name.split("/")[-1]
                    id = file_name.split(".")[0]
                    if id in idTrongDanhSach:
                        studentIds.append(file_name.split(".")[0])
                        file_names_output.append(file_name)

                        blob = bucket.get_blob(f'database/{file_name}')
                        array = np.frombuffer(blob.download_as_string(), np.uint8)
                        imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)
                        imgStudent = cv2.cvtColor(imgStudent, cv2.COLOR_BGR2RGB)
                        encode = face_recognition.face_encodings(imgStudent)
                        if encode:
                            encodeList.append(encode[0])
                        else:
                            print("không tìm thấy khuôn mặt nào để mã hóa")

                encodeListKnown = encodeList
                print(f"id đã được mã hóa{studentIds}")
                print("mã hóa xong\n")

                # tạo file điểm danh
                tendanhsachOut = tendanhsach.split('.')[0]
                outputFile = f"./outputCSV/{tendanhsachOut}"
                extension = datetime.now()
                extension = f"({gio})" + extension.strftime('(%d-%m-%Y)')
                with open(outputFile + extension + ".csv", "a") as f:
                    f.write("")
                fileNames = outputFile + extension + ".csv"

            while (gio_bat_dau < current_time < gio_ket_thuc):

                flag_diemdanh = 1
                success, img = cap.read()

                # nhận dạng real fake
                faceCurFrame1 = face_recognition.face_locations(img)
                for faceLoc in faceCurFrame1:
                    y1, x2, y2, x1 = faceLoc
                    h, w = x2 - x1, y2 - y1
                    img1 = img[y1:y1+w, x1:x1+h]

                    results = model(img, stream=True, verbose=False)

                    for r in results:
                        boxes = r.boxes
                        for box in boxes:
                            # lấy thông tin vị trí khuôn mặt
                            x1, y1, x2, y2 = box.xyxy[0]
                            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                            h, w = x2 - x1, y2 - y1

                            # sác xuất
                            conf = math.ceil((box.conf[0] * 100)) / 100
                            cls = int(box.cls[0])
                            print(f"real/fake = {cls}, confident={conf}")
                            if conf > confidence:
                                if classNames[cls] == 'fake':
                                    # phủ trắng các gương mặt fake
                                    matrix_white = np.full((w, h, 3), 255, dtype=np.uint8)
                                    img[y1:y1 + w, x1:x1 + h] = matrix_white

                # mã hóa khuôn mặt trên camera
                imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
                faceCurFrame = face_recognition.face_locations(imgS)
                encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

                # so sánh khuông mặt trên camera dữ liệu mã hóa trước đó, vẽ đường bao xung quanh khuôn mặt
                for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                    print("giá trị so sánh: " + str(faceDis))
                    matchIndex = np.argmin(faceDis)
                    valueMatchIndex = np.amin(faceDis)
                    print(f"id ({matchIndex}) có sai số nhỏ nhất: {round(valueMatchIndex,2)}")

                    if valueMatchIndex < soSanhLayAnh:
                        id = studentIds[matchIndex]
                        idClears.append(id)
                        # lấy dữ liệu từ database về
                        studentInfo = db.reference(f'Students/{id}').get()

                        join(id, tendanhsach)
                    else:
                        id = "unknow"

                    #vẽ đường bao khuôn mặt
                    if id != "unknow":
                        color_box = (20, 250,40 )
                    else:
                        color_box = (0, 0, 255)
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = x1, y1, x2 - x1, y2 - y1
                    imgBackGround = cvzone.cornerRect(img, bbox, rt=0, colorR=color_box)
                    cv2.putText(img, id, (x2, y2), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)

                # cập nhật biến dừng vòng lặp
                # current_time = float(datetime.now().strftime(typeTime[2]))
                current_time = float(datetime.now().strftime(f"{typeTime[0]}.{typeTime[1]}"))
                cv2.imshow("DATN", img)
                cv2.waitKey(1)


            if flag_diemdanh:
                flag_diemdanh = 0

                # kiểm tra những id dị biệt, và cài đặt total_attention trong buổi điểm danh về 0
                id_suspicion = check_total(outputFile + extension + ".csv")
                idDuocDiemDanh = []
                idKhongCoMat = []
                with open(outputFile + extension + ".csv", 'r') as f:
                    for line in f.readlines():
                        line = line.replace("\n", "")
                        line.split(",")
                        line.strip()
                        idDuocDiemDanh.append(line[0])

                for i in idTrongDanhSach:
                    if i not in idDuocDiemDanh:
                        idKhongCoMat.append(i)
                title = []
                print("\n\n\n------KẾT QUẢ-----\nkết quả điểm danh: [id, tổng số lần điểm danh, giờ vào, giờ ra]")
                with open(outputFile + extension + ".csv", "r") as f:
                    for i in f.readlines():
                        print(i, end='')
                print(f"\n\nid có trong danh sách: {idTrongDanhSach}")
                print(f"id vắng: {idKhongCoMat}")

                # with open(outputFile + extension + ".csv", 'a') as f:
                #     f.write("\nkhong co mat," + str(idKhongCoMat).strip('[]').replace("'",""))

                # thêm title cho file output
                with open(outputFile + extension + ".csv", "r") as f:
                    title = f.readlines()
                for i,titleline in enumerate(title):
                    new = titleline.strip('\n') + ', co\n'
                    title[i] = new

                title.insert(0,"ID,TONG SO DIEM DANH,THOI GIAN BAT DAU,THOI GIAN KET THUC,KET QUA\n")

                for i in idKhongCoMat:
                    title.append(f"{i},,,, vang\n")

                with open(outputFile + extension + ".csv", "w") as f:
                    f.writelines(title)

                if id_suspicion:
                    if len(id_suspicion[1]) > 2 :
                        for i, line in enumerate(title):
                           for j in id_suspicion[0]:
                               if line[0] == str(j):
                                    title[i] = title[i].replace("co", "thieu gio hoc")
                        with open(outputFile + extension + ".csv", "w") as f:
                            f.writelines(title)
                        # with open(outputFile + extension + ".csv", 'a') as f:
                        #     f.write("\n\nid_nghi_ngo," + str(id_suspicion[0]).strip('[]'))
                # gửi file điểm danh lên file base
                bucket = storage.bucket()
                blob = bucket.blob("file/" + tendanhsachOut + extension + ".csv")
                blob.upload_from_filename(fileNames)

                for idClear in idClears:
                    refclear = db.reference(f'Students/{idClear}')
                    refclear.child("total_attendance").set(0)

                print(f"----DONE---- {gio}\n\n\n\n")
cv2.destroyAllWindows()





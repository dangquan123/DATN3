import cv2
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import numpy as np

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendacerealtime-23cfc-default-rtdb.firebaseio.com/',
    'storageBucket':'faceattendacerealtime-23cfc.appspot.com'
})

#import student image into list
# folderPath = "images"
# PathList = os.listdir(folderPath)
# print(len(PathList))
imgList = []
studentIds = []
# for path in PathList:
#
#     imgList.append(cv2.imread(os.path.join(folderPath, path)))
#     studentIds.append(os.path.splitext(path)[0])
    # filename = f'{folderPath}/{path}'
    # bucket = storage.bucket()
    # blob = bucket.blob(filename)
    # blob.upload_from_filename(filename
bucket = storage.bucket()
blobs = bucket.list_blobs(prefix="database/")
encodeList = []
    # for img in imagesList:
    #     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #     encode = face_recognition.face_encodings(img)[0]
    #     encodeList.append(encode)
    # Tạo một danh sách để lưu tên các tệp
file_names = []
file_names_output = []

for blob in blobs:
    file_names.append(blob.name)

for file_name in file_names:

    file_name = file_name.split("/")[-1]
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

print("Encoding Started ...")
encodeListKnown = encodeList
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")
print(studentIds)
file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")
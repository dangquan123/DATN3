import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import cv2

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendacerealtime-23cfc-default-rtdb.firebaseio.com/',
    'storageBucket':'faceattendacerealtime-23cfc.appspot.com'
})

img = cv2.imread('./images/2.png')

# Chuyển đổi hình ảnh thành bytes
_, img_encoded = cv2.imencode('.jpg', img)
img_bytes = img_encoded.tobytes()
#gửi hình ảnh lên firebase
bucket = storage.bucket()
blob = bucket.blob("imgg")
blob.upload_from_string(img_bytes,  content_type='image/jpeg')
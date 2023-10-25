from firebase_admin import credentials
from firebase_admin import storage
import firebase_admin

# kết nối với firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendacerealtime-23cfc-default-rtdb.firebaseio.com/',
    'storageBucket':'faceattendacerealtime-23cfc.appspot.com'
})

# tạo đối tượng để sử dụng kho lưu trữ trên firebase
bucket = storage.bucket()

# dowload file từ firebase
bucket = storage.bucket()
blob = bucket.blob("file/thamdu.csv")
blob.download_to_filename("thamdu.csv")
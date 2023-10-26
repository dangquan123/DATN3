from firebase_admin import credentials
from firebase_admin import storage
import firebase_admin
import numpy as np
import cv2

# kết nối với firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendacerealtime-23cfc-default-rtdb.firebaseio.com/',
    'storageBucket':'faceattendacerealtime-23cfc.appspot.com'
})

bucket = storage.bucket()
fileName = '(12h45m 26-10-2023).csv'
blobs = bucket.blob(f'file/{fileName}')
blobs.download_to_filename("dowloadFile/" + fileName)
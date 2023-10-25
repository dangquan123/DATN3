import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://faceattendacerealtime-23cfc-default-rtdb.firebaseio.com/'
})

ref = db.reference('Students')
data = {
    '1':
        {
            'name':'quan',
            'total_attendance':6,
            'last_attendance_time':'2023-12-25 16:34:00',
            'fist_attendance_time':'2023-12-25 16:34:00'
},
    '2':
        {
            'name':'messi',
            'total_attendance':6,
            'last_attendance_time':'2023-12-25 16:34:00',
            'fist_attendance_time':'2023-12-25 16:34:00'
        },
    '3':
        {
            'name':'mtp',
            'total_attendance':6,
            'last_attendance_time':'2023-12-25 16:34:00',
            'fist_attendance_time':'2023-12-25 16:34:00'
        }
}

for key, value in data.items():
    ref.child(key).set(value)

studentInfo = db.reference(f'Students/{1}').get()
print(studentInfo)


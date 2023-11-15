numbers1 = [1, 5, 15,  7, 10, 24, 16, 17, 18,12,34,15,65]
def check_total(file_name_check):

    idCheck = []
    totalCheck = []
    selected_numbers = []
    index_id = []
    value_idCheck_suspicion = []

    with open(file_name_check, "r") as f:
        for i in f.readlines():
            list_line = i.split(",")
            idCheck.append(int(list_line[0].strip()))
            totalCheck.append(int((list_line[1]).strip()))

    numbers = list(totalCheck)
    numbers.sort()
    min_difference = 0

    for i in range(len(numbers) - 1):
        current_difference = numbers[i + 1] - numbers[i]
        if current_difference > min_difference:
            min_difference = current_difference
            selected_numbers = numbers[i]

    index_value = numbers.index(selected_numbers)
    for i in range(index_value + 1):
         for index, value in enumerate(totalCheck):
             if value == numbers[i]:
                 if index not in index_id:
                    index_id.append(index)

    idCheck_suspicion = index_id
    for i in idCheck_suspicion:
        value_idCheck_suspicion.append(idCheck[i])


    return (value_idCheck_suspicion, idCheck)

# # filename = "outputCSV/DATN(['1', '10'])(13-11-2023).csv"
# # id, idc = check_total(filename)
# # print(type(id))
# # with open(filename, "a") as f:
# #     f.write(str(id))
#
# numbers = list(numbers1)
# numbers.sort()
# min_difference = 0
# total_difference = []
# for i in range(len(numbers) - 1):
#     current_difference = numbers[i + 1] - numbers[i]
#     total_difference.append(current_difference)
#     if current_difference > min_difference:
#         min_difference = current_difference
#         selected_numbers = numbers[i]
#
# def tinh_trung_binh(danh_sach):
#     tong = sum(danh_sach)
#     trung_binh = tong / len(danh_sach)
#     return trung_binh
#
# trung_binh = tinh_trung_binh(total_difference)
#
# print(trung_binh)

import cv2
import cvzone
import face_recognition

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    faceCurFrame1 = face_recognition.face_locations(img)
    print(faceCurFrame1)
    for faceLoc in faceCurFrame1:
        y1, x2, y2, x1 = faceLoc
        bbox = x1, y1, x2 - x1, y2 - y1
        imgBackGround = cvzone.cornerRect(img, bbox, rt=0)
    cv2.imshow("quan",imgBackGround)
    cv2.waitKey(1)

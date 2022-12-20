import numpy as np
import cv2
import os
import sqlite3
from sqlite3 import Error

def create_database():
    try:
        con = sqlite3.connect('Students.db')
        print("Connection is established: Database is created in memory")

        cursorObl = con.cursor()

        cursorObl.execute("CREATE TABLE students(mssv integer PRIMARY KEY, name text)")

        con.commit()
    except Error:
        print(Error)
    finally:
        con.close()

def insert_student(entities):
    con = sqlite3.connect('Students.db')

    cursorObj = con.cursor()

    cursorObj.execute('INSERT INTO students(mssv, name) VALUES(?, ?)', entities)

    con.commit()
    con.close()

def list_student():
    con = sqlite3.connect('Students.db')

    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM students')


name = input("Nhập tên(Không viết dấu): ")
mssv = input("MSSV: ")
# entities = (mssv, name)
# insert_student(entities)
name = name.split(" ")
newname = None
for x in name:
    if newname == None:
        newname = x
    else:
        newname += ('_' + x)

label = newname+'_'+mssv
cam = cv2.VideoCapture(0)

# Biến đếm để xác định số ảnh đã chụp
i = 0
while True:
    # Capture frame-by-frame

    ret, frame = cam.read()
    frame = cv2.flip(frame, 1)
    if not ret:
        continue

    # Vẽ khung giữa màn hình để người dùng đưa mặt vào
    centerH = frame.shape[0] // 2;
    centerW = frame.shape[1] // 2;
    sizeboxW = 300;
    sizeboxH = 400;

    # Tạo thư mục nếu chưa có
    imagefolder = 'DataSet/FaceData/raw/' + str(label)
    if not os.path.isdir(imagefolder):
        os.mkdir(imagefolder)

    # Lưu dữ liệu
    if cv2.waitKey(1) & 0xFF == 32:
        if not cv2.imwrite(imagefolder + "/" + str(name[-1]) + '_' + str(i) + ".jpg", frame):
            raise Exception("Could not write image")
        i += 1
    cv2.rectangle(frame, (centerW - sizeboxW // 2, centerH - sizeboxH // 2),
                  (centerW + sizeboxW // 2, centerH + sizeboxH // 2),
                  (255, 255, 255), 5)
    cv2.putText(frame, f'Images Captured: {i}/10', (30, 30), cv2.FONT_HERSHEY_SIMPLEX
                , 1, (255, 0, 255), 2, cv2.LINE_AA)

    # Hiển thị
    cv2.imshow('frame', frame)

    if (cv2.waitKey(1) == ord('q') or i == 10):
        break

# When everything done, release the capture
cam.release()
cv2.destroyAllWindows()
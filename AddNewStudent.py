import numpy as np
import cv2
import os
import sqlite3
from sqlite3 import Error

try:
    con = sqlite3.connect('Students.db')
except Error:
    print(Error)


def check_table(con):
    cursorObj = con.cursor()
    list_of_table = cursorObj.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Students';").fetchall()
    if list_of_table == []:
        print("Table not found!")
        return True
    else:
        print("Table exists")
        return False


def sql_table(con):
    cursorObj = con.cursor()
    if check_table(con):
        cursorObj.execute("CREATE TABLE Students(mssv integer PRIMARY KEY, name text)")
        con.commit()


def check_data(con, mssv, name):
    cursorObj = con.cursor()
    data = cursorObj.execute(f"SELECT * FROM Students WHERE mssv={mssv} AND name='{name}'").fetchall()
    if data == []:
        print("Thong tin chua co trong database")
        return True
    else:
        print("Thong tin da co trong database")
        return False


def insert_student(con, mssv, name):
    cursorObj = con.cursor()
    cursorObj.execute('INSERT INTO students(mssv, name) VALUES(?, ?)', (mssv, name))
    con.commit()


# Nhập tên và mssv
name = input("Nhập tên(Không viết dấu): ")
mssv = input("MSSV: ")


# Tạo bảng và nạp dữ liệu với tên được chuẩn hóa
sql_table(con)
if check_data(con, mssv, name):
    insert_student(con, mssv, name)
    con.close()


    # Xử lý tên để đặt file ảnh
    name = name.split(" ")
    newname = None
    for x in name:
        if newname == None:
            newname = x
        else:
            newname += ('_' + x)


    #Bắt đầu lấy ảnh
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
        print(os.path.isdir(imagefolder))
        if not os.path.isdir(imagefolder):
            os.makedirs(imagefolder)
        print(imagefolder)
        print(os.path.isdir(imagefolder))

        # Lưu dữ liệu
        if cv2.waitKey(1) & 0xFF == 32:
            if not cv2.imwrite(imagefolder + "/" + str(newname) + '_' + str(i) + ".jpg", frame):
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
con.close()
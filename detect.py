import os
import shutil
import cv2
import pafy
import mysql.connector
from ultralytics import YOLO
from dotenv import load_dotenv

load_dotenv()

YOLOV8_MODEL = YOLO("yolov8n.pt")
CONNECTION =mysql.connector.connect(    
    host = os.getenv("MYSQL_HOST"),
    user = os.getenv("MYSQL_USER"),
    password = os.getenv("MYSQL_PASSWORD"),
    database = os.getenv("MYSQL_DATABASE"))

def check_directory():
    detect_dir_path = "./detect_images"
    runs_dir_path = "./runs"

    if os.path.isdir(detect_dir_path):
        shutil.rmtree(detect_dir_path)
    
    if os.path.isdir(runs_dir_path):
        shutil.rmtree(runs_dir_path)

    os.mkdir(detect_dir_path)
    os.mkdir(runs_dir_path)

def get_images(spot_data):
    update_data = []

    for i in range(len(spot_data)):
        id = spot_data[i]["id"]
        url = spot_data[i]["spots_url"]
        dir_path = "./detect_images"
        ext = "jpg"
        video = pafy.new(url)
        best = video.getbest(preftype="mp4")
        cap = cv2.VideoCapture(best.url)

        if not cap.isOpened():
            return

        os.makedirs(dir_path, exist_ok=True)
        base_path = os.path.join(dir_path, str(id))
        ret, frame = cap.read()
        cv2.imwrite('{}.{}'.format(base_path, ext), frame)

        results = YOLOV8_MODEL("./detect_images" ,save=True, classes=0)    
        box_count = len(results[0].boxes.data)
        update_data.append([id, box_count, spot_data[i]["spots_day_count"], spot_data[i]["spots_month_count"]])
    
    return update_data

def select_databese():
    cursor = CONNECTION.cursor(dictionary=True)
    cursor.execute("SELECT * FROM spots")
    spot_data = cursor.fetchall()
    CONNECTION.commit()
    cursor.close()

    return spot_data

def update_database(update_data):
    cursor = CONNECTION.cursor(dictionary=True)

    for i in range(len(update_data)):
        spots_id = update_data[i][0]
        spots_count = update_data[i][1]
        spots_day_count = update_data[i][2]
        spots_month_count = update_data[i][3]
        day_list = []
        month_list = []

        if spots_day_count == "None":
            day_list = [spots_count]
        else:
            day_list = spots_day_count.split(",")
            day_list.append(spots_count)

            if len(day_list) >= 25:
                day_name = ""
                day_list_backup = ",".join(map(str, day_list))
                cursor.execute("SELECT * FROM days WHERE spots_id =%s" % (spots_id))
                day_data = cursor.fetchall()
                if len(day_data) >= 35:
                    cursor.execute("DELETE FROM days WHERE spots_id = %s AND WHERE id = (SELECT MIN(id) FROM days)" % (spots_id)) 
                    cursor.execute("INSERT INTO days (spots_id, days_name, days_count) VALUES ('%s', '%s', '%s')" % (spots_id, day_name, day_list_backup))
                else:
                    cursor.execute("INSERT INTO days (spots_id, days_name, days_count) VALUES ('%s', '%s', '%s')" % (spots_id, day_name, day_list_backup))
        
        if len(day_list) >= 25:
            day_list = [spots_count]
            average = sum(day_list)
            
            if spots_month_count == "None":
                month_data = "0," * 29
                month_list = month_data.split(",")
                month_list.pop(29)
                month_list.append(average)
            else:
                month_list = spots_month_count.split(",")
                month_list.append(average)
                month_list.pop(0)
            
            month_list = ",".join(map(str, month_list))
            cursor.execute("UPDATE spots SET spots_month_count = '%s' WHERE id = %s" % (month_list, spots_id))  

        day_list = ",".join(map(str, day_list))
        cursor.execute("UPDATE spots SET spots_count = '%s' WHERE id = %s" % (spots_count, spots_id))  
        cursor.execute("UPDATE spots SET spots_day_count = '%s' WHERE id = %s" % (day_list, spots_id))

    CONNECTION.commit()
    cursor.close()

def main():
    check_directory()
    spot_data = select_databese()
    update_data = get_images(spot_data)
    update_database(update_data)

main()
import os
import shutil
import cv2
import pafy
from fastapi import FastAPI
from typing import List
from ultralytics import YOLO

APP = FastAPI()
YOLOV8_MODEL = YOLO("./yolo_models/yolov8n.pt")

def check_directory():
    detect_dir_path = "detect_images"
    runs_dir_path = "runs"

    if os.path.isdir(detect_dir_path):
        shutil.rmtree(detect_dir_path)
    
    if os.path.isdir(runs_dir_path):
        shutil.rmtree(runs_dir_path)

    os.mkdir(detect_dir_path)
    os.mkdir(runs_dir_path)

def get_images(spot_data):
    update_data = []

    for i in range(len(spot_data)):
        spot_key = spot_data[i]["spot_key"]
        url = spot_data[i]["url"]
        dir_path = "detect_images"
        ext = "jpg"
        video = pafy.new(url)
        best = video.getbest(preftype="mp4")
        cap = cv2.VideoCapture(best.url)

        if not cap.isOpened():
            return

        os.makedirs(dir_path, exist_ok=True)
        base_path = os.path.join(dir_path, spot_key)
        ret, frame = cap.read()
        cv2.imwrite('{}.{}'.format(base_path, ext), frame)

        results = YOLOV8_MODEL("detect_images/%s.jpg" % spot_key ,save=True, classes=0)    
        box_count = len(results[0].boxes.data)
        update_data.append({
            "spot_key": spot_key,
            "count": box_count
        })
        
    return update_data

@APP.post("/batch_detection")
async def detect(spot_data: List[dict]):
    check_directory()
    response = get_images(spot_data)

    return response
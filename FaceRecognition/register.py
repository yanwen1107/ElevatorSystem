import os
import shutil
import numpy as np
import sqlite3
from database import create_db, adapt_array, convert_array
from retinaface import RetinaFace
import onnxruntime as ort
from face_recognition import face_detect
from face_recognition import feature_extract
import cv2
from PyQt5.QtWidgets import QMessageBox  # 引入QMessageBox

def register_into_database(user_name, img_rgb,parent_window):
    
    # initial detector and model
    detector = RetinaFace(quality='normal')
    onnx_path = 'model/arcface_r100_v1.onnx'
    sess = ort.InferenceSession(onnx_path)
    
    # Detect face and extract embeddings
    #img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_rgb, detections = face_detect(img_rgb, detector)

    if not detections:
        # 顯示錯誤信息並返回主畫面
        QMessageBox.critical(parent_window, "錯誤", "未檢測到人臉，請選擇包含人臉的圖片。")
        parent_window.back_to_main_window()
        return

    position, landmarks, embeddings = feature_extract(img_rgb, detections, sess)

    # Save in database folder
    folder_name = f"database/{user_name}"  
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    file_name = f"{user_name}.jpg"
    full_path = os.path.join(folder_name, file_name)
    img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
    cv2.imwrite (full_path, img_bgr)
    
    # Register into database
    db_path = 'database.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("BEGIN")
    
    try:
        # Insert or update if user_name already exists
        conn.execute("INSERT OR REPLACE INTO face_info (NAME, Embeddings) VALUES (?, ?)",
                        (user_name, adapt_array(embeddings)))
        conn.commit()
        print(f"Successfully registered {user_name} into the database.")
    except Exception as e:
        conn.rollback()
        print(f"Failed to register {user_name}: {str(e)}")
    finally:
        conn.close()


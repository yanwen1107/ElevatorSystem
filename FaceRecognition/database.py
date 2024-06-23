import sqlite3
import os
import numpy as np
import io
import cv2

def adapt_array(arr):
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)

    return sqlite3.Binary(out.read())


def convert_array(text):

    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)


def load_file(file_path):
    file_data = {}
    for person_name in os.listdir(file_path):
        person_dir = os.path.join(file_path, person_name)

        person_pictures = []
        for picture in os.listdir(person_dir):
            picture_path = os.path.join(person_dir, picture)
            person_pictures.append(picture_path)

        file_data[person_name] = person_pictures

    return file_data


def create_db(db_path, file_path, detector, sess):
    from face_recognition import face_detect, feature_extract  # avoid circle
    if os.path.exists(file_path):
        conn_db = sqlite3.connect(db_path)
        conn_db.execute('DROP TABLE IF EXISTS face_info')
        conn_db.execute("CREATE TABLE face_info \
                            (ID INTEGER PRIMARY KEY AUTOINCREMENT, \
                             NAME TEXT NOT NULL, \
                            Embeddings ARRAY NOT NULL)")
        file_data = load_file(file_path)
        for i, person_name in enumerate(file_data.keys()):
            picture_path = file_data[person_name]
            sum_embeddings = np.zeros([1, 512])
            for j, picture in enumerate(picture_path):
                img_bgr = cv2.imread(picture, cv2.IMREAD_COLOR)
                img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
                img_rgb, detections = face_detect(img_rgb, detector)
                position, landmarks, embeddings = feature_extract(img_rgb, detections, sess)
                sum_embeddings += embeddings

            final_embedding = sum_embeddings / len(picture_path)
            adapt_embedding = adapt_array(final_embedding)

            conn_db.execute("INSERT INTO face_info (ID, NAME, Embeddings) VALUES (?, ?, ?)",
                            (i, person_name, adapt_embedding))
        conn_db.commit()
        conn_db.close()
    else:
        print('database path does not exist')
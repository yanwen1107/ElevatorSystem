import numpy as np
import cv2

#detect
from retinaface import RetinaFace
import onnxruntime as ort

#alignment
from skimage import transform as trans

#feature_extract
from sklearn.preprocessing import normalize

# compare face
import sqlite3
from database import convert_array



detector = RetinaFace(quality="normal")
onnx_path = 'model/arcface_r100_v1.onnx'
sess = ort.InferenceSession(onnx_path)

# Face detection==========================================================================================
def face_detect(img_rgb, detector):
    #img_bgr = cv2.imread(img_path, cv2.IMREAD_COLOR)
    # img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    detections = detector.predict(img_rgb)

    return img_rgb, detections


def draw_bbox(img_rgb, detections, label):
    detection_result = dict(list(detections[0].items())[:4])
    x1, y1, x2, y2 = detection_result['x1'], detection_result['y1'], detection_result['x2'], detection_result['y2']
    img_result = cv2.rectangle(img_rgb.copy(), (x1, y1), (x2, y2), (0, 255, 0), 2) 
    
    # Font
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_color = (0, 255, 0)
    font_thickness = 2 
    
    # label
    label_size, _ = cv2.getTextSize(label, font, font_scale, font_thickness)

    label_x = x2 - label_size[0] 
    label_y = y2-10 

    # draw label
    cv2.putText(img_result, label, (label_x, label_y), font, font_scale, font_color, font_thickness)
    return img_result

#Face alignment========================================================================================
def face_align(img_rgb, landmarks):
    src = np.array([
        [30.2946, 51.6963],
        [65.5318, 51.5014],
        [48.0252, 71.7366],
        [33.5493, 92.3655],
        [62.7299, 92.2041]], dtype=np.float32)

    dst = np.array(landmarks, dtype=np.float32).reshape(5, 2)

    tform = trans.SimilarityTransform()
    tform.estimate(dst, src)

    M = tform.params[0:2, :]

    aligned = cv2.warpAffine(img_rgb, M, (112, 112), borderValue=0)

    return aligned
# Feature extraction=========================================================================================
def feature_extract(img_rgb, detections, sess):
    positions = []
    landmarks = []
    embeddings = np.zeros((len(detections), 512))
    for i, face_info in enumerate(detections):
        face_position = [face_info['x1'], face_info['y1'], face_info['x2'], face_info['y2']]
        face_landmarks = [face_info['left_eye'], face_info['right_eye'],
                          face_info['nose'], face_info['left_lip'], face_info['right_lip']]

        positions.append(face_position)
        landmarks.append(face_landmarks)

        aligned = face_align(img_rgb, face_landmarks)
        t_aligned = np.transpose(aligned, (2, 0, 1))

        inputs = t_aligned.astype(np.float32)
        input_blob = np.expand_dims(inputs, axis=0)

        first_input_name = sess.get_inputs()[0].name
        first_output_name = sess.get_outputs()[0].name

        prediction = sess.run([first_output_name], {first_input_name: input_blob})[0]
        final_embedding = normalize(prediction).flatten()

        embeddings[i] = final_embedding

    return positions, landmarks, embeddings

#Compare face=========================================================================
def compare_face(embeddings, threshold):

    conn_db = sqlite3.connect('database.db')
    cursor = conn_db.execute("SELECT * FROM face_info")
    db_data = cursor.fetchall()

    total_distances = []
    total_names = []
    for data in db_data:
        total_names.append(data[1])
        db_embeddings = convert_array(data[2])
        distance = round(np.linalg.norm(db_embeddings - embeddings), 2)
        total_distances.append(distance)
    total_result = dict(zip(total_names, total_distances))
    idx_min = np.argmin(total_distances)

    name, distance = total_names[idx_min], total_distances[idx_min]

    if distance > threshold:
        name = 'Unknown person'

    return name, distance, total_result
#Recognition==============================================================================================
def recognition(img_rgb, threshold):
    img_rgb, detections = face_detect(img_rgb, detector)
    if detections:
            positions, landmarks, embeddings = feature_extract(img_rgb, detections, sess)
            name, distance, total_result = compare_face(embeddings, threshold)
            img_result = draw_bbox(img_rgb, detections, name)
    else:
        img_result = img_rgb
        name=' '
    img_bgr = cv2.cvtColor(img_result, cv2.COLOR_RGB2BGR)
    return name, img_bgr

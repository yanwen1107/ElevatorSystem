# Package
import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
import socket
import io
from PIL import Image

# UI
from MainUI import Ui_MainWindow
from RegisterUI import Ui_RegisterWindow 
from RegisterCamUI import UI_RegisterCamWindow 

# Function from other code
from face_recognition import recognition  
from register import register_into_database

# UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,0)
s.bind(("192.168.22.28", 9090))
s.settimeout(0.1)

# global variable
name = 'Unknown person'

# Main Window ##########################################################################################################
class FaceRecognitionApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect button function -----------------------------------------------------
        self.ui.RegisterButton.clicked.connect(self.switch_to_register_window) # Register
        self.ui.RecognizeButton.clicked.connect(self.recognize_to_esp32) # Regognize (to esp32)
        
        # Connect to camera ---------------------------------------------------------
        self.camera_thread = CameraThread()
        self.camera_thread.frame_ready.connect(self.display_frame)
        self.camera_thread.start()

    # Switch to register window --------------------------------------------------------
    def switch_to_register_window(self):
        self.stop_camera()
        self.register_window = RegisterWindow(self)
        self.register_window.show()
        self.hide()
    
    # Display ----------------------------------------------------------------
    def display_frame(self, frame):
        self.camera_thread.current_frame = frame
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_img = QtGui.QImage(frame_rgb.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qt_img)
        current_size = self.ui.CameraView.size()
        scaled_pixmap = pixmap.scaled(current_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        if self.ui.CameraView.pixmap() is None:
            self.ui.CameraView.setScaledContents(False) 
            self.ui.CameraView.setMinimumSize(1, 1) 
        self.ui.CameraView.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.CameraView.setPixmap(scaled_pixmap)
    
    # Send recognize message to esp32----------------------------------------------------------
    def recognize_to_esp32(self):
        print(name)
        if(name !='Unknown person'):
            recognition_result = 'ok'
            print(type(recognition_result))
            print(recognition_result)
            s.sendto(recognition_result.encode(),('192.168.214.54',22000))

    # Control camera------------------------------------------------------------------
    def stop_camera(self):
        self.camera_thread.stop()
        self.camera_thread.wait()
    
    def start_camera(self):
        self.camera_thread = CameraThread()
        self.camera_thread.frame_ready.connect(self.display_frame)
        self.camera_thread.start()
    
# Register Window ###########################################################################################################
class RegisterWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.ui = Ui_RegisterWindow()
        self.ui.setupUi(self)
        
        # Connect button function ------------------------------------------------
        self.ui.Back_button.clicked.connect(self.back_to_main_window) # Back
        self.ui.BrowseButton.clicked.connect(self.browse_file) # Browse files
        self.ui.SaveButton.clicked.connect(self.save_data) # Save to database
        self.ui.TakePictureButton.clicked.connect(self.switch_to_register_cam_window) # Switch to Register Cam Window
        
    # Back to main window ----------------------------------------------------
    def back_to_main_window(self):
        self.parent().show() 
        self.close()  
        self.parent().start_camera()
    
    # Switch to Register Cam Window --------------------------------------------
    def switch_to_register_cam_window(self):
        self.register_cam_window = RegisterCamWindow(self)
        self.register_cam_window.show()
        self.hide()  
        
    # Browse file --------------------------------------------------------
    def browse_file(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "選擇檔案", "", "所有檔案 (*);;圖像檔案 (*.jpg *.jpeg *.png)", options=options)
        if file_name:
            self.ui.image_path_textEdit.setPlainText(file_name)
    
    # Save to database ----------------------------------------------------------
    def save_data(self):
        user_name = self.ui.Name_textEdit.toPlainText()
        image_path = self.ui.image_path_textEdit.toPlainText()
        print(f"Name: {user_name}, Image Path: {image_path}")
        img_bgr = cv2.imread(image_path, cv2.IMREAD_COLOR)
        register_into_database(user_name,img_bgr,self)

        self.back_to_main_window() 

# Register Cam Window ###########################################################################################################
class RegisterCamWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.ui = UI_RegisterCamWindow()
        self.ui.setupUi(self)
        
        # Connect button function ------------------------------------------------
        self.ui.BackButton.clicked.connect(self.back_to_register_window) # 返回
        self.ui.TakeButton.clicked.connect(self.take_a_picture)
        self.ui.SaveButton.clicked.connect(self.save_picture) 
        self.ui.SaveButton.setEnabled(False)


        # Connect to camera ---------------------------------------------------------
        self.camera_thread = CameraThread()
        self.camera_thread.raw_frame_ready.connect(self.display_raw_frame)
        self.camera_thread.start()
        
        # To store the current frame
        self.current_frame = None  

    # Push Take button ------------------------------------------------------------
    def take_a_picture(self):
        self.current_frame = self.camera_thread.current_frame
        self.stop_camera()

        self.ui.SaveButton.setEnabled(True)
        self.ui.TakeButton.setText("Retake")
        self.ui.TakeButton.clicked.disconnect()
        self.ui.TakeButton.clicked.connect(self.retake_a_picture)
    
    # Retake a picture --------------------------------------------------------------
    def retake_a_picture(self):
        self.start_camera()
        self.ui.SaveButton.setEnabled(False)
        self.ui.TakeButton.setText("Take")
        self.ui.TakeButton.clicked.disconnect()
        self.ui.TakeButton.clicked.connect(self.take_a_picture)

    # Save to database ----------------------------------------------------
    def save_picture(self):
        user_name = self.ui.Name_textEdit.toPlainText()
        register_into_database(user_name,self.current_frame,self)
        self.back_to_main_window() 

    # Back to Main windows-------------------------------------------------------------
    def back_to_main_window(self):
        self.parent().parent().show()  
        self.close()
        self.parent().close()
        self.parent().parent().start_camera()
    
    
    # Display ----------------------------------------------------------------
    def display_raw_frame(self, frame):
        self.camera_thread.current_frame = frame
        h, w, ch = frame.shape
        bytes_per_line = ch * w
        qt_img = QtGui.QImage(frame.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(qt_img)
        current_size = self.ui.CameraView.size()
        scaled_pixmap = pixmap.scaled(current_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        if self.ui.CameraView.pixmap() is None:
            self.ui.CameraView.setScaledContents(False) 
            self.ui.CameraView.setMinimumSize(1, 1)  
        self.ui.CameraView.setAlignment(QtCore.Qt.AlignCenter)
        self.ui.CameraView.setPixmap(scaled_pixmap)
    
    #  Back to Register Window ---------------------------------------------------
    def back_to_register_window(self):
        self.parent().show()
        self.close()  
        self.stop_camera()

    # Control camera ---------------------------------------------------------
    def stop_camera(self):
        self.camera_thread.stop()
        self.camera_thread.wait()   
    def start_camera(self):
        self.camera_thread = CameraThread()
        self.camera_thread.raw_frame_ready.connect(self.display_raw_frame)
        self.camera_thread.start() 
# Camera Thread ============================================================================================
class CameraThread(QtCore.QThread):
    frame_ready = QtCore.pyqtSignal(np.ndarray)
    raw_frame_ready = QtCore.pyqtSignal(np.ndarray)
    def __init__(self):
        super().__init__()
        self.running = True
    # Face recognition -----------------------------------------------------
    def run(self):
        global name
        # Using computer camera test
        # cap = cv2.VideoCapture(0)  
        # if not cap.isOpened():
        #     print("Error: Could not open camera.")
        #     return
        threshold = 1.05
        while self.running: 
            try:
                data, IP = s.recvfrom(100000) # Receive data from esp32cam
                bytes_stream = io.BytesIO(data)
                image = Image.open(bytes_stream)
                img = np.asarray(image)
                name, img_bgr = recognition(img, threshold)
                self.frame_ready.emit(img_bgr)
                self.raw_frame_ready.emit(img)
            except:
                pass
            
            # Using computer camera test
            # ret, frame = cap.read()
            # if not ret:
            #     print("Error: Could not read frame.")
            #     break
        # cap.release()

    def stop(self):
        self.running = False
        self.wait()

# Main cade =======================================================================================
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = FaceRecognitionApp()
    window.show()
    sys.exit(app.exec_())

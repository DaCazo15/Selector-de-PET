import numpy as np
import cv2, time
from tensorflow import keras
import os
import serial
from config import *
import customtkinter as ctk
from PIL import Image, ImageTk
import sys

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
if hasattr(sys, '_MEIPASS'):
    DIR_PATH = sys._MEIPASS
else:
    DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# Inicializa conexión con Arduino
try:
    arduino = serial.Serial(port=COM, baudrate=BAUDRATE, timeout=TIMEOUT)
except serial.SerialException as e:
    print(f"Error al conectar con Arduino: {e}")
    exit()

class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Layout principal usando grid para proporciones 80/20
        self.main_frame = ctk.CTkFrame(window, fg_color="#23272f")
        self.main_frame.pack(fill="both", expand=True)
        self.main_frame.grid_columnconfigure(0, weight=8)
        self.main_frame.grid_columnconfigure(1, weight=2)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Frame de video (80%)
        self.video_frame = ctk.CTkFrame(self.main_frame, fg_color="#23272f")
        self.video_frame.grid(row=0, column=0, sticky="nsew", padx=(20, 10), pady=20)
        self.video_label = ctk.CTkLabel(self.video_frame, text="")
        self.video_label.pack(fill="both", expand=True, padx=10, pady=10)

        # Barra lateral de información (20%)
        self.info_frame = ctk.CTkFrame(self.main_frame, fg_color="#181a1b")
        self.info_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 20), pady=20)
        self.title_label = ctk.CTkLabel(
            self.info_frame,
            text="Resultados IA",
            font=ctk.CTkFont("Arial", 16, "bold"),
            text_color="#00bfff"
        )
        self.title_label.pack(pady=(20, 20))

        self.result_labels = []
        for i in range(3):
            lbl = ctk.CTkLabel(
                self.info_frame,
                text="",
                font=ctk.CTkFont("Arial", 13, "bold"),
                fg_color="#23272f",
                text_color="white",
                width=120,
                height=35,
                corner_radius=8
            )
            lbl.pack(pady=10, padx=10, fill="x")
            self.result_labels.append(lbl)

        self.close_button = ctk.CTkButton(
            self.info_frame,
            text="Cerrar",
            font=ctk.CTkFont("Arial", 13, "bold"),
            fg_color="#ff5555",
            hover_color="#ff8888",
            command=self.on_closing,
            width=100,
        )
        self.close_button.pack(pady=40)

        # Carga etiquetas de clases
        labels_path = f"{DIR_PATH}/keras/labels.txt"
        with open(labels_path, 'r') as labelsfile:
            self.classes = [line.split(' ', 1)[1].rstrip() for line in labelsfile]

        # Carga modelo de IA
        model_path = f"{DIR_PATH}/keras/keras_model.h5"
        self.model = keras.models.load_model(model_path, compile=False)

        # Configura cámara (alta calidad)
        self.cap = cv2.VideoCapture(1)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_GAIN, 0)

        # Umbral de confianza
        self.conf_threshold = CONFIANZA
        self.running = True
        self.ready_to_send = True  # Solo puedes enviar si es True
        self.update()

    def update(self):
        if not self.running:
            return
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            resized_img = cv2.resize(frame, (224, 224))
            model_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
            data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
            normalized_image_array = (model_img.astype(np.float32) / 127.0) - 1
            data[0] = normalized_image_array
            predictions = self.model.predict(data, verbose=0)

            confs = [int(predictions[0][i]*100) for i in range(len(self.classes))] 
            max_conf = max(confs)#
            for i, label in enumerate(self.classes):
                color = "#44ff44" if confs[i] == max_conf and confs[i] > self.conf_threshold else "white"
                self.result_labels[i].configure(
                    text=f"{label}: {confs[i]}%",
                    text_color=color
                )

            # Lee la respuesta de Arduino
            if arduino.in_waiting:
                respuesta = arduino.read()
                if respuesta == b'0':
                    self.ready_to_send = True

            # Solo envía si está listo para enviar
            max_class = self.classes[confs.index(max_conf)] 
            if max_conf > self.conf_threshold: 
                if self.ready_to_send:
                    num = 0
                    if max_class == "Pet":
                        num = 1
                    elif max_class == "No pet":
                        num = 0
                    elif max_class == "Nada":
                        num = 0

                    arduino.write((str(num) + '\n').encode())

                    if num == 1:
                        self.ready_to_send = False  # Espera respuesta de Arduino antes de volver a enviar

            # Muestra el frame en customtkinter usando ImageTk.PhotoImage
            label_width = self.video_label.winfo_width()
            label_height = self.video_label.winfo_height()
            if label_width < 10 or label_height < 10:
                label_width = LABEL_WIDTH
                label_height = LABEL_HEIGHT
            frame_resized = cv2.resize(frame, (label_width, label_height))
            img = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            im_pil = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=im_pil)
            self.video_label.imgtk = imgtk  # Previene que Python lo elimine
            self.video_label.configure(image=imgtk)
        self.window.after(UPDATE_FRAME, self.update)

    def on_closing(self):
        self.running = False
        self.cap.release()
        self.window.destroy()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    if hasattr(sys, '_MEIPASS'):
        # Ejecutable PyInstaller
        ICON_PATH = os.path.join(sys._MEIPASS, "icon.ico")
    else:
        # Ejecución normal
        ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icon.ico")
    root = ctk.CTk()
    root.geometry("1080x580+100+50")
    try:
        root.iconbitmap(ICON_PATH)
    except Exception as e:
        print("No se pudo cargar el icono en la ventana:", e)
    app = App(root, NAME_APP)
    root.mainloop()
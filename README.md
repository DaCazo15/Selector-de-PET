<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="https://i.postimg.cc/PrRfhrLh/Diseno-sin-titulo-removebg-preview.png" alt="Project logo"></a>
</p>

<h1 align="center"> B-28</h1>

# Selector Inteligente de PET para Reciclaje

**Proyecto desarrollado para la World Robot Olympiad (WRO) 2025, categoría "Future Innovators".**

---

> "B-28" es un sistema autónomo que utiliza inteligencia artificial para identificar y clasificar botellas de plástico PET, optimizando el primer paso crucial de la cadena de reciclaje para la creación de filamento de impresión 3D.


---

## 🌍 El Desafío: Contaminación Plástica

El plástico PET, aunque 100% reciclable, a menudo termina en vertederos debido a procesos de selección ineficientes y costosos. La contaminación de los lotes de PET con otros materiales disminuye drásticamente la calidad del producto reciclado. Un reciclaje efectivo comienza con una clasificación precisa.

## 🤖 Nuestra Solución: B-28

**B-28** (nombre código del proyecto) es un prototipo funcional que automatiza la clasificación de botellas PET. Utilizando visión por computadora y un modelo de aprendizaje profundo, el sistema analiza objetos en tiempo real, distingue las botellas PET de otros desechos y activa un mecanismo de separación.

Este proyecto no solo representa una solución tecnológica a un problema ambiental, sino que también demuestra el poder de la IA y la robótica para crear un futuro más sostenible.

### ✨ Interfaz de Usuario

El sistema cuenta con una interfaz gráfica de usuario desarrollada con CustomTkinter que permite monitorear en tiempo real la cámara, ver las predicciones del modelo de IA y el estado del sistema.

---

## 🚀 Características Principales

-   **Clasificación Inteligente:** Utiliza un modelo de red neuronal (entrenado con la plataforma **Teachable Machine de Google** y exportado a formato Keras) para lograr una identificación precisa de objetos con una confianza superior al 85%.
-   **Procesamiento en Tiempo Real:** Analiza el video de una cámara en vivo para tomar decisiones instantáneas.
-   **Actuación Robótica:** Se comunica con una placa Arduino para controlar un servomotor que desvía físicamente las botellas PET.
-   **Comunicación Bidireccional:** Implementa un protocolo de comunicación serial robusto donde el sistema principal espera una confirmación del Arduino antes de procesar el siguiente objeto, evitando errores de saturación.
-   **Interfaz de Monitoreo:** Incluye una GUI de escritorio que muestra la vista de la cámara y las probabilidades de clasificación en tiempo real.
-   **Independiente y portable:** El proyecto puede ser compilado en un único archivo ejecutable `.exe`, facilitando su despliegue en cualquier sistema Windows.

---

## 🛠️ Arquitectura del Sistema

El proyecto integra software y hardware en un flujo de trabajo cohesivo:

1.  **Captura de Imagen (Cámara Web):** Una cámara captura el video de los objetos que pasan por la banda transportadora.
2.  **Procesamiento y Clasificación (Python / TensorFlow Lite):**
    -   El script principal en Python toma los fotogramas del video.
    -   Cada fotograma se procesa y se pasa al modelo de Keras (`.h5`).
    -   El modelo clasifica el objeto en una de tres categorías: `Pet`, `No Pet`, o `Nada`.
3.  **Toma de Decisión (Python):**
    -   Si se detecta "Pet" con alta confianza, el script envía el comando `"1"` al Arduino.
    -   En caso contrario, envía `"0"`.
4.  **Actuación Mecánica (Arduino):**
    -   El Arduino recibe la señal a través del puerto serial.
    -   Si la señal es `"1"`, activa un servomotor para desviar la botella.
    -   Tras completar la acción, el Arduino envía una señal de "listo" (`"0"`) de vuelta al script de Python para procesar el siguiente objeto.

---

## ⚙️ Stack Tecnológico

### Software
-   **Lenguaje Principal:** Python 3.9+
-   **Inteligencia Artificial:** TensorFlow, Keras
-   **Visión por Computadora:** OpenCV
-   **GUI:** CustomTkinter, PIL (Pillow)
-   **Comunicación Hardware:** PySerial
-   **Controlador de Hardware:** Arduino (C++)

### Hardware
| Componente       | Función                                  |
|------------------|------------------------------------------|
| Cámara Web       | Captura de imágenes en tiempo real.      |
| Arduino Nano     | Controlador para el mecanismo de sorting.|
| Servomotor MG996 | Actuador para desviar las botellas PET.  |
| Computadora      | Ejecuta el programa principal en Python. |

---

## 🔧 Instalación y Puesta en Marcha

### Prerrequisitos
-   Python 3.9 o superior.
-   Tener el IDE de Arduino para cargar el sketch en la placa.

### 1. Clonar el Repositorio
```bash
git clone https://github.com/Dcazorla/Selector-de-PET.git
cd Selector-de-PET
```

### 2. Instalar Dependencias de Python
El proyecto requiere las siguientes librerías. Puedes instalarlas usando `pip`:
```bash
pip install numpy opencv-python tensorflow pillow pyserial customtkinter
```

### 3. Configurar el Hardware
1.  Conecta la cámara web a tu computadora.
2.  Carga el código de `src/Communication.ino` a tu placa Arduino Nano.
3.  Conecta el servomotor al pin digital y a la alimentación correspondientes según el código del Arduino.
4.  Conecta el Arduino a la computadora. El script de Python detectará automáticamente el puerto COM disponible.

### 4. Ejecutar la Aplicación
Para iniciar el sistema, simplemente ejecuta el script `main.py`:
```bash
python main.py
```
La interfaz de usuario se abrirá y el sistema comenzará a clasificar los objetos que muestres a la cámara.

---

## 📦 Compilar como Ejecutable (Opcional)

Puedes empaquetar toda la aplicación en un solo archivo `.exe` para una fácil distribución en sistemas Windows usando PyInstaller.

Desde la raíz del proyecto, ejecuta el siguiente comando:
```bash
pyinstaller --onefile --noconsole --icon=icon.ico --add-data "keras;keras" --name="Selector de PET" main.py
```
El ejecutable se encontrará en la carpeta `dist`.

---

## 🏆 Sobre la Competencia

La **World Robot Olympiad (WRO)** es una competencia global que inspira a los jóvenes a interesarse por la ciencia y la tecnología. La categoría **Future Innovators** desafía a los equipos a desarrollar proyectos robóticos innovadores que resuelvan problemas del mundo real.

---

## 👥 Equipo

* **Alberto Medina** - Desarrollador Principal
*   **Ing. Daniel Cazorla** - Colaborador

---

## 📜 Licencia

Este proyecto está bajo la Licencia MIT.

**Contacto:** `Dcazorla.0190@gmail.com`

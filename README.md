# Selector de PET con IA y Arduino  

---

## 📌 Descripción del Proyecto  
Sistema inteligente que clasifica botellas de plástico PET usando visión por computadora (IA) y las separa automáticamente mediante un mecanismo controlado por Arduino. Las botellas seleccionadas se destinan a reciclaje para producir filamento de impresión 3D.  

---

## ⚙️ Funcionamiento  
### 1. Clasificación con IA  
Modelo entrenado en **Teachable Machine** con 3 clases:  
- ✅ **PET** (botella válida) → Envía señal `"1"` por serial  
- ❌ **No PET** (objeto no válido) → Ignora  
- 🚫 **Nada** (fondo vacío) → No actúa  

### 2. Control con Arduino  
Al recibir `"1"`, el **Arduino Nano** activa un servomotor para abrir una compuerta, permitiendo el paso de la botella al área de procesamiento.  

---

## 🛠️ Componentes  
### Hardware  
| Componente       | Función                                  |  
|------------------|------------------------------------------|  
| Cámara web       | Captura imágenes en tiempo real          |  
| Arduino Nano     | Control del servo mediante señal serial  |  
| Servo MG996 | Mecanismo de apertura de compuerta       |  

### Software  
- **Python** + **TensorFlow Lite** (para inferencia del modelo)  
- **Código Arduino** (procesamiento de señales seriales)  

---

## 🎯 Resultados Esperados
- Botellas PET: Clasificadas correctamente y depositadas en el contenedor

- No PET/Nada: Ignoradas sin activar el servo

##n🔮 Futuras Mejoras
- Mejora	Impacto
- Contador de botellas procesadas	Monitoreo de eficiencia
- Sensor de peso	Medición de material acumulado
- Trituradora integrada	Automatización completa del reciclaje

## 📜 Licencia
MIT © Ing. Daniel Cazorla / Dcazorla.0190@gmail.com

# 🤖 CHATBOT ADMINISTRATIVO CON IA - ZOOTEC

## ✅ TODO EN UN SOLO CHAT

El chatbot responde **consultas simples + predicciones** en la misma interfaz conversacional.

---

## 🚀 INICIO RÁPIDO (3 pasos)

### **1. Instalar e iniciar el Chatbot IA:**

```bash
cd C:\Users\User\Desktop\ZOOTEC-IA

# Instalar dependencias
pip install -r requirements.txt

# Iniciar chatbot
python chatbot.py
```

Debe mostrar:

```
🤖 Iniciando Chatbot IA de ZOOTEC...
📍 URL: http://localhost:8000
📖 Docs: http://localhost:8000/docs
```

---

### **2. Agregar el componente en el Dashboard Angular:**

```typescript
// dashboard.component.ts
import { ChatbotComponent } from '../../shared/chatbot/chatbot.component';

@Component({
  // ... tus imports existentes
  imports: [...tusImportsActuales, ChatbotComponent],
})
```

```html
<!-- dashboard.component.html -->
<!-- Al FINAL del archivo, agregar: -->
<app-chatbot></app-chatbot>
```

---

### **3. Iniciar Backend + Frontend:**

```bash
# Terminal 1: Backend Java
cd C:\Users\User\Desktop\zzootec\admin
mvnw spring-boot:run

# Terminal 2: IA Chatbot (ya lo iniciaste en paso 1)

# Terminal 3: Frontend Angular
cd C:\Users\User\Desktop\zzootec-front\zzootec-admin
npm start
```

---

## 💬 CÓMO USAR EL CHAT

### **Preguntas que puedes hacer:**

#### 📦 Stock:

```
"¿Cuánto stock hay de alimento premium?"
"¿Qué productos tienen stock bajo?"
"Muestra el inventario"
```

#### 📊 Predicciones:

```
"¿Cuándo se agotará el alimento?"
"¿Debo reponer los collares?"
```

#### 💰 Ventas:

```
"¿Cuántas ventas hubo hoy?"
"Muestra los productos más vendidos"
```

#### ❓ Ayuda:

```
"ayuda"
```

---

## 🎯 EJEMPLO CONVERSACIÓN REAL

```
👤 Usuario: "Hola"
🤖 Bot: "¡Hola! 👋 Soy el asistente inteligente de ZOOTEC.
        ¿En qué puedo ayudarte?"

👤 Usuario: "¿Cuánto stock hay de alimento premium?"
🤖 Bot: "📦 Alimento Premium
        • Stock actual: 45 unidades
        • Precio: S/ 89.90
        ¿Necesitas saber cuándo se agotará?"

👤 Usuario: "Sí"
🤖 Bot: "📊 Predicción para Alimento Premium
        • Stock actual: 45 unidades
        • 🟡 PLANIFICAR Se agotará en: ~9 días
        • Recomendación: Planificar compra de 150 unidades"

👤 Usuario: "¿Qué productos tienen stock bajo?"
🤖 Bot: "⚠️ Productos con Stock Bajo (3)
        1. Collar antiparasitario: 2 unidades
        2. Shampoo perros: 4 unidades
        3. Arena gatos: 3 unidades"
```

---

## 🎨 INTERFAZ

El componente aparece como un **botón flotante** en la esquina inferior derecha:

```
┌─────────────────────────┐
│  🤖 Asistente IA  ●     │  ← Click aquí
└─────────────────────────┘
```

Al hacer click, se abre la ventana de chat completa.

---

## 🔧 TECNOLOGÍA

### Backend IA:

- **FastAPI** (Python)
- **Procesamiento de Lenguaje Natural** (pattern matching)
- **Algoritmos de predicción** (análisis de tendencias)
- **Integración con backend Spring Boot**

### Frontend:

- **Angular standalone component**
- **RxJS** para manejo de streams
- **Servicio dedicado** (chatbot.service.ts)
- **UI moderna** con animaciones

---

## 📊 PARA TU TESIS

### ¿Es IA real?

✅ **SÍ**

- Procesamiento de Lenguaje Natural
- Reconocimiento de intenciones
- Predicción de agotamiento de stock
- Análisis de tendencias
- Recomendaciones automáticas basadas en datos

### ¿Es innovador?

✅ **SÍ**

- Chat conversacional != CRUD tradicional
- Combina consultas + predicciones en una sola interfaz
- Aplica algoritmos de análisis de datos
- Interfaz natural para usuarios administrativos

---

## 🐛 TROUBLESHOOTING

### "Error al conectar con el backend"

✅ Verifica que Spring Boot esté corriendo en `localhost:8080`

### "No puedo ver el chatbot en Angular"

✅ Verifica que importaste `ChatbotComponent` en tu dashboard

### "El bot no responde"

✅ Verifica que `python chatbot.py` esté corriendo en `localhost:8000`

### "Las predicciones son incorrectas"

✅ Por ahora usa datos simulados - conecta con ventas reales del backend

---

## 🚀 PRÓXIMAS MEJORAS (Opcional)

1. **NLP Avanzado**: Usar transformers (BERT, GPT-2)
2. **Predicción precisa**: Conectar con datos reales de ventas
3. **Aprendizaje**: Guardar historial y mejorar respuestas
4. **Multilenguaje**: Responder en español/inglés
5. **Voz**: Agregar reconocimiento de voz

---

## ✅ CHECKLIST DE INTEGRACIÓN

- [ ] Backend Java corriendo (localhost:8080)
- [ ] Chatbot IA corriendo (localhost:8000)
- [ ] Frontend Angular corriendo (localhost:4200)
- [ ] Componente `<app-chatbot>` agregado al dashboard
- [ ] Probar preguntas de ejemplo
- [ ] Ver predicciones funcionando

---

**¿Listo para probar?** Ejecuta los 3 comandos y empieza a chatear 🤖💬

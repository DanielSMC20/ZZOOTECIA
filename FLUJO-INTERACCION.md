# 🔄 FLUJO DE INTERACCIÓN: IA ↔ BACKEND

## 📊 Arquitectura del Sistema

```
┌─────────────────┐
│   USUARIO       │
│   (Dashboard)   │
└────────┬────────┘
         │
         │ "¿Cuánto stock hay de alimento?"
         ▼
┌─────────────────────────────────────────┐
│  FRONTEND ANGULAR (localhost:4200)      │
│  ┌───────────────────────────────────┐  │
│  │  ChatbotComponent                 │  │
│  │  - Captura mensaje del usuario    │  │
│  │  - Muestra respuesta del bot      │  │
│  └──────────────┬────────────────────┘  │
│                 │                        │
│  ┌──────────────▼────────────────────┐  │
│  │  ChatbotService                   │  │
│  │  - sendMessage(message)           │  │
│  │  - Gestiona historial de chat    │  │
│  └──────────────┬────────────────────┘  │
└─────────────────┼────────────────────────┘
                  │
                  │ HTTP POST /api/chat
                  │ { message: "¿Cuánto stock hay de alimento?" }
                  ▼
┌─────────────────────────────────────────┐
│  IA PYTHON (localhost:8000)             │
│  chatbot.py                             │
│  ┌───────────────────────────────────┐  │
│  │ FastAPI Endpoint: /api/chat       │  │
│  │ 1. Recibe mensaje del usuario     │  │
│  └──────────────┬────────────────────┘  │
│                 │                        │
│  ┌──────────────▼────────────────────┐  │
│  │ detect_intent(message)            │  │
│  │ - Analiza el texto                │  │
│  │ - Identifica intención            │  │
│  │ → "consulta_stock"                │  │
│  └──────────────┬────────────────────┘  │
│                 │                        │
│                 │ ¿Qué datos necesito?  │
│                 │ → Productos del backend│
│                 ▼                        │
│  ┌───────────────────────────────────┐  │
│  │ get_all_products()                │  │
│  │ - Hace HTTP GET a backend         │  │
│  └──────────────┬────────────────────┘  │
└─────────────────┼────────────────────────┘
                  │
                  │ HTTP GET /api/admin/products
                  ▼
┌─────────────────────────────────────────┐
│  BACKEND JAVA (localhost:8080)          │
│  Spring Boot                            │
│  ┌───────────────────────────────────┐  │
│  │ ProductController                 │  │
│  │ @GetMapping("/api/admin/products")│  │
│  └──────────────┬────────────────────┘  │
│                 │                        │
│  ┌──────────────▼────────────────────┐  │
│  │ ProductService                    │  │
│  │ - getAll()                        │  │
│  └──────────────┬────────────────────┘  │
│                 │                        │
│  ┌──────────────▼────────────────────┐  │
│  │ MySQL Database                    │  │
│  │ SELECT * FROM products            │  │
│  └──────────────┬────────────────────┘  │
│                 │                        │
│                 │ [{ id: 1, name: "Alimento Premium",│
│                 │    stock: 45, price: 89.90 }, ...]│
│                 ▼                        │
│  ┌───────────────────────────────────┐  │
│  │ Retorna JSON                      │  │
│  │ Response: 200 OK                  │  │
│  └──────────────┬────────────────────┘  │
└─────────────────┼────────────────────────┘
                  │
                  │ [productos...]
                  ▼
┌─────────────────────────────────────────┐
│  IA PYTHON (localhost:8000)             │
│  ┌───────────────────────────────────┐  │
│  │ handle_consulta_stock()           │  │
│  │ 1. Busca "alimento" en productos  │  │
│  │ 2. Encuentra match                │  │
│  │ 3. Extrae datos relevantes        │  │
│  └──────────────┬────────────────────┘  │
│                 │                        │
│  ┌──────────────▼────────────────────┐  │
│  │ Genera respuesta formateada       │  │
│  │ "📦 **Alimento Premium**          │  │
│  │  • Stock: 45 unidades             │  │
│  │  • Precio: S/ 89.90"              │  │
│  └──────────────┬────────────────────┘  │
│                 │                        │
│                 │ ChatResponse          │
│                 ▼                        │
│  ┌───────────────────────────────────┐  │
│  │ Retorna JSON                      │  │
│  │ {                                 │  │
│  │   response: "📦 Alimento...",     │  │
│  │   intent: "consulta_stock",       │  │
│  │   data: {...}                     │  │
│  │ }                                 │  │
│  └──────────────┬────────────────────┘  │
└─────────────────┼────────────────────────┘
                  │
                  │ Response JSON
                  ▼
┌─────────────────────────────────────────┐
│  FRONTEND ANGULAR                       │
│  ┌───────────────────────────────────┐  │
│  │ ChatbotService                    │  │
│  │ - Recibe respuesta                │  │
│  │ - Agrega al historial             │  │
│  └──────────────┬────────────────────┘  │
│                 │                        │
│  ┌──────────────▼────────────────────┐  │
│  │ ChatbotComponent                  │  │
│  │ - Muestra mensaje en UI           │  │
│  │ - Formatea con markdown           │  │
│  └──────────────┬────────────────────┘  │
└─────────────────┼────────────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │   USUARIO       │
         │   Ve respuesta  │
         └─────────────────┘
```

---

## 🔍 EJEMPLO DETALLADO: "¿Cuánto stock hay de alimento?"

### **PASO 1: Usuario escribe en el chat**

```typescript
// ChatbotComponent
sendMessage() {
  this.chatbotService.sendMessage("¿Cuánto stock hay de alimento?")
}
```

---

### **PASO 2: Service envía a IA**

```typescript
// ChatbotService
sendMessage(message: string): Observable<ChatResponse> {
  return this.http.post('http://localhost:8000/api/chat', {
    message: "¿Cuánto stock hay de alimento?"
  });
}
```

---

### **PASO 3: IA detecta intención**

```python
# chatbot.py
def detect_intent(message: str):
    message = message.lower()  # "¿cuánto stock hay de alimento?"

    if 'stock' in message and 'cuanto' in message:
        return 'consulta_stock'  # ✅ Detectado
```

---

### **PASO 4: IA solicita datos al backend**

```python
def get_all_products():
    # Hace HTTP GET al backend Java
    response = requests.get("http://localhost:8080/api/admin/products")
    return response.json()
    # Retorna: [
    #   { id: 1, name: "Alimento Premium", stock: 45, price: 89.90 },
    #   { id: 2, name: "Collar", stock: 12, price: 25.00 },
    #   ...
    # ]
```

---

### **PASO 5: Backend consulta base de datos**

```java
// ProductController.java
@GetMapping("/api/admin/products")
public List<ProductResponseDto> getAll() {
    return productService.getAll();  // SELECT * FROM products
}
```

```sql
-- MySQL ejecuta:
SELECT id, name, stock, price, category_id, brand_id, image_url
FROM products
WHERE deleted = false;
```

---

### **PASO 6: IA procesa y busca el producto**

```python
def extract_product_name(message: str, products: list):
    # Busca "alimento" en los productos
    for product in products:
        if "alimento" in product['name'].lower():
            return product  # ✅ Encuentra "Alimento Premium"
    return None

# Resultado:
# { id: 1, name: "Alimento Premium", stock: 45, price: 89.90 }
```

---

### **PASO 7: IA formatea respuesta**

```python
def handle_consulta_stock(message: str, products: list):
    product = extract_product_name(message, products)

    response = f"""📦 **{product['name']}**

• Stock actual: **{product['stock']} unidades**
• Precio: **S/ {product['price']:.2f}**

¿Necesitas saber cuándo se agotará? Pregúntame: '¿Cuándo se agotará?'"""

    return ChatResponse(
        response=response,
        intent="consulta_stock",
        data={"product": product}
    )
```

---

### **PASO 8: IA retorna JSON a Angular**

```json
{
  "response": "📦 **Alimento Premium**\n\n• Stock actual: **45 unidades**\n• Precio: **S/ 89.90**\n\n¿Necesitas saber cuándo se agotará?",
  "intent": "consulta_stock",
  "data": {
    "product": {
      "id": 1,
      "name": "Alimento Premium",
      "stock": 45,
      "price": 89.9
    }
  }
}
```

---

### **PASO 9: Angular muestra en UI**

```typescript
// ChatbotComponent
this.chatbotService.sendMessage(message).subscribe({
  next: (response) => {
    // Agrega mensaje al chat
    this.messages.push({
      message: response.response, // El texto formateado
      isUser: false,
      timestamp: new Date(),
    });
  },
});
```

---

## 🚀 FLUJOS ADICIONALES

### **A. Predicción (requiere análisis de ventas):**

```
Usuario: "¿Cuándo se agotará el alimento?"
    ↓
IA pide productos → Backend retorna productos
IA pide ventas → Backend retorna ventas
    ↓
IA calcula: 45 unidades ÷ 5 ventas/día = 9 días
    ↓
Respuesta: "Se agotará en ~9 días"
```

---

### **B. Stock bajo (filtrado en backend):**

```
Usuario: "¿Qué tiene stock bajo?"
    ↓
IA llama: GET /api/admin/products/low-stock?threshold=10
    ↓
Backend: SELECT * FROM products WHERE stock < 10
    ↓
IA formatea: "3 productos con stock bajo: ..."
```

---

### **C. Ventas del día:**

```
Usuario: "¿Cuántas ventas hubo hoy?"
    ↓
IA llama: GET /api/sales/daily-report
    ↓
Backend calcula métricas del día
    ↓
IA formatea: "Hoy: 12 ventas, S/ 3,450.00"
```

---

## 🔐 SEGURIDAD ACTUAL

**Sin autenticación entre IA y Backend:**

```python
# IA hace peticiones sin token
requests.get("http://localhost:8080/api/admin/products")
# ✅ Funciona porque /api/admin/products/** está en .permitAll()
```

**Configurado en SecurityConfig.java:**

```java
.requestMatchers("/api/admin/products/**").permitAll()
.requestMatchers("/api/sales/**").permitAll()
```

---

## ⚡ VENTAJAS DE ESTA ARQUITECTURA

1. **Separación de responsabilidades:**
   - Backend = Datos (Java)
   - IA = Inteligencia (Python)
   - Frontend = Interfaz (Angular)

2. **IA accede a datos reales:**
   - No tiene datos hardcodeados
   - Siempre consulta al backend
   - Información actualizada

3. **Escalable:**
   - Puedes agregar más intenciones
   - Mejorar algoritmos de IA sin tocar backend
   - Backend sigue igual

4. **Reutilizable:**
   - Mismos endpoints para dashboard y chatbot
   - IA puede llamar cualquier API del backend

---

## 🎯 RESUMEN TÉCNICO

| Componente     | Tecnología           | Puerto | Rol                              |
| -------------- | -------------------- | ------ | -------------------------------- |
| **Frontend**   | Angular + TypeScript | 4200   | Interfaz de usuario              |
| **Chatbot IA** | Python + FastAPI     | 8000   | Procesamiento NLP + Predicciones |
| **Backend**    | Java + Spring Boot   | 8080   | API REST + Lógica de negocio     |
| **Database**   | MySQL                | 3306   | Persistencia de datos            |

**Flujo resumido:**

```
Usuario → Angular → IA → Backend → MySQL → Backend → IA → Angular → Usuario
```

---

¿Alguna parte del flujo necesitas que explique con más detalle? 🚀

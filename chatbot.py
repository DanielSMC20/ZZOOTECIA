"""
CHATBOT ADMINISTRATIVO CON IA - ZOOTEC
Sistema de Gestion de Ventas Omnicanal - Ica, 2025

Chatbot inteligente que responde consultas y hace predicciones
Todo en una sola interfaz conversacional
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import re
import requests
from datetime import datetime, timedelta

app = FastAPI(title="ZOOTEC IA Chatbot")

# CORS para Angular
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL del backend
import os
from dotenv import load_dotenv

# Cargar variables de entorno locales
load_dotenv()

# URL del backend (puede configurarse en .env)
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8080")


# ============================================
# MODELOS
# ============================================

class ChatMessage(BaseModel):
    message: str
    user_id: Optional[str] = "admin"

class ChatResponse(BaseModel):
    response: str
    intent: str
    data: Optional[dict] = None


# ============================================
# FUNCIONES AUXILIARES
# ============================================

def get_all_products():
    """Obtiene todos los productos del backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/admin/products", timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error al obtener productos: {e}")
        return []


def get_sales_data():
    """Obtiene datos de ventas del backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/sales", timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error al obtener ventas: {e}")
        return []


def get_low_stock_products(threshold=10):
    """Obtiene productos con stock bajo"""
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/admin/products/low-stock?threshold={threshold}",
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error al obtener stock bajo: {e}")
        return []


def get_categories():
    """Obtiene categorias del backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/admin/categories", timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error al obtener categorias: {e}")
        return []


def get_clients():
    """Obtiene clientes del backend"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/clients", timeout=5)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        print(f"Error al obtener clientes: {e}")
        return []


def normalize_text(text: str) -> str:
    """Normaliza texto para comparaciones simples."""
    if not text:
        return ""
    normalized = text.lower().strip()
    replacements = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u",
        "à": "a", "è": "e", "ì": "i", "ò": "o", "ù": "u",
        "ä": "a", "ë": "e", "ï": "i", "ö": "o", "ü": "u",
        "ñ": "n"
    }
    for src, dst in replacements.items():
        normalized = normalized.replace(src, dst)
    return normalized


# ============================================
# PROCESAMIENTO DE LENGUAJE NATURAL
# ============================================

def detect_intent(message: str):
    """
    Detecta la intención del usuario usando pattern matching
    (En producción se puede usar NLP más avanzado)
    """
    message = normalize_text(message)
    
    # CONSULTAS DE STOCK / INVENTARIO
    if any(word in message for word in ['stock', 'inventario', 'existencias', 'cuanto', 'cuánto', 'cantidad', 'hay']):
        if any(word in message for word in ['bajo', 'poco', 'crítico', 'alerta']):
            return 'stock_bajo'
        return 'consulta_stock'
    
    # PREDICCIONES
    if any(word in message for word in ['cuándo', 'cuando', 'agotará', 'agotara', 'acabará', 'acabara', 'predicción', 'prediccion']):
        return 'prediccion'
    
    # VENTAS
    if any(word in message for word in ['ventas', 'vendido', 'vendi', 'ingresos']):
        if 'hoy' in message:
            return 'ventas_hoy'
        elif any(word in message for word in ['semana', 'semanal']):
            return 'ventas_semana'
        return 'ventas_general'
    
    # CATEGORIAS
    if any(word in message for word in ['categoria', 'categorias', 'rubro', 'rubros']):
        return 'listar_categorias'

    # ORDENES / PEDIDOS / COMPRAS
    if any(word in message for word in ['orden', 'ordenes', 'pedido', 'pedidos', 'compra', 'compras']):
        if any(word in message for word in ['cliente', 'clientes', 'por cliente', 'del cliente']):
            return 'ordenes_cliente'
        return 'ordenes_general'

    # PRODUCTOS / LISTADO
    if any(word in message for word in ['productos', 'items', 'articulos', 'inventario', 'listar', 'lista', 'muestra', 'ver']):
        if any(word in message for word in ['más', 'mas', 'mejor', 'top']):
            return 'top_productos'
        return 'listar_productos'
    
    # RECOMENDACIONES
    if any(word in message for word in ['comprar', 'reponer', 'reabastecer', 'reposición', 'reposicion']):
        return 'recomendacion_compra'
    
    # AYUDA
    if any(word in message for word in ['ayuda', 'qué puedes', 'que puedes', 'comandos', 'opciones']):
        return 'ayuda'
    
    # SALUDO
    if any(word in message for word in ['hola', 'buenas', 'saludos', 'hey']):
        return 'saludo'
    
    return 'desconocido'


def extract_product_name(message: str, products: list):
    """Extrae el nombre del producto de la consulta"""
    message_lower = message.lower()
    
    for product in products:
        product_name = product.get('name', '').lower()
        if product_name in message_lower:
            return product
    
    return None


def extract_client_from_message(message: str, clients: list):
    """Busca un cliente por nombre y apellidos dentro del mensaje."""
    message_normalized = normalize_text(message)

    best_client = None
    best_score = 0

    for client in clients:
        nombres_raw = client.get('nombres', '')
        apellidos_raw = client.get('apellidos', '')

        nombres = normalize_text(nombres_raw)
        apellidos = normalize_text(apellidos_raw)
        full_name = f"{nombres} {apellidos}".strip()

        if not full_name:
            continue

        score = 0
        if full_name and full_name in message_normalized:
            score += 3

        for token in (nombres.split() if nombres else []):
            if len(token) > 2 and token in message_normalized:
                score += 1

        for token in (apellidos.split() if apellidos else []):
            if len(token) > 2 and token in message_normalized:
                score += 1

        if score > best_score:
            best_score = score
            best_client = client

    return best_client if best_score >= 1 else None


def predict_stock_depletion(product: dict, sales_data: list):
    """
    Predice cuándo se agotará un producto
    Algoritmo simple basado en promedio de ventas
    """
    product_id = product.get('id')
    current_stock = product.get('stock', 0)
    
    # Filtrar ventas del producto (simulado - en tu caso usa la data real)
    # Por ahora usamos un promedio simple
    daily_avg_sales = 5  # Placeholder - calcular de sales_data real
    
    if daily_avg_sales <= 0:
        return {
            'days_until_depleted': 999,
            'recommendation': 'Producto con baja rotación. No requiere reposición inmediata.'
        }
    
    days_until_depleted = int(current_stock / daily_avg_sales)
    
    if days_until_depleted <= 3:
        urgency = '[URGENTE]'
        recommendation = f'Comprar {daily_avg_sales * 30} unidades INMEDIATAMENTE'
    elif days_until_depleted <= 7:
        urgency = '[IMPORTANTE]'
        recommendation = f'Comprar {daily_avg_sales * 30} unidades esta semana'
    elif days_until_depleted <= 15:
        urgency = '[PLANIFICAR]'
        recommendation = f'Planificar compra de {daily_avg_sales * 30} unidades'
    else:
        urgency = '[OK]'
        recommendation = 'Stock suficiente por ahora'
    
    return {
        'days_until_depleted': days_until_depleted,
        'urgency': urgency,
        'recommendation': recommendation
    }


# ============================================
# HANDLERS DE INTENCIONES
# ============================================

def handle_consulta_stock(message: str, products: list):
    """Responde consultas de stock"""
    product = extract_product_name(message, products)
    
    if product:
        stock = product.get('stock', 0)
        name = product.get('name', 'Producto')
        price = product.get('price', 0)
        
        return ChatResponse(
            response=f"**{name}**\n\n• Stock actual: **{stock} unidades**\n• Precio: **S/ {price:.2f}**\n\n¿Necesitas saber cuándo se agotará? Pregúntame: '¿Cuándo se agotará?'",
            intent="consulta_stock",
            data={"product": product}
        )
    else:
        total_stock = sum(p.get('stock', 0) for p in products)
        return ChatResponse(
            response=f"**Stock General**\n\nTotal de productos: **{len(products)}**\nUnidades totales: **{total_stock}**\n\nPara ver un producto especifico, menciona su nombre. Ejemplo: '¿Cuanto stock hay de iPhone 13?'",
            intent="consulta_stock",
            data={"total_products": len(products), "total_stock": total_stock}
        )


def handle_stock_bajo(products: list):
    """Lista productos con stock bajo"""
    low_stock = get_low_stock_products(10)
    
    if not low_stock:
        return ChatResponse(
            response="No hay productos con stock bajo en este momento.",
            intent="stock_bajo",
            data={"count": 0}
        )
    
    response_text = f"**Productos con Stock Bajo** ({len(low_stock)})\n\n"
    
    for i, product in enumerate(low_stock[:10], 1):
        name = product.get('name', 'Producto')
        stock = product.get('stock', 0)
        response_text += f"{i}. **{name}**: {stock} unidades\n"
    
    response_text += f"\nTip: Pregunta '¿Cuándo se agotará [producto]?' para saber cuándo reponer."
    
    return ChatResponse(
        response=response_text,
        intent="stock_bajo",
        data={"products": low_stock}
    )


def handle_prediccion(message: str, products: list, sales_data: list):
    """Predice cuándo se agotará un producto"""
    product = extract_product_name(message, products)
    
    if not product:
        return ChatResponse(
            response="Por favor especifica el producto. Ejemplo: '¿Cuándo se agotará el iPhone 13?'",
            intent="prediccion",
            data=None
        )
    
    prediction = predict_stock_depletion(product, sales_data)
    name = product.get('name')
    stock = product.get('stock', 0)
    
    response_text = f"**Prediccion para {name}**\n\n"
    response_text += f"• Stock actual: {stock} unidades\n"
    response_text += f"• {prediction['urgency']} Se agotará en: **~{prediction['days_until_depleted']} días**\n"
    response_text += f"• Recomendación: {prediction['recommendation']}"
    
    return ChatResponse(
        response=response_text,
        intent="prediccion",
        data={"product": product, "prediction": prediction}
    )


def handle_ventas_hoy(sales_data: list):
    """Muestra ventas de hoy"""
    today = datetime.now().date()
    
    # Simulación - en tu caso filtrar por fecha real
    total_sales = 3450.50
    total_transactions = 12
    
    response_text = f"**Ventas de Hoy** ({today.strftime('%d/%m/%Y')})\n\n"
    response_text += f"• Total vendido: **S/ {total_sales:,.2f}**\n"
    response_text += f"• Número de ventas: **{total_transactions}**\n"
    response_text += f"• Ticket promedio: **S/ {total_sales/total_transactions:.2f}**"
    
    return ChatResponse(
        response=response_text,
        intent="ventas_hoy",
        data={"total": total_sales, "count": total_transactions}
    )


def handle_top_productos(products: list):
    """Muestra productos más vendidos (simulado)"""
    # En producción, ordenar por ventas reales
    top_products = products[:5]
    
    response_text = "**Top 5 Productos**\n\n"
    
    for i, product in enumerate(top_products, 1):
        name = product.get('name', 'Producto')
        stock = product.get('stock', 0)
        response_text += f"{i}. **{name}** - Stock: {stock} unidades\n"
    
    return ChatResponse(
        response=response_text,
        intent="top_productos",
        data={"products": top_products}
    )


def handle_listar_categorias(categories: list):
    """Lista categorias disponibles"""
    if not categories:
        return ChatResponse(
            response="No se encontraron categorias registradas.",
            intent="listar_categorias",
            data={"count": 0}
        )

    response_text = f"**Categorias** ({len(categories)})\n\n"

    for i, category in enumerate(categories[:10], 1):
        name = category.get('name', 'Categoria')
        response_text += f"{i}. {name}\n"

    if len(categories) > 10:
        response_text += "\nMostrando 10 categorias. Puedes pedir mas si lo necesitas."

    return ChatResponse(
        response=response_text,
        intent="listar_categorias",
        data={"count": len(categories)}
    )


def handle_ordenes_general(sales: list):
    """Lista ordenes (ventas) recientes"""
    if not sales:
        return ChatResponse(
            response="No se encontraron ordenes registradas.",
            intent="ordenes_general",
            data={"count": 0}
        )

    response_text = "**Ordenes recientes**\n\n"

    for sale in sales[:10]:
        sale_id = sale.get('id')
        total = sale.get('total', 0)
        date = sale.get('date', '')
        client = sale.get('client') or {}
        client_name = f"{client.get('nombres', '')} {client.get('apellidos', '')}".strip() or "Cliente no registrado"
        response_text += f"- Orden #{sale_id} | {client_name} | Total: S/ {total}\n"

    return ChatResponse(
        response=response_text,
        intent="ordenes_general",
        data={"count": len(sales)}
    )


def handle_ordenes_cliente(message: str, sales: list, clients: list):
    """Lista ordenes de un cliente especifico"""
    if not clients:
        return ChatResponse(
            response="No hay clientes registrados en el sistema.",
            intent="ordenes_cliente",
            data=None
        )

    client = extract_client_from_message(message, clients)

    if not client:
        return ChatResponse(
            response="No encontre el cliente en tu mensaje. Ejemplo: 'ordenes del cliente Juan Perez'.",
            intent="ordenes_cliente",
            data=None
        )

    client_id = client.get('id')
    client_name = f"{client.get('nombres', '')} {client.get('apellidos', '')}".strip()

    client_sales = [sale for sale in sales if (sale.get('client') or {}).get('id') == client_id]

    if not client_sales:
        return ChatResponse(
            response=f"No se encontraron ordenes para {client_name}.",
            intent="ordenes_cliente",
            data={"clientId": client_id, "count": 0}
        )

    response_text = f"**Ordenes de {client_name}** ({len(client_sales)})\n\n"

    for sale in client_sales[:10]:
        sale_id = sale.get('id')
        total = sale.get('total', 0)
        date = sale.get('date', '')
        items = sale.get('items') or []
        response_text += f"- Orden #{sale_id} | Total: S/ {total} | Items: {len(items)}\n"

    return ChatResponse(
        response=response_text,
        intent="ordenes_cliente",
        data={"clientId": client_id, "count": len(client_sales)}
    )


def handle_ayuda():
    """Muestra ayuda de comandos"""
    response_text = """
**¿Qué puedo hacer por ti?**

**Consultas de Stock:**
• "¿Cuánto stock hay de [producto]?"
• "¿Qué productos tienen stock bajo?"
• "Muestra el inventario"

**Predicciones:**
• "¿Cuándo se agotará [producto]?"
• "¿Debo reponer [producto]?"

**Ventas:**
• "¿Cuántas ventas hubo hoy?"
• "Muestra los productos más vendidos"

**Categorias:**
• "Lista las categorias"
• "Muestra categorias"

**Ordenes:**
• "Ordenes recientes"
• "Ordenes del cliente Juan Perez"

**Otros:**
• Simplemente escribe tu pregunta y te ayudaré

Tip: Sé natural, entiendo lenguaje cotidiano
"""
    
    return ChatResponse(
        response=response_text.strip(),
        intent="ayuda",
        data=None
    )


def handle_saludo():
    """Responde saludos"""
    return ChatResponse(
        response="Hola, soy el asistente inteligente de ZOOTEC.\n\n¿En que puedo ayudarte? Puedo consultar stock, hacer predicciones, mostrar ventas y mas.\n\nEscribe 'ayuda' para ver todo lo que puedo hacer.",
        intent="saludo",
        data=None
    )


# ============================================
# ENDPOINT PRINCIPAL
# ============================================

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Endpoint principal del chatbot
    Procesa mensajes y retorna respuestas inteligentes
    """
    try:
        user_message = message.message.strip()
        
        if not user_message:
            raise HTTPException(status_code=400, detail="Mensaje vacío")
        
        # Detectar intención
        intent = detect_intent(user_message)
        
        # Obtener datos necesarios
        products = get_all_products()
        sales_data = get_sales_data()
        categories = get_categories()
        clients = get_clients()
        
        # Procesar según intención
        if intent == 'consulta_stock':
            return handle_consulta_stock(user_message, products)
        
        elif intent == 'stock_bajo':
            return handle_stock_bajo(products)
        
        elif intent == 'prediccion':
            return handle_prediccion(user_message, products, sales_data)
        
        elif intent == 'ventas_hoy':
            return handle_ventas_hoy(sales_data)
        
        elif intent == 'top_productos':
            return handle_top_productos(products)
        
        elif intent == 'listar_productos':
            return handle_consulta_stock(user_message, products)

        elif intent == 'listar_categorias':
            return handle_listar_categorias(categories)

        elif intent == 'ordenes_general':
            return handle_ordenes_general(sales_data)

        elif intent == 'ordenes_cliente':
            return handle_ordenes_cliente(user_message, sales_data, clients)
        
        elif intent == 'ayuda':
            return handle_ayuda()
        
        elif intent == 'saludo':
            return handle_saludo()
        
        else:
            return ChatResponse(
                response="No entendi eso. Escribe 'ayuda' para ver que puedo hacer o reformula tu pregunta.",
                intent="desconocido",
                data=None
            )
    
    except requests.RequestException as e:
        raise HTTPException(
            status_code=503,
            detail=f"Error al conectar con el backend: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error interno: {str(e)}"
        )


@app.get("/api/chat/health")
async def health_check():
    """Health check del chatbot"""
    return {
        "status": "operational",
        "service": "ZOOTEC IA Chatbot",
        "version": "1.0.0",
        "capabilities": [
            "Consultas de stock",
            "Predicción de agotamiento",
            "Análisis de ventas",
            "Recomendaciones automáticas"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    print("Iniciando Chatbot IA de ZOOTEC...")
    print("URL: http://localhost:8000")
    print("Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)

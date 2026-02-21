from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from contextlib import asynccontextmanager
from database import init_db, get_db
from models.preferences import predict_preferences
from models.promotions import suggest_promotions
from typing import Optional

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Validar BD al arrancar"""
    init_db()
    print("AI service iniciado - Conectado a BD MySQL ZOOTEC")
    print("API disponible en: http://localhost:8000")
    yield
    print("AI service detenido")

app = FastAPI(title="ZOOTEC AI SERVICE", lifespan=lifespan)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "AI service running",
        "database": "MySQL ZOOTEC",
        "version": "2.0",
        "endpoints": {
            "preferences": "POST /api/ai/preferences",
            "promotions": "POST /api/ai/promotions",
            "products": "GET /api/products",
            "sales": "GET /api/sales"
        }
    }

# Endpoints con prefijo /api/
@app.post("/api/ai/preferences")
def get_preferences_api(data: dict, db: Session = Depends(get_db)):
    return predict_preferences(data, db)

@app.post("/api/ai/promotions")
def get_promotions_api(data: Optional[dict] = None, db: Session = Depends(get_db)):
    """Acepta opcional payload desde backend pero no lo usa"""
    return suggest_promotions(db)

# Endpoints sin prefijo (compatibilidad)
@app.post("/ai/preferences")
def get_preferences(data: dict, db: Session = Depends(get_db)):
    return predict_preferences(data, db)

@app.post("/ai/promotions")
def get_promotions(data: Optional[dict] = None, db: Session = Depends(get_db)):
    """Acepta opcional payload desde backend pero no lo usa"""
    return suggest_promotions(db)

@app.get("/products")
def list_products(db: Session = Depends(get_db)):
    """Lista productos con stock"""
    try:
        query = text("""
            SELECT p.id, p.name, p.stock, p.price, 
                   COALESCE(c.name, 'N/A') as categoria, 
                   COALESCE(b.name, 'N/A') as marca
            FROM products p
            LEFT JOIN categories c ON p.category_id = c.id
            LEFT JOIN brands b ON p.brand_id = b.id
            WHERE p.active = 1
            ORDER BY p.stock ASC
            LIMIT 50
        """)
        results = db.execute(query).fetchall()
        return {
            "total": len(results),
            "products": [
                {
                    "id": row[0],
                    "name": row[1],
                    "stock": row[2],
                    "price": float(row[3]) if row[3] else 0,
                    "category": row[4],
                    "brand": row[5]
                } for row in results
            ]
        }
    except Exception as e:
        return {"error": str(e), "total": 0, "products": []}

@app.get("/api/products")
def list_products_api(db: Session = Depends(get_db)):
    """Lista productos con stock"""
    return list_products(db)

@app.get("/sales")
def sales_analytics(db: Session = Depends(get_db)):
    """Análisis de ventas"""
    try:
        query = text("""
            SELECT COALESCE(c.name, 'Sin categoría') as categoria,
                   COUNT(DISTINCT s.id) as total_ventas,
                   COALESCE(SUM(si.subtotal), 0) as ingresos,
                   COALESCE(AVG(si.subtotal), 0) as ticket_promedio
            FROM sales s
            JOIN sale_items si ON s.id = si.sale_id
            JOIN products p ON si.product_id = p.id
            LEFT JOIN categories c ON p.category_id = c.id
            GROUP BY c.id, c.name
            ORDER BY ingresos DESC
            LIMIT 20
        """)
        results = db.execute(query).fetchall()
        return {
            "categories": [
                {
                    "categoria": row[0],
                    "vendidas": row[1],
                    "ingresos": float(row[2]),
                    "ticket_promedio": float(row[3])
                } for row in results
            ]
        }
    except Exception as e:
        return {"error": str(e), "categories": []}

@app.get("/api/sales")
def sales_analytics_api(db: Session = Depends(get_db)):
    """Análisis de ventas"""
    return sales_analytics(db)

@app.get("/topology")
def db_topology(db: Session = Depends(get_db)):
    """Estructura de la BD"""
    try:
        query = text("""
            SELECT TABLE_NAME 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = 'zzootec_db'
            ORDER BY TABLE_NAME
        """)
        tables = db.execute(query).fetchall()
        return {
            "database": "zzootec_db",
            "table_count": len(tables),
            "tables": [row[0] for row in tables]
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/topology")
def db_topology_api(db: Session = Depends(get_db)):
    """Estructura de la BD"""
    return db_topology(db)


# Intento de incluir las rutas del chatbot si el módulo existe.
# Esto permite que `/api/chat` (definido en chatbot.py) esté disponible
# cuando se ejecuta el `app` de `main.py`.
try:
    import chatbot as chatbot_module
    for _route in chatbot_module.app.router.routes:
        app.router.routes.append(_route)
except Exception as _e:
    print(f"Advertencia: no se pudieron añadir rutas del chatbot: {_e}")

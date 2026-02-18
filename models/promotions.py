from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal
import time

def suggest_promotions(db: Session = None):
    """
    Sugiere promociones - Versión ultra simplificada
    """
    
    start_time = time.time()
    print(f"[PROMOTIONS] Iniciando generación de promociones...")
    
    if db is None:
        db = SessionLocal()
    
    try:
        # Query optimizada con índice en active
        query = text("""
            SELECT 
                p.id,
                p.name,
                p.stock,
                p.price
            FROM products p
            WHERE p.active = 1
            LIMIT 50
        """)
        
        query_start = time.time()
        results = db.execute(query).fetchall()
        query_time = time.time() - query_start
        print(f"[PROMOTIONS] Query ejecutada en {query_time:.2f}s - {len(results)} productos")
        
        suggestions = []
        
        for row in results:
            product_id = row[0]
            name = row[1]
            stock = row[2] or 0
            price = row[3] or 0
            
            # Lógica simple basada solo en stock
            if stock == 0:
                suggestion = "SIN STOCK"
                priority = "CRITICAL"
            elif stock < 5:
                suggestion = "STOCK CRITICO"
                priority = "HIGH"
            elif stock > 100:
                suggestion = "EXCESO STOCK"
                priority = "MEDIUM"
            elif stock < 20:
                suggestion = "STOCK BAJO"
                priority = "MEDIUM"
            else:
                continue
            
            suggestions.append({
                "product_id": product_id,
                "product_name": name,
                "stock": stock,
                "price": float(price),
                "suggestion": suggestion,
                "priority": priority
            })
        
        # Ordenar por prioridad
        priority_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}
        suggestions.sort(key=lambda x: priority_order.get(x["priority"], 4))
        
        total_time = time.time() - start_time
        print(f"[PROMOTIONS] Completado en {total_time:.2f}s - {len(suggestions)} sugerencias")
        
        return {"count": len(suggestions), "promotions": suggestions[:50]}
        
    except Exception as e:
        print(f"[PROMOTIONS] ERROR: {str(e)}")
        return {
            "error": str(e),
            "message": "Error al generar promociones",
            "count": 0,
            "promotions": []
        }

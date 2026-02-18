from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal

def predict_preferences(data: dict, db: Session = None):
    """
    Analiza preferencias de cliente basado en historial de compras
    Utiliza las tablas: sales, sale_items, products, clients
    """
    
    if db is None:
        db = SessionLocal()
    
    try:
        customer_id = data.get("client_id")
        
        # Si se proporciona cliente específico
        if customer_id:
            query = text("""
                SELECT c.nombres, c.apellidos, 
                       cat.name as categoria,
                       COUNT(si.id) as cantidad,
                       SUM(si.quantity) as total_cantidad
                FROM sales s
                JOIN sale_items si ON s.id = si.sale_id
                JOIN products p ON si.product_id = p.id
                JOIN categories cat ON p.category_id = cat.id
                JOIN clients c ON s.client_id = c.id
                WHERE s.client_id = :client_id
                GROUP BY cat.name, c.id
                ORDER BY total_cantidad DESC
                LIMIT 5
            """)
            results = db.execute(query, {"client_id": customer_id}).fetchall()
        else:
            # Análisis general de categorías más vendidas
            query = text("""
                SELECT cat.name as categoria,
                       COUNT(si.id) as compras,
                       SUM(si.quantity) as total_cantidad,
                       SUM(si.subtotal) as ingresos
                FROM sale_items si
                JOIN products p ON si.product_id = p.id
                JOIN categories cat ON p.category_id = cat.id
                GROUP BY cat.name
                ORDER BY total_cantidad DESC
                LIMIT 10
            """)
            results = db.execute(query).fetchall()
        
        if results:
            preferred = results[0][0]
            confidence = round(0.85 + (0.15 * len(results) / 10), 2)
            
            return {
                "preferredCategory": preferred,
                "confidence": confidence,
                "topCategories": [{"category": row[0], "quantity": row[2]} for row in results],
                "source": "database"
            }
        else:
            return {
                "message": "Sin historial de compras",
                "confidence": 0.0
            }
        
    except Exception as e:
        return {
            "error": str(e),
            "message": "Error al analizar preferencias",
            "confidence": 0.0
        }

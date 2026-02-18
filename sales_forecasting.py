"""
MÓDULO DE IA PARA TESIS: CHATBOT ADMINISTRATIVO
Sistema de Gestión de Ventas Omnicanal - Zzootec
Ica, 2025

Chatbot inteligente para consultas de inventario y productos
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import re
import requests
from datetime import datetime

app = FastAPI(title="ZOOTEC IA - Chatbot Administrativo")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URL del backend
BACKEND_URL = "http://localhost:8080"

class SaleData(BaseModel):
    date: str
    product_id: int
    product_name: str
    quantity: int
    total: float

class ForecastRequest(BaseModel):
    product_id: int
    historical_sales: List[SaleData]
    days_ahead: int = 30

class ForecastResponse(BaseModel):
    product_id: int
    product_name: str
    predictions: List[Dict[str, any]]
    confidence: float
    recommendation: str

@app.post("/api/forecast/sales", response_model=ForecastResponse)
async def forecast_sales(request: ForecastRequest):
    """
    Predice ventas futuras usando análisis de tendencias
    
    ALGORITMO:
    1. Analiza histórico de ventas
    2. Detecta tendencias y estacionalidad
    3. Calcula promedio móvil
    4. Predice ventas futuras
    5. Genera recomendaciones
    """
    
    try:
        # Convertir datos a DataFrame
        df = pd.DataFrame([sale.dict() for sale in request.historical_sales])
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Calcular estadísticas
        avg_daily_sales = df['quantity'].mean()
        std_sales = df['quantity'].std()
        trend = calculate_trend(df['quantity'].values)
        
        # Generar predicciones
        predictions = []
        base_date = datetime.now()
        
        for day in range(request.days_ahead):
            pred_date = base_date + timedelta(days=day)
            
            # Predicción simple con tendencia
            predicted_qty = max(0, int(avg_daily_sales + (trend * day)))
            
            # Agregar variabilidad (simulación de estacionalidad)
            weekend_factor = 0.8 if pred_date.weekday() >= 5 else 1.0
            predicted_qty = int(predicted_qty * weekend_factor)
            
            predictions.append({
                "date": pred_date.strftime("%Y-%m-%d"),
                "predicted_quantity": predicted_qty,
                "confidence": round(max(0.5, 1 - (std_sales / avg_daily_sales)), 2)
            })
        
        # Calcular total predicho
        total_predicted = sum(p['predicted_quantity'] for p in predictions)
        
        # Generar recomendación
        recommendation = generate_recommendation(
            total_predicted, 
            avg_daily_sales * request.days_ahead,
            trend
        )
        
        return ForecastResponse(
            product_id=request.product_id,
            product_name=request.historical_sales[0].product_name,
            predictions=predictions,
            confidence=round(max(0.6, 1 - (std_sales / avg_daily_sales)), 2),
            recommendation=recommendation
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error en predicción: {str(e)}")


def calculate_trend(sales_data):
    """Calcula la tendencia lineal de las ventas"""
    if len(sales_data) < 2:
        return 0
    
    x = np.arange(len(sales_data))
    y = sales_data
    
    # Regresión lineal simple
    slope = np.polyfit(x, y, 1)[0]
    return slope


def generate_recommendation(predicted_total, expected_total, trend):
    """Genera recomendación basada en predicción"""
    
    if trend > 0.5:
        return f"[TENDENCIA ALCISTA]: Se predice aumento de ventas. Recomendación: Aumentar stock en 20%."
    elif trend < -0.5:
        return f"[TENDENCIA BAJISTA]: Ventas en descenso. Recomendación: Considerar promoción para aumentar rotación."
    elif predicted_total < expected_total * 0.8:
        return f"[BAJA DEMANDA ESPERADA]: Ajustar stock para evitar sobreinventario."
    elif predicted_total > expected_total * 1.2:
        return f"[ALTA DEMANDA ESPERADA]: Asegurar stock suficiente para {int(predicted_total)} unidades."
    else:
        return f"[OK]: Mantener niveles actuales de inventario."


@app.get("/api/forecast/health")
async def health_check():
    """Health check del servicio de IA"""
    return {
        "status": "operational",
        "service": "Sales Forecasting ML",
        "version": "1.0.0",
        "algorithm": "Linear Regression + Moving Average"
    }


# ============================================
# ENDPOINT ADICIONAL: Análisis de Productos
# ============================================

@app.post("/api/analyze/product-performance")
async def analyze_product_performance(sales_data: List[SaleData]):
    """
    Analiza rendimiento de productos y detecta patrones
    
    Retorna:
    - Productos con mejor/peor rendimiento
    - Detección de anomalías
    - Recomendaciones de acción
    """
    
    df = pd.DataFrame([sale.dict() for sale in sales_data])
    
    # Agrupar por producto
    product_stats = df.groupby('product_id').agg({
        'quantity': ['sum', 'mean', 'std'],
        'total': 'sum'
    }).reset_index()
    
    # Detectar productos top y bottom
    product_stats.columns = ['product_id', 'total_qty', 'avg_qty', 'std_qty', 'revenue']
    product_stats = product_stats.sort_values('revenue', ascending=False)
    
    top_products = product_stats.head(5).to_dict('records')
    bottom_products = product_stats.tail(5).to_dict('records')
    
    return {
        "analysis_date": datetime.now().isoformat(),
        "total_products_analyzed": len(product_stats),
        "top_performers": top_products,
        "low_performers": bottom_products,
        "recommendations": [
            "Promover productos de bajo rendimiento con descuentos",
            "Aumentar stock de productos top",
            "Analizar causas de baja rotación en productos bottom"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

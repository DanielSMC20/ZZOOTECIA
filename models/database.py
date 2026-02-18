from sqlalchemy import Table, MetaData
from database import engine

# Reflexionar todas las tablas existentes automáticamente
metadata = MetaData()
metadata.reflect(bind=engine)

# Acceso a las tablas
products = metadata.tables.get('products')
sales = metadata.tables.get('sales')
sale_items = metadata.tables.get('sale_items')
clients = metadata.tables.get('clients')
categories = metadata.tables.get('categories')
brands = metadata.tables.get('brands')
orders = metadata.tables.get('orders')
order_items = metadata.tables.get('order_items')
inventory_movements = metadata.tables.get('inventory_movements')
usuarios = metadata.tables.get('usuarios')

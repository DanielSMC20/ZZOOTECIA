from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe
load_dotenv()

# Configuración de conexión MySQL (leer desde variables de entorno, con valores por defecto)
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "zzootec_db")

# URL de conexión
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
)

# Crear engine con pool de conexiones
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
    max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
    echo=False
)

# Crear sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos
Base = declarative_base()

def get_db():
    """Dependencia para obtener la sesión de BD en FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Validar conexión a BD - NO crea ni modifica tablas"""
    try:
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()
        
        print("✅ Conexión a BD establecida")
        print(f"   Tablas encontradas: {', '.join(existing_tables)}")
    except Exception as e:
        print(f"⚠️  MySQL no disponible: {str(e)}")
        print("   La API funcionará pero sin persistencia de datos")


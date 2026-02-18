from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import QueuePool

# Configuración de conexión MySQL
# Cambia estos valores con tus credenciales
DB_USER = "root"  # Tu usuario MySQL
DB_PASSWORD = "DanielSMC123-"  # Tu contraseña
DB_HOST = "localhost"  # Host MySQL
DB_NAME = "zzootec_db"  # Nombre de la base de datos

# URL de conexión
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

# Crear engine con pool de conexiones
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
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
    inspector = inspect(engine)
    existing_tables = inspector.get_table_names()
    
    print("Conexión a BD establecida")
    print(f"Tablas encontradas: {', '.join(existing_tables)}")


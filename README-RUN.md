Arranque rápido (solo local)

Requisitos

- Python 3.8+ instalado

Preparación (una sola vez)

1. Copia y edita variables locales:

```powershell
copy .env.example .env
notepad .env
```

2. Preparar entorno y dependencias (PowerShell):

```powershell
.
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Uso diario

- Lanzador (desde CMD):

```cmd
start-chatbot.bat
```

- O PowerShell (si ya activaste `.venv`):

```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🔌 Configurar MySQL (opcional pero recomendado)

Si quieres persistencia de datos, configura MySQL:

### Windows - Con XAMPP/WAMP

1. Inicia cualquiera de estos:
   - **XAMPP**: Abre `xampp-control.exe` → Click en "Start" junto a MySQL
   - **WAMP**: Abre `wampmanager.exe` → Click en MySQL
   - **MySQL Community Server**: Asegúrate de que el servicio está corriendo

2. Verifica la conexión:

   ```cmd
   mysql -u root -p
   ```

3. Edita `.env` con tus credenciales reales:
   ```env
   DB_USER=root
   DB_PASSWORD=tu_contraseña_mysql
   DB_HOST=localhost
   DB_NAME=zzootec_db
   ```

### Crear la base de datos (si no existe)

```bash
mysql -u root -p
```

Luego en MySQL:

```sql
CREATE DATABASE IF NOT EXISTS zzootec_db;
EXIT;
```

---

## Notas importantes

- `start-chatbot.bat` es un lanzador inteligente: **crea automáticamente el entorno virtual e instala dependencias si no existen**, luego ejecuta `uvicorn main:app`.
- Otros usuarios solo necesitan ejecutar `start-chatbot.bat` sin configuración previa.
- Para desarrollo avanzado, usa `start-server.ps1` o los comandos manuales en PowerShell.
- Copia y ajusta `.env.example` a `.env` para configurar `BACKEND_URL` y datos de MySQL.
- `main.py` expone `/api/chat` desde `chatbot.py`.

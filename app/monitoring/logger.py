import sys
from loguru import logger
import os

# Buat folder logs jika belum ada
if not os.path.exists("logs"):
    os.makedirs("logs")

# 1. Konfigurasi Logger
# Hapus handler default biar tidak double log
logger.remove()

# 2. Handler untuk Terminal (Warna-warni, mudah dibaca)
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# 3. Handler untuk File (Menyimpan log ke file "app.log")
# rotation="10 MB" artinya kalau file sudah 10MB, dia buat file baru (biar hardisk gak penuh)
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days", # Simpan log selama 7 hari saja
    level="DEBUG"
)

# Fungsi helper agar mudah diimport
def get_logger(name: str):
    return logger.bind(name=name)
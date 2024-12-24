from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
import os

# Konfigurasi logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URL database dari environment variables atau default
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mssql+pyodbc://sa:Sloth123@localhost\\SQLEXPRESS/matkul_db?driver=ODBC+Driver+17+for+SQL+Server"
)

# Inisialisasi engine
try:
    engine = create_engine(DATABASE_URL, echo=True)
    # Tes koneksi awal ke database
    with engine.connect() as conn:
        logger.info("Berhasil terkoneksi ke database!")
except Exception as e:
    logger.error(f"Gagal koneksi ke database: {str(e)}")
    raise

# Inisialisasi sessionmaker dan Base
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Fungsi untuk mendapatkan instance database session
def get_db():
    """
    Mendapatkan session database. Pastikan menggunakan `yield` agar otomatis ditutup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fungsi untuk inisialisasi database
def init_db():
    """
    Membuat tabel di database berdasarkan model yang didefinisikan di Base.
    Pastikan semua model sudah di-import sebelum fungsi ini dipanggil.
    """
    try:
        # Call to create all tables based on the models
        Base.metadata.create_all(bind=engine)
        logger.info("Tabel berhasil dibuat di database!")
    except Exception as e:
        logger.error(f"Error saat inisialisasi database: {str(e)}")
        raise
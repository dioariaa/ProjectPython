# controllers/nilai_controller.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from schemas.schemas import NilaiBase, MataKuliahBase
from database.models import Nilai, MataKuliah
from typing import List
import pandas as pd
import joblib

router = APIRouter()

# Cache data Excel using joblib
def load_excel_data_cached():
    try:
        # Check if the cached data exists
        df = joblib.load("data_mahasiswa_cache.pkl")
    except FileNotFoundError:
        # If no cache, read from Excel and save it to cache
        df = pd.read_excel("biodata_mahasiswa.xlsx")
        joblib.dump(df, "data_mahasiswa_cache.pkl")
    return df

# Function to get Nama from Excel
def get_nama_from_excel(nim: str):
    try:
        df = load_excel_data_cached()  # Using cached data
        df["NIM"] = df["NIM"].astype(str).str.strip()  # Convert NIM to string and remove extra spaces
        
        # Find the record by NIM
        result = df[df["NIM"] == nim]
        
        if not result.empty:
            return result.iloc[0]["Nama"]
        else:
            return "Nama tidak ditemukan"
    except Exception as e:
        # Reduce unnecessary logging for performance
        return "Error saat membaca file Excel"

@router.get("/data/{nim}")
async def get_data_by_nim(nim: str, db: Session = Depends(get_db)):
    # Retrieve data for the given NIM
    query = db.query(Nilai, MataKuliah).join(MataKuliah, Nilai.Matkul_ID == MataKuliah.Matkul_ID).filter(Nilai.NIM == nim)
    result = query.all()

    # Fetch Name from Excel
    nama = get_nama_from_excel(nim)
    
    # Format the response
    response = {
        "Nama": nama,
        "NIM": nim,
        "Matakuliah": [
            {
                "Matkul_ID": item[1].Matkul_ID,
                "Nama_Matkul": item[1].nama_matkul,
                "SKS": item[1].sks,
                "Nilai": item[0].Nilai
            }
            for item in result
        ]
    }

    return response

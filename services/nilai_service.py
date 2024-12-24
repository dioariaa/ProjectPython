from fastapi import HTTPException
from sqlalchemy.orm import Session
import pandas as pd
from typing import Dict, List
import logging
from repositories.nilai_repository import get_nilai_by_nim

logger = logging.getLogger(__name__)

async def fetch_nilai_by_nim(
    nim: str,
    db: Session,
    biodata_mahasiswa: pd.DataFrame
) -> Dict:
    """
    Mengambil dan menggabungkan data nilai dengan biodata mahasiswa
    """
    try:
        # Cari data mahasiswa
        mahasiswa = biodata_mahasiswa[biodata_mahasiswa["NIM"].astype(str) == str(nim)]
        if mahasiswa.empty:
            logger.warning(f"Mahasiswa dengan NIM {nim} tidak ditemukan")
            raise HTTPException(
                status_code=404,
                detail="Mahasiswa tidak ditemukan"
            )

        nama = mahasiswa.iloc[0]["Nama"]
        
        # Ambil data nilai
        nilai_data = await get_nilai_by_nim(db, nim)
        if not nilai_data:
            logger.warning(f"Nilai tidak ditemukan untuk NIM {nim}")
            raise HTTPException(
                status_code=404,
                detail="Nilai tidak ditemukan"
            )

        # Susun response
        results = [
            {
                "id_mk": matkul.id,
                "nama_mk": matkul.nama,
                "nim": nim,
                "nama": nama,
                "nilai": nilai.nilai,
            }
            for nilai, matkul in nilai_data
        ]

        return {"data": results}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error dalam fetch_nilai_by_nim: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Gagal memproses data nilai"
        )
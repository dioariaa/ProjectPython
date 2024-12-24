from fastapi import HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from database.models import Nilai, MataKuliah
import logging
import pandas as pd  # Import pandas for Excel export
from io import BytesIO  # Import BytesIO for in-memory file handling

logger = logging.getLogger(__name__)

async def get_nilai_by_nim(db: Session, nim: str, export_excel: bool = False):
    """
    Mengambil data nilai mahasiswa berdasarkan NIM.

    Args:
        db (Session): Koneksi database SQLAlchemy
        nim (str): Nomor Induk Mahasiswa
        export_excel (bool): Jika True, hasil akan diekspor ke file Excel

    Returns:
        List[Dict] atau Response: Daftar nilai dan informasi mata kuliah atau file Excel

    Raises:
        HTTPException: Jika terjadi masalah dengan database atau data tidak ditemukan
    """
    try:
        # Test koneksi database
        db.execute(text("SELECT 1"))

        # Query utama menggunakan ORM
        result = (
            db.query(Nilai, MataKuliah)
            .join(MataKuliah, Nilai.Matkul_ID == MataKuliah.Matkul_ID)
            .filter(Nilai.NIM == nim)
            .all()
        )

        if not result:
            logger.warning(f"Tidak ada data nilai untuk NIM: {nim}")
            return []

        # Format ulang hasil query
        formatted_result = []
        for row in result:
            if isinstance(row, tuple) and len(row) == 2 and isinstance(row[0], Nilai) and isinstance(row[1], MataKuliah):
                nilai, matkul = row
                formatted_result.append({
                    "id_mk": matkul.Matkul_ID,
                    "nama_mk": matkul.nama,
                    "nim": nilai.NIM,
                    "nilai": nilai.Nilai,
                })
            else:
                logger.error(f"Unexpected row format: {row}, types: {type(row[0])}, {type(row[1])}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Format hasil query tidak sesuai: {row}"
                )

        logger.info(f"Berhasil mengambil {len(formatted_result)} data nilai untuk NIM: {nim}")

        if export_excel:
            # Convert to DataFrame
            df = pd.DataFrame(formatted_result)
            # Create a BytesIO buffer
            output = BytesIO()
            # Write DataFrame to Excel file
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Nilai')
            output.seek(0)
            # Return the Excel file as a response
            headers = {
                'Content-Disposition': f'attachment; filename=nilai_{nim}.xlsx'
            }
            return Response(content=output.read(), media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', headers=headers)

        return formatted_result

    except SQLAlchemyError as e:
        # Log error database dengan detail
        error_msg = f"Error database saat mengambil nilai untuk NIM {nim}: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail=f"Error database: {str(e)}"
        )
    except Exception as e:
        # Log error tidak terduga
        error_msg = f"Error tidak terduga saat mengambil nilai untuk NIM {nim}: {str(e)}"
        logger.error(error_msg)
        raise HTTPException(
            status_code=500,
            detail=f"Error sistem: {str(e)}"
        )

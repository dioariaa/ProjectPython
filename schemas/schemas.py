from pydantic import BaseModel, root_validator

class MataKuliahBase(BaseModel):
    Matkul_ID: int
    nama_matkul: str
    sks: int

class NilaiBase(BaseModel):
    Matkul_ID: int
    NIM: str
    Nilai: float
    matakuliah: MataKuliahBase
    Nama: str  # Tambahkan field Nama

    class Config:
        orm_mode = True  # Agar bisa bekerja dengan model SQLAlchemy

    @root_validator(pre=True)
    def convert_nim_to_string(cls, values):
        # Convert NIM to string if it's passed as an integer
        if 'NIM' in values and isinstance(values['NIM'], int):
            values['NIM'] = str(values['NIM'])
        return values
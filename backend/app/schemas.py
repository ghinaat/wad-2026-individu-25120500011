from pydantic import BaseModel, Field


class BukuCreate(BaseModel):
    """Skema INPUT — dipakai saat client mengirim data lewat POST.
    Tidak punya `id`, karena id dibuat oleh server."""

    judul: str = Field(..., min_length=1, description="Judul buku")
    penulis: str = Field(..., min_length=1, description="Nama penulis")
    isbn: str = Field(
        ...,
        pattern=r"^\d{13}$",
        description="ISBN harus tepat 13 digit angka, contoh: 9786020383177",
    )
    tahun_terbit: int = Field(
        ..., ge=1900, le=2026, description="Tahun terbit, antara 1900 dan 2026"
    )


class BukuOut(BukuCreate):
    """Skema OUTPUT — dikembalikan ke client. Mewarisi semua field
    BukuCreate lalu menambahkan `id` yang dibuat server."""

    id: int

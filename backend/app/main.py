from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query, Response

from .schemas import BukuCreate, BukuOut

app = FastAPI(title="API Buku — Tugas Individu FastAPI Endpoint")


_db: Dict[int, BukuOut] = {}
_next_id: int = 1


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/buku", response_model=BukuOut, status_code=201)
def create_buku(payload: BukuCreate, response: Response):
    """POST /api/buku -> 201 Created + header Location.
    Body tidak valid (isbn bukan 13 digit, tahun di luar rentang, dst)
    otomatis ditolak FastAPI/Pydantic dengan 422 sebelum masuk ke sini."""
    global _next_id
    new_id = _next_id
    _next_id += 1

    buku = BukuOut(id=new_id, **payload.model_dump())
    _db[new_id] = buku

    response.headers["Location"] = f"/api/buku/{new_id}"
    return buku


@app.get("/api/buku", response_model=List[BukuOut])
def list_buku(
    skip: int = Query(0, ge=0, description="Lewati N item pertama"),
    limit: int = Query(10, ge=1, le=100, description="Maksimum item yang dikembalikan"),
    search: Optional[str] = Query(
        None, description="Cari (case-insensitive) di judul atau penulis"
    ),
):
    """GET /api/buku -> 200 OK, mendukung ?skip, ?limit, ?search."""
    items = list(_db.values())

    if search:
        needle = search.lower()
        items = [
            b for b in items if needle in b.judul.lower() or needle in b.penulis.lower()
        ]

    return items[skip : skip + limit]


@app.get("/api/buku/{buku_id}", response_model=BukuOut)
def get_buku(buku_id: int):
    """GET /api/buku/{id} -> 404 kalau id tidak ada."""
    buku = _db.get(buku_id)
    if buku is None:
        raise HTTPException(
            status_code=404, detail=f"Buku dengan id={buku_id} tidak ditemukan"
        )
    return buku
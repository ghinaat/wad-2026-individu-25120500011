# wad-2026-individu-&lt;NIM&gt; — API Buku (T1)

Tugas individu: satu endpoint FastAPI untuk entitas **Buku**.

## Cara menjalankan

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Buka `http://localhost:8000/docs` untuk OpenAPI/Swagger UI.

## Endpoint

| Method | Path | Sukses | Gagal |
|---|---|---|---|
| POST | `/api/buku` | `201 Created` + header `Location: /api/buku/{id}` | `422` kalau `isbn` bukan 13 digit atau `tahun_terbit` di luar 1900–2026 |
| GET | `/api/buku` | `200 OK`, dukung `?skip=`, `?limit=`, `?search=` | — |
| GET | `/api/buku/{id}` | `200 OK` | `404 Not Found` kalau id tidak ada |

### Contoh body POST (valid)

```json
{
  "judul": "Laskar Pelangi",
  "penulis": "Andrea Hirata",
  "isbn": "9786020383177",
  "tahun_terbit": 2005
}
```

Field `id` **tidak** dikirim client — dibuat server dan hanya muncul di response
(`BukuOut`), bukan di skema input (`BukuCreate`).

### Validasi khusus (T1)

- `isbn`: harus tepat 13 digit angka (regex `^\d{13}$`)
- `tahun_terbit`: integer antara 1900 dan 2026 (inklusif)

## Contoh curl untuk verifikasi manual

```bash
# 201 + Location
curl -i -X POST http://localhost:8000/api/buku \
  -H "Content-Type: application/json" \
  -d '{"judul":"Laskar Pelangi","penulis":"Andrea Hirata","isbn":"9786020383177","tahun_terbit":2005}'

# 422 - isbn tidak 13 digit
curl -i -X POST http://localhost:8000/api/buku \
  -H "Content-Type: application/json" \
  -d '{"judul":"X","penulis":"Y","isbn":"123","tahun_terbit":2005}'

# 404 - id tidak ada
curl -i http://localhost:8000/api/buku/999
```

## Alur kerja (workflow)

```bash
git checkout -b feature/endpoint-individu
# ... kerjakan kode di backend/ ...
git add .
git commit -m "feat: tambah endpoint /api/buku (POST, GET list, GET by id)"
git push -u origin feature/endpoint-individu
# buka PR di GitHub: feature/endpoint-individu -> main
# review sendiri, lalu merge sendiri
```

## Bukti yang perlu di-screenshot untuk submit

1. `/docs` — POST sukses (`201`)
2. `/docs` — POST dengan body invalid (`422`)
3. `/docs` — GET `/api/buku/{id}` dengan id yang tidak ada (`404`)
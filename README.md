# Dokumen Skripsi — FT UM Buton (LaTeX + Word)

Tiga dokumen, masing-masing dapat dibuat sebagai **PDF (LaTeX)** dan **Word (.docx)**.

| Dokumen | Sumber | Isi |
|---|---|---|
| Pedoman Penulisan Skripsi | `pedoman/pedoman.tex` | A4, TNR 12, margin 4/3/3/3 cm, 2 spasi |
| Template Proposal Skripsi | `proposal/proposal.tex` | A4, TNR 12, margin 4/4/3/3 cm, 1,5 spasi, sitasi **APA** |
| Formulir Pengajuan Judul | `formulir/formulir.tex` | A4, Arial 12 |
| Format Seminar Hasil | `seminar-hasil/seminar-hasil.tex` + `bab/` | Bab I–V, 4/4/3/3 cm, 2 spasi, APA |
| Format Skripsi | `skripsi/skripsi.tex` + `bab/` | + pengesahan, keaslian, abstrak, kata pengantar, daftar isi/tabel/gambar |

## Cara pakai

```bash
./menu.sh                 # menu interaktif
./menu.sh word proposal   # langsung: pdf | word | semua | buka | bersih | cek  [pedoman|proposal|formulir|seminar-hasil|skripsi|semua]
```

Hasil ada di folder `hasil/`. Perlu: `xelatex`, `latexmk`, `pandoc`, `python3` (`./menu.sh cek`).

## Struktur

- `common/skripsi.sty` — gaya bersama LaTeX · `common/skripsi-bab.sty` — tata letak dokumen berbab (seminar hasil, skripsi)
- `proposal/bab/`, `seminar-hasil/bab/`, `skripsi/bab/` — isi per bab (satu berkas per bab); tambah bab baru dengan `\input{bab/NN-nama}` di berkas utama
- `word/buat_word.py` — pembuat Word (gaya, nomor halaman, section break) · `word/filter.lua` — filter pandoc
- `gambar/` — logo & gambar contoh (ganti file dengan nama sama untuk memakai gambar sendiri)

## Catatan

- Daftar Isi di Word berupa field: pilih **Yes/Ya** saat Word menawarkan memperbarui field.
- Edit isi hanya di file `.tex`; PDF dan Word dibuat ulang dari sumber yang sama.
- Hindari `>{\centering}p{..}` di tabel (pandoc menghilangkan isi sel); pakai `c` atau `p{..}`.
- Jangan jalankan pandoc dengan `TEXINPUTS` terisi (pandoc akan membongkar `skripsi.sty`); `menu.sh`/`buat_word.py` sudah menanganinya.

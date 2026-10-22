# Dokumen Skripsi — FT UM Buton (LaTeX + Word)

Program Studi Rekayasa Sistem Komputer, Fakultas Teknik, Universitas Muhammadiyah Buton.
Semua dokumen ditulis dalam **LaTeX** dan dapat dibuat sebagai **PDF** maupun **Word (.docx)** dari satu sumber yang sama.

## Dokumen

| Dokumen | Sumber | Isi |
| --- | --- | --- |
| Pedoman Penulisan Skripsi | `pedoman/pedoman.tex` + `bab/` | Bab I–V dan 7 lampiran (contoh, daftar periksa, gaya APA) |
| Template Proposal Skripsi | `proposal/proposal.tex` + `bab/` | sampul, persetujuan, abstrak, daftar isi, Bab I–III (jadwal pelaksanaan di Bab III), daftar pustaka |
| Format Seminar Hasil | `seminar-hasil/seminar-hasil.tex` + `bab/` | Bab I–V, daftar pustaka, lampiran; daftar isi/tabel/gambar/lampiran |
| Format Skripsi | `skripsi/skripsi.tex` + `bab/` | seminar hasil + pengesahan, pernyataan keaslian, abstrak, kata pengantar |
| Formulir Pengajuan Judul | `formulir/formulir.tex` | tiga usulan judul (tabel kotak penuh, satu halaman per usulan) + halaman verifikasi |
| **Contoh terisi** | `contoh/` | proposal, seminar hasil, dan skripsi yang sudah berisi (data fiktif) beserta PDF/Word-nya |
| Panduan LaTeX | `panduan/panduan-latex.md` (+ `.pdf`, `.docx`) | cara memakai, mengedit, dan mengonversi; analisis kesesuaian dokumen asli (bagian 14) |

## Aturan format yang sudah tertanam

| Hal | Pengaturan |
| --- | --- |
| Kertas / margin | A4; kiri 4, atas 4, kanan 3, bawah 3 cm (formulir: Arial 12, margin sendiri) |
| Huruf / spasi | Times New Roman 12 pt; isi 1,5 spasi; abstrak, judul tabel/gambar, daftar, daftar pustaka, lampiran 1 spasi; alinea menjorok 1 cm, rata kanan-kiri |
| Judul | `BAB I` + judul (14 pt tebal, tengah), tiap bab di halaman baru; subbab sampai tiga tingkat |
| Nomor halaman | sampul, persetujuan, pengesahan, keaslian: tanpa nomor; abstrak–daftar lampiran: romawi; isi: arab (awal bab tengah bawah, selanjutnya kanan atas) |
| Tabel / gambar | tabel kotak penuh, judul **di atas** (tengah); gambar, judul **di bawah** (tengah); nomor per bab (Tabel 2.1, Gambar 3.2; lampiran L1.1) |
| Sitasi | **APA edisi ke-7** (penulis–tahun), daftar pustaka lengkap dengan tanggal akses untuk sumber web |
| Nama dosen | nama pada lembar persetujuan/pengesahan selalu satu baris |

## Cara pakai

```bash
./menu.sh                      # menu interaktif
./menu.sh pdf proposal         # PDF
./menu.sh word skripsi         # Word
./menu.sh semua semua          # PDF + Word semua dokumen
./menu.sh semua contoh         # PDF + Word tiga dokumen contoh -> contoh/hasil/
./menu.sh peran                # atur pembimbing, penguji, ketua prodi, dekan
./menu.sh buka proposal | bersih | cek
```

Dokumen yang dapat dipilih: `pedoman`, `proposal`, `formulir`, `seminar-hasil`, `skripsi`, `semua` (template), `contoh` (tiga dokumen contoh; atau satu per satu: `contoh-proposal`, `contoh-hasil`, `contoh-skripsi`).
Hasil ada di `hasil/` (dokumen contoh di `contoh/hasil/`). Perlu: `xelatex`, `latexmk`, `pandoc`, `python3` (`./menu.sh cek`).

**Dosen dan peran:** daftar dosen ada di `common/dosen.tex`; peran (Pembimbing I/II, Penguji I/II, Ketua Prodi, Dekan) diatur sekali di `common/peran.tex` atau lewat `./menu.sh peran`, lalu otomatis dipakai di semua dokumen.

## Struktur

```text
common/      gaya bersama: skripsi.sty, skripsi-bab.sty, dosen.tex, peran.tex, atur_peran.py
pedoman/  proposal/  seminar-hasil/  skripsi/  formulir/    sumber dokumen (isi per bab di bab/)
contoh/      dokumen contoh terisi (proposal, seminar-hasil, skripsi), gambar/, hasil/
panduan/     panduan penggunaan LaTeX
word/        buat_word.py (pembuat Word) dan filter.lua (filter pandoc)
gambar/      logo dan gambar contoh
hasil/       keluaran PDF/Word
```

Tambah bab baru: buat `bab/NN-nama.tex`, lalu `\input{bab/NN-nama}` di berkas utama.

## Catatan

- **Data pada `contoh/` fiktif** (nama, NPM, angka hasil, peran dosen) dan hanya memperagakan format.
- Daftar isi, daftar tabel, daftar gambar, dan daftar lampiran di Word berupa field: pilih **Yes/Ya** saat Word menawarkan memperbarui field (atau Ctrl+A, F9).
- Edit isi hanya di file `.tex`; PDF dan Word dibuat ulang dari sumber yang sama.
- Hindari `>{\centering}p{..}` di tabel (pandoc menghilangkan isi sel); pakai `c` atau `p{..}`.
- Jangan jalankan pandoc dengan `TEXINPUTS` terisi (pandoc akan membongkar `skripsi.sty`); `menu.sh`/`buat_word.py` sudah menanganinya.
- Isi Bab IV Pedoman (tata cara pengajuan, bimbingan, seminar, ujian) bersifat umum; sesuaikan dengan ketentuan Program Studi.

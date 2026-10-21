# Contoh dokumen terisi

Folder ini berisi **contoh hasil jadi** dari tiga dokumen: Proposal, Seminar Hasil, dan Skripsi,
agar tampilan akhirnya dapat dilihat langsung. Topik contoh: *Analisis Kinerja Algoritma Penjadwalan
Paket pada Jaringan LTE Menggunakan Simulator ns-3*.

> **Penting:** nama mahasiswa, NPM, alamat, **seluruh angka hasil simulasi**, dan peran dosen
> (pembimbing/penguji/ketua prodi) pada contoh ini **fiktif/ilustrasi** dan hanya untuk memperagakan
> format. Referensi pada daftar pustaka adalah sumber nyata, tetapi ringkasannya sebatas contoh.
> Jangan disalin sebagai isi skripsi.

## Isi

| Folder | Keterangan |
|---|---|
| `proposal/` | Proposal: sampul, persetujuan, abstrak, daftar isi, Bab I–III, jadwal, daftar pustaka |
| `seminar-hasil/` | Seminar hasil: Bab I–V, daftar pustaka, lampiran |
| `skripsi/` | Skripsi lengkap: sampul, pengesahan, keaslian, abstrak, kata pengantar, daftar isi/tabel/gambar, Bab I–V, daftar pustaka, lampiran |
| `gambar/` | Gambar contoh (diagram alir, topologi, grafik) dan sumbernya `buat-gambar.tex` |
| `hasil/` | **PDF dan Word siap lihat** (`proposal`, `seminar-hasil`, `skripsi`) |

Setiap dokumen memakai gaya yang sama dengan templatenya (`../common/`), sehingga bisa dipakai sebagai
acuan penulisan: sitasi gaya APA di kalimat, tabel dan gambar bernomor per bab, persamaan, daftar pustaka.

## Membuat ulang

Dari folder utama:

```bash
./menu.sh semua contoh      # PDF + Word ketiganya  -> contoh/hasil/
./menu.sh pdf contoh-skripsi
./menu.sh word contoh-proposal
./menu.sh buka contoh
```

Atau menu interaktif `./menu.sh`, pilih dokumen nomor 7.
Pada berkas Word, buka lalu pilih *Ya/Yes* bila diminta memperbarui field agar daftar isi terisi.

## Mengganti gambar contoh

```bash
cd contoh/gambar
xelatex buat-gambar.tex
pdftoppm -r 250 -png buat-gambar.pdf hasil   # lalu ganti nama sesuai keperluan
```

---
title: "Panduan Penggunaan LaTeX untuk Penulisan Skripsi"
subtitle: "Program Studi Rekayasa Sistem Komputer, Fakultas Teknik, Universitas Muhammadiyah Buton"
---

# 1. Gambaran singkat

Semua dokumen (pedoman, proposal, seminar hasil, skripsi, formulir judul) ditulis dalam **LaTeX**. Dari satu sumber yang sama Anda bisa menghasilkan:

- **PDF** (tata letak persis sesuai pedoman), dan
- **Word (.docx)** (untuk diedit atau diserahkan dalam format Word).

Anda **cukup mengedit berkas `.tex`**. PDF dan Word dibuat otomatis lewat menu, tidak perlu diatur ulang margin, spasi, atau nomor halamannya.

## Struktur folder

```
panduan-skripsi/
├── menu.sh                  <- menu pembuat PDF / Word
├── hasil/                   <- keluaran: *.pdf dan *.docx
├── skripsi/                 <- format skripsi
│   ├── skripsi.tex            berkas utama (sampul, halaman depan, daftar bab)
│   └── bab/                   satu berkas per bab
├── seminar-hasil/           <- format seminar hasil (struktur sama)
├── proposal/                <- template proposal
│   ├── proposal.tex
│   └── bab/
├── pedoman/pedoman.tex      <- pedoman penulisan skripsi
├── formulir/formulir.tex    <- formulir pengajuan judul
├── common/                  <- gaya & data bersama (jarang diubah)
│   ├── skripsi.sty, skripsi-bab.sty   tata letak
│   ├── dosen.tex                      daftar dosen
│   └── peran.tex                      pembimbing/penguji/dst.
├── gambar/                  <- logo & gambar
├── word/                    <- mesin konversi ke Word
└── panduan/                 <- panduan ini
```

# 2. Persiapan (sekali saja)

Dibutuhkan empat program. Periksa dengan:

```bash
./menu.sh cek
```

| Program | Fungsi | Cara memasang (macOS) |
|---|---|---|
| `xelatex`, `latexmk` | membuat PDF | `brew install --cask mactex-no-gui` |
| `pandoc` | konversi ke Word | `brew install pandoc` |
| `python3` | pendukung konversi Word | bawaan macOS |

Font **Times New Roman** dipakai bila tersedia; jika tidak, otomatis diganti *TeX Gyre Termes* yang bentuknya serupa.

# 3. Cara membuat PDF dan Word

## Lewat menu (disarankan)

```bash
cd panduan-skripsi
./menu.sh
```

Pilih: **1** Buat PDF, **2** Convert ke Word, **3** keduanya, lalu pilih dokumen. Hasil ada di folder `hasil/`.

## Lewat perintah langsung

```bash
./menu.sh pdf skripsi        # PDF skripsi
./menu.sh word skripsi       # Word skripsi
./menu.sh semua skripsi      # PDF + Word
./menu.sh semua semua        # semua dokumen
./menu.sh buka skripsi       # membuka hasilnya
./menu.sh bersih             # menghapus berkas sementara
```

Nama dokumen: `pedoman`, `proposal`, `formulir`, `seminar-hasil`, `skripsi`, atau `semua`.

## Membuat PDF tanpa menu

```bash
cd skripsi
TEXINPUTS="../common//:" latexmk -xelatex skripsi.tex
```

`TEXINPUTS` wajib agar LaTeX menemukan gaya di folder `common/`.

## Membuat PDF dari editor (VS Code, TeXstudio, dll.)

Tiap folder dokumen sudah berisi berkas `latexmkrc` yang mengatur `TEXINPUTS` dan memilih **XeLaTeX** otomatis. Jadi cukup **buka berkas utama** (`skripsi/skripsi.tex`, `proposal/proposal.tex`, dst.) lalu tekan tombol *Build* / *Compile*. Tidak perlu mengatur apa pun.

- Di **VS Code** pasang ekstensi *LaTeX Workshop*, buka berkas utama, lalu **Ctrl+Alt+B** (Cmd+Option+B). Pengaturan proyek sudah ada di `.vscode/settings.json`.
- Di **TeXstudio**, pilih *Tools → Commands → LaTeX* menjadi `latexmk` (bukan `pdflatex`) dan buka berkas utama.
- Selalu kompilasi **berkas utama**, bukan berkas di dalam `bab/`.
- PDF dari editor muncul di folder dokumennya (mis. `skripsi/skripsi.pdf`). Salinan rapi di `hasil/` dibuat lewat `./menu.sh`.

# 4. Struktur sebuah dokumen

Contoh `skripsi/skripsi.tex` (dipersingkat; proposal dan seminar hasil serupa):

```latex
\documentclass[12pt,a4paper]{report}
\usepackage{skripsi}          % font, bahasa, lingkungan khusus
\usepackage{skripsi-bab}      % margin, spasi, nomor halaman
\input{../common/dosen}       % data dosen
\input{../common/peran}       % peran dosen

\begin{document}
  ... sampul, halaman pengajuan, pengesahan, abstrak, kata pengantar ...
  \begin{daftarisi}\end{daftarisi}
  \begin{daftartabel}\end{daftartabel}
  \begin{daftargambar}\end{daftargambar}
  \begin{akhirdepan}\end{akhirdepan}   % halaman isi mulai dari angka 1
  \pagestyle{isi}
  \input{bab/01-pendahuluan}
  \input{bab/02-tinjauan-pustaka}
  ...
\end{document}
```

Setiap bab ada di berkas sendiri di folder `bab/`:

| Berkas | Isi |
|---|---|
| `01-pendahuluan.tex` | Bab I |
| `02-tinjauan-pustaka.tex` | Bab II |
| `03-metode-penelitian.tex` | Bab III |
| `04-hasil-pembahasan.tex` | Bab IV |
| `05-kesimpulan-saran.tex` | Bab V |
| `06-daftar-pustaka.tex` | Daftar Pustaka |
| `07-lampiran.tex` | Lampiran |

**Menambah bab/lampiran baru:** buat berkas baru di `bab/`, lalu tambahkan `\input{bab/nama-berkas}` pada berkas utama di urutan yang diinginkan.

# 5. Mengedit isi

## 5.1 Judul bab dan subbab

```latex
\chapter{PENDAHULUAN}              % BAB I  (judul ditulis HURUF BESAR)
\section{Latar Belakang}           % 1.1
\subsection{Teori Pertama}         % 1.1.1
\subsubsection{Rincian}            % 1.1.1.1 (miring)
\babtp{DAFTAR PUSTAKA}             % judul tanpa nomor, tetap masuk daftar isi
```

Nomor bab, subbab, dan daftar isi dibuat otomatis. Subbab ditulis dengan *Huruf Awal Kapital* setiap kata.

## 5.2 Paragraf dan teks

- Paragraf baru = **baris kosong** di antara dua paragraf. Jangan menekan spasi atau Tab untuk membuat alinea; menjorok 1,27 cm sudah otomatis.
- Cetak miring: `\textit{template}` (kata asing/Inggris/Latin ditulis miring, sesuai pedoman).
- Cetak tebal: `\textbf{penting}`.
- Kutipan: gunakan tanda kutip dua melengkung langsung, misalnya “seperti ini”.

## 5.3 Karakter khusus

Karakter berikut punya arti khusus di LaTeX, tulis dengan garis miring terbalik di depannya:

| Ketik | Hasil | Ketik | Hasil |
|---|---|---|---|
| `\%` | % | `\&` | & |
| `\#` | # | `\_` | _ |
| `\$` | $ | `\{ \}` | { } |

> **Peringatan:** tanda `%` yang tidak diberi `\` akan **menghapus sisa baris** (dianggap komentar). Tulis `5\%`, bukan `5%`.

Tanda `--` menghasilkan tanda hubung panjang (misalnya rentang halaman `264--269`).

## 5.4 Daftar (butir)

```latex
\begin{enumerate}        % bernomor 1. 2. 3.
\item Butir pertama.
\item Butir kedua.
\end{enumerate}

\begin{enumerate}[a.]    % huruf a. b. c.
\item ...
\end{enumerate}

\begin{itemize}          % butir berpoin
\item ...
\end{itemize}
```

## 5.5 Tabel

Judul tabel di **atas**, bentuk tabel **kotak penuh** (garis atas, bawah, kiri, kanan, dan antarbaris). Nomor otomatis mengikuti bab: tabel pertama di Bab IV bernomor **Tabel 4.1**, yang kedua **Tabel 4.2**, dan seterusnya (angka setelah titik adalah urutan di bab itu). Di lampiran nomornya berawalan nomor lampiran, mis. Tabel L2.1. Cara paling aman (dan terbaca baik di Word) memakai `longtable`:

```latex
\begin{singlespace}
\begin{longtable}{|p{0.32\linewidth}|p{0.28\linewidth}|p{0.28\linewidth}|}
\caption{Hasil pengujian sistem}\\
\hline
\textbf{Parameter} & \textbf{Hasil} & \textbf{Keterangan} \\
\hline
Latensi (ms) & 12,5 & Baik \\
\hline
Akurasi (\%) & 95,2 & Baik \\
\hline
\end{longtable}
\end{singlespace}
```

- Lebar kolom ditulis sebagai pecahan `\linewidth` (jumlah sekitar 0,9–1,0). Lebar ini ikut terbaca saat konversi ke Word.
- Isi tabel diketik satu spasi (`singlespace`).
- Angka desimal memakai **koma** (`12,5`), ribuan dengan titik (`1.000`).
- Sebut tabel di teks: "Tabel 1 menunjukkan ...".

## 5.6 Gambar

Judul gambar di **bawah**, nomor otomatis dengan aturan yang sama (Gambar 1.1 = gambar pertama di Bab I; di lampiran Gambar L2.1). Simpan berkas gambar di folder `gambar/` (format `.png` atau `.jpg`).

```latex
\begin{figure}[H]
\centering
\includegraphics[width=0.6\textwidth]{../gambar/grafik-hasil.png}
\caption{Grafik hasil pengujian}
\end{figure}
```

`[H]` menempatkan gambar tepat di posisinya. Atur ukuran dengan `width=0.6\textwidth` (60% lebar teks).

## 5.7 Persamaan

```latex
$ds = \sqrt{r^{2} + \left(\frac{dr}{d\theta}\right)^{2}}\, d\theta$
```

Di Word, persamaan menjadi objek persamaan yang dapat diedit.

## 5.8 Sitasi dan daftar pustaka (gaya APA edisi ke-7)

Sitasi di dalam teks ditulis langsung:

- satu penulis: Andrews (2007) atau (Andrews, 2007)
- dua penulis: (Xu \& Fischione, 2012)  → di LaTeX tulis `(Xu \& Fischione, 2012)`
- tiga penulis atau lebih: (Capozzi et al., 2013)

Daftar pustaka memakai lingkungan `pustaka`; **satu paragraf (dipisah baris kosong) = satu pustaka**, diurutkan abjad nama penulis pertama:

```latex
\babtp{DAFTAR PUSTAKA}
\begin{pustaka}
Andrews, M. (2007). A survey of scheduling theory in wireless data networks.
\textit{Wireless Communications, 143}, 1--17.

Ghosh, A., Zhang, J., Andrews, J. G., \& Muhamed, R. (2010).
\textit{Fundamentals of LTE}. Prentice Hall.
\end{pustaka}
```

Judul buku/jurnal diberi cetak miring. Tanda `&` ditulis `\&`. Alamat web ditulis dengan `\url{...}`.

**Contoh untuk berbagai jenis sumber** (lengkapnya ada di berkas daftar pustaka tiap dokumen, `bab/05-` atau `bab/06-daftar-pustaka.tex`; hapus yang tidak dipakai):

| Jenis | Pola |
|---|---|
| Buku | Penulis, A. (Tahun). *Judul buku*. Penerbit. |
| Buku terjemahan | Penulis, A. (Tahun). *Judul* (B. Penerjemah, Penerj.). Penerbit. |
| Bab dalam buku suntingan | Penulis, A. (Tahun). Judul bab. Dalam B. Editor (Ed.), *Judul buku* (hlm. 10--25). Penerbit. |
| Artikel jurnal | Penulis, A. (Tahun). Judul artikel. *Nama Jurnal, vol*(no), hlm--hlm. `\url{https://doi.org/...}` |
| Prosiding | Penulis, A. (Tahun). Judul makalah. *Nama Prosiding*, hlm--hlm. |
| Skripsi/tesis | Penulis, A. (Tahun). *Judul* [Skripsi, Nama Universitas]. Repositori. `\url{...}` |
| Laporan lembaga | Nama Lembaga. (Tahun). *Judul laporan*. Penerbit. |
| Lembar data / standar | Produsen. (Tahun). *Judul datasheet* (Versi x) [Lembar data]. `\url{...}` |
| Artikel daring | Penulis/Lembaga. (Tahun, tanggal). *Judul halaman*. Nama Situs. **Diakses pada 21 Oktober 2026, dari** `\url{...}` |
| Kode di repositori | Penulis. (Tahun). *Nama repo* [Kode sumber]. GitHub. **Diakses pada ..., dari** `\url{...}` |
| Tanpa penulis | *Judul*. (Tahun). Penerbit. |

**Sumber web wajib mencantumkan tanggal akses**, yaitu hari saat sumber dibuka, karena isinya bisa berubah. Tulis di akhir entri: `Diakses pada 21 Oktober 2026, dari \url{...}`. Artikel jurnal dengan DOI tidak perlu tanggal akses. Bila tahun tidak diketahui tulis `(t.t.)`.

Bentuk sitasi di dalam teks: Andrews (2007); (Xu \& Fischione, 2012); (Capozzi et al., 2013); (Badan Pusat Statistik, 1997); kutipan langsung dengan halaman (Ghosh et al., 2010, hlm. 15).

## 5.9 Lampiran

Tiap lampiran adalah judul tanpa nomor bab dengan format "LAMPIRAN n. judul":

```latex
\babtp{LAMPIRAN 2. Daftar pertanyaan wawancara}
Isi lampiran ...
```

# 6. Mengisi data sampul

Ganti teks berikut langsung di berkas `.tex` utama (bagian sampul dan halaman pengajuan):

- `JUDUL SKRIPSI` / `JUDUL PENELITIAN` → judul Anda (huruf besar)
- `NAMA MAHASISWA` dan `NPM`
- `202x` → tahun

Gunakan *Cari & Ganti* di editor agar semua kemunculan terganti sekaligus.

# 7. Dosen dan peran (pembimbing, penguji, dst.)

Daftar dosen ada di `common/dosen.tex` (nama, gelar, NIDN). Peran tiap dosen diatur **sekali** dan otomatis dipakai di sampul, lembar persetujuan/pengesahan, kata pengantar, dan abstrak semua dokumen.

**Cara termudah:**

```bash
./menu.sh peran
```

(atau menu nomor **7**). Ketik nomor dosen untuk tiap peran: Pembimbing I, Pembimbing II, Penguji I, Penguji II, Ketua Program Studi, Dekan. Tekan Enter untuk membiarkan, `0` untuk mengosongkan. Setelah itu buat ulang dokumen (menu PDF/Word).

**Cara manual:** edit `common/peran.tex`:

```latex
\newcommand{\PembimbingI}{\dsnAwaluddin}\newcommand{\PembimbingInidn}{\nidnAwaluddin}
```

**Menambah dosen baru:** salin dua baris di `common/dosen.tex` dengan kunci baru:

```latex
\newcommand{\dsnBudi}{Budi Santoso, S.T., M.T.}
\newcommand{\nidnBudi}{0912345678}
```

# 8. Aturan format yang sudah otomatis

Anda tidak perlu mengatur hal-hal ini secara manual:

| Hal | Pengaturan |
|---|---|
| Kertas | A4 |
| Margin (proposal, seminar hasil, skripsi, pedoman) | kiri 4, atas 4, kanan 3, bawah 3 cm |
| Huruf | Times New Roman 12 pt |
| Spasi isi | proposal, seminar hasil, skripsi: 1,5 spasi (pedoman: 2 spasi); judul tabel/gambar, lampiran, daftar pustaka 1 spasi |
| Alinea | menjorok 1 cm (pedoman: 1,27 cm), rata kanan-kiri |
| Nomor halaman | awal bab: tengah bawah; halaman berikutnya: kanan atas; bagian depan angka romawi |
| Penomoran | bab (I, II, ...), subbab (1.1, 1.1.1), tabel dan gambar per bab (Gambar 1.1, Tabel 2.3) |
| Daftar isi, tabel, gambar | dibuat otomatis |

Proposal, seminar hasil, dan skripsi memakai ukuran, sampul, halaman depan, dan gaya bab yang sama; yang berbeda hanya tulisannya. Judul bab ditulis "BAB I" di tengah lalu judulnya, dan **setiap bab mulai di halaman baru** (halaman pertama bab bernomor tengah bawah, halaman berikutnya kanan atas).

# 9. Konversi ke Word

Setelah memilih **Convert ke Word**, berkas `.docx` muncul di `hasil/`. Perhatikan:

1. Saat membuka di Word, pilih **Yes/Ya** bila ditanya memperbarui field. Ini mengisi **Daftar Isi, Daftar Tabel, dan Daftar Gambar**. Jika belum terisi: klik kanan tulisan di daftar → *Update Field* → *Update entire table*.
2. Pengaturan gaya ada di *Styles* Word (Heading 1–4, Body Text, Table Caption, dst.); mengubah gaya akan mengubah seluruh dokumen.
3. Jangan menghapus *section break* antar bab di skripsi dan seminar hasil; di situlah aturan nomor halaman per bab bekerja.
4. **Edit isi sebaiknya tetap di `.tex`**, lalu konversi ulang. Mengedit langsung di Word hanya untuk penyesuaian akhir; perubahan di Word tidak kembali ke `.tex`.

**Batasan konversi** (agar hasil Word tetap rapi):

- Gunakan lingkungan standar yang ada di contoh (`longtable`, `figure`, `enumerate`, `pustaka`, dst.).
- Hindari spesifikasi kolom berbentuk `>{\centering\arraybackslash}p{...}` pada tabel isi; isi sel bisa hilang di Word. Gunakan kolom `c`, `l`, `r`, atau `p{...}`.
- Gambar yang dibuat dengan kode (TikZ/PGF) tidak ikut ke Word; simpan sebagai `.png` terlebih dahulu.
- Perintah pengatur tata letak murni (`\vspace`, `\hspace`, `\newpage`) tidak berpengaruh di Word. Gunakan lingkungan khusus di bawah ini.

# 10. Lingkungan khusus yang tersedia

| Lingkungan | Fungsi |
|---|---|
| `tengah` | blok rata tengah satu spasi (sampul, judul halaman) |
| `kanan` | blok digeser ke kanan (penutup kata pengantar, tanda tangan) |
| `pustaka` | daftar pustaka (baris kedua menjorok, 1 spasi) |
| `tanpagaris` | tabel tanpa garis (tanda tangan, data) |
| `tabelpusat` | semua kolom tabel di dalamnya rata tengah (khusus Word) |
| `ruang` | jarak kosong vertikal, mis. `\begin{ruang}{2}\end{ruang}` = 2 cm |
| `daftarisi`, `daftartabel`, `daftargambar` | membuat daftar otomatis |
| `akhirsampul`, `akhirdepan` | penanda pergantian bagian (nomor halaman) |
| `halamanbaru` | pindah halaman (di Word jadi *page break*) |

# 11. Pemecahan masalah

| Gejala | Penyebab / solusi |
|---|---|
| `File 'skripsi.sty' not found` | LaTeX dijalankan di luar folder dokumen atau tanpa `latexmk`. Kompilasi **berkas utama** dengan `latexmk` (editor) atau pakai `./menu.sh` (bagian 3). |
| `fontspec ... requires XeTeX or LuaTeX` | editor memakai pdfLaTeX. Ganti ke `latexmk` (XeLaTeX); jangan pakai tombol *pdfLaTeX* langsung. |
| Berkas di dalam `bab/` dikompilasi sendiri dan galat | kompilasi berkas utama, bukan berkas bab. |
| `Undefined control sequence` | salah ketik perintah, atau lupa `\` pada karakter khusus (bagian 5.3). Lihat nomor baris pada pesan galat. |
| Kalimat tiba-tiba terpotong | ada `%` tanpa `\` di baris itu. Tulis `\%`. |
| Daftar isi kosong / nomor halaman salah | jalankan pembuatan PDF sekali lagi (daftar butuh dua putaran; menu sudah mengulang otomatis). |
| Daftar isi di Word hanya tulisan "Klik kanan..." | belum diperbarui; lihat bagian 9 butir 1. |
| Gambar tidak muncul | periksa nama dan lokasi berkas di `gambar/`; nama berkas peka huruf besar-kecil. |
| Teks tabel hilang di Word | hindari `>{\centering...}`, lihat bagian 9. |
| Menu: "gagal membuat PDF" | buka `build/<dokumen>-latex.log`; galat pertama diawali tanda `!`. |
| Menu: "gagal membuat Word" | buka `build/<dokumen>-word.log`. |
| Hasil tidak berubah | pastikan berkas yang diedit adalah berkas bab yang dipanggil `\input`, lalu buat ulang dokumen. |

# 12. Ringkasan alur kerja

1. Isi sampul dan data (bagian 6); atur dosen/peran (`./menu.sh peran`).
2. Tulis isi tiap bab di `bab/NN-....tex` (bagian 5).
3. Simpan gambar di `gambar/`.
4. `./menu.sh semua skripsi` → periksa `hasil/skripsi.pdf` dan `hasil/skripsi.docx`.
5. Perbaiki di `.tex`, ulangi langkah 4 sampai siap dikumpulkan.

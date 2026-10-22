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
├── contoh/                  <- contoh terisi (proposal, seminar hasil, skripsi) + PDF/Word di contoh/hasil
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
  \begin{daftarlampiran}\end{daftarlampiran}   % skripsi dan seminar hasil
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

## 7.1 Daftar dosen

Satu dosen memiliki dua makro: `\dsn` + kunci (nama dan gelar) dan `\nidn` + kunci (NIDN). *Kunci* adalah singkatan yang dipakai di `peran.tex`. Nomor pada kolom pertama adalah nomor yang diketik di menu pengaturan peran (urutannya mengikuti isi `dosen.tex`).

| No | Nama dan gelar | NIDN | Kunci |
|---|---------------------------------------------|------------------|-----------|
| 1 | Muhammad Awaluddin, S.Kom., M.Kom | 0909038201 | Awaluddin |
| 2 | Darmawan, S.Kom., M.Kom | 0911048204 | Darmawan |
| 3 | Rando, S.Kom., M.Eng. | 0911069501 | Rando |
| 4 | La Ode Muhammad Saidi, S.Si., M.Kom | 0913038905 | Saidi |
| 5 | Didin Adri, S.Si., M.Sc | 0930088802 | Didin |
| 6 | Muhammad Hibrian Wiwi, S.T., M.Kom | 0930129003 | Hibrian |
| 7 | Muhammad Abdur Rasyid Asruddin, S.T., M.Kom | 6641774675130242 | Rasyid |
| 8 | Agusman, S.T., M.M (Dekan Fakultas Teknik) | 0917088206 | Agusman |

Contoh pemakaian kunci: untuk Awaluddin makro namanya `\dsnAwaluddin` dan makro NIDN-nya `\nidnAwaluddin`.

Dekan Fakultas Teknik sudah terisi tetap (Agusman, S.T., M.M) di `peran.tex`. Bila ada pergantian dekan, tambahkan dosen barunya (7.4) lalu pilih lewat menu.

## 7.2 Daftar peran

Ada enam peran. Nama makronya dipakai di berkas `.tex`, dan di menu muncul dengan nama biasa:

| Peran di menu | Makro nama | Makro NIDN | Dipakai di |
|---|---|---|---|
| Pembimbing I | `\PembimbingI` | `\PembimbingInidn` | lembar persetujuan, pengesahan, kata pengantar |
| Pembimbing II | `\PembimbingII` | `\PembimbingIInidn` | lembar persetujuan, pengesahan, kata pengantar |
| Penguji I | `\PengujiI` | `\PengujiInidn` | halaman pengesahan, kata pengantar |
| Penguji II | `\PengujiII` | `\PengujiIInidn` | halaman pengesahan, kata pengantar |
| Ketua Program Studi | `\KetuaProdi` | `\KetuaProdinidn` | halaman pengesahan, kata pengantar |
| Dekan Fakultas Teknik | `\Dekan` | `\Dekannidn` | halaman pengesahan, kata pengantar pedoman |

Peran yang belum dipilih tampil sebagai titik-titik isian (……) sehingga dapat ditulis tangan.

## 7.3 Mengatur peran

**Cara termudah:**

```bash
./menu.sh peran
```

(atau menu nomor **7** pada menu interaktif). Program menampilkan daftar dosen bernomor, lalu menanyakan satu per satu: Pembimbing I, Pembimbing II, Penguji I, Penguji II, Ketua Program Studi, dan Dekan. Ketik nomor dosen, tekan Enter untuk membiarkan pilihan yang ada, atau ketik `0` untuk mengosongkan. Berkas `common/peran.tex` ditulis ulang otomatis. Setelah itu buat ulang dokumen (menu PDF/Word).

**Cara manual:** edit `common/peran.tex`. Isi dengan kunci dosen dari tabel di atas. Contoh, Pembimbing I = Muhammad Awaluddin dan Pembimbing II = Darmawan:

```latex
\newcommand{\PembimbingI}{\dsnAwaluddin}\newcommand{\PembimbingInidn}{\nidnAwaluddin}
\newcommand{\PembimbingII}{\dsnDarmawan}\newcommand{\PembimbingIInidn}{\nidnDarmawan}
```

Nama pada lembar persetujuan dan pengesahan selalu tampil satu baris; bila terlalu panjang, ukuran hurufnya diperkecil otomatis (tidak pindah baris).

## 7.4 Menambah dosen baru

Salin dua baris di `common/dosen.tex` dengan kunci baru (tanpa spasi atau tanda baca), lalu isi nama dan NIDN:

```latex
\newcommand{\dsnBudi}{Budi Santoso, S.T., M.T.}
\newcommand{\nidnBudi}{0912345678}
```

Dosen baru otomatis muncul di daftar menu pengaturan peran (di urutan paling bawah), dan kuncinya dapat dipakai di `peran.tex`. Perbarui juga tabel 7.1 pada panduan ini bila perlu.

## 7.5 Peran pada folder contoh

Dokumen pada folder `contoh/` mengatur peran dosennya sendiri (hanya ilustrasi) lewat `\renewcommand` di berkas utamanya, sehingga `common/peran.tex` tidak berubah. Untuk dokumen sungguhan, cukup atur peran di `common/peran.tex` seperti di atas.

# 8. Formulir pengajuan judul

`formulir/formulir.tex` berisi formulir pengajuan judul penelitian (Arial 12). Strukturnya:

- **Kop dan identitas:** logo, judul formulir, lalu NPM/Nama, No. HP, dan Tanggal Pengajuan.
- **Tiga usulan judul**, masing-masing dibuat oleh satu perintah: `\usulan{1}`, `\usulan{2}`, `\usulan{3}`. Tiap usulan berupa **satu tabel kotak penuh** berisi: judul usulan, petunjuk penulisan judul (maksimum 15 kata), lalu enam bagian: (1) Objek/Tempat Penelitian, (2) Latar Belakang Masalah, (3) Rumusan Masalah, (4) Tujuan Penelitian, (5) Penelitian Terkait, dan (6) Daftar Pustaka. Setiap bagian terdiri dari satu baris judul (tebal) dan satu baris isian.
- **Hasil verifikasi:** kotak untuk Ketua Prodi/dosen verifikator, kotak dosen pembimbing I dan II, serta tanda tangan Ketua Prodi (nama dan NIDN diambil dari `common/peran.tex`).

Tiap usulan memakai halaman sendiri (`halamanbaru`) sehingga tidak ada kotak yang terpotong antarhalaman. Untuk mengubah teks petunjuk, edit definisi `\usulan` di bagian atas berkas; ketiga usulan ikut berubah. Membuatnya: `./menu.sh semua formulir`.

# 9. Aturan format yang sudah otomatis

Anda tidak perlu mengatur hal-hal ini secara manual:

| Hal | Pengaturan |
|---|---|
| Kertas | A4 |
| Margin (proposal, seminar hasil, skripsi, pedoman) | kiri 4, atas 4, kanan 3, bawah 3 cm |
| Huruf | Times New Roman 12 pt |
| Spasi isi | pedoman, proposal, seminar hasil, skripsi: 1,5 spasi; judul tabel/gambar, lampiran, daftar pustaka 1 spasi |
| Alinea | menjorok 1 cm, rata kanan-kiri |
| Nomor halaman | sampul, lembar persetujuan, pengesahan, dan pernyataan keaslian: tanpa nomor; abstrak sampai daftar lampiran: angka romawi (tengah bawah); isi: angka Arab, awal bab tengah bawah, halaman berikutnya kanan atas |
| Penomoran | bab (I, II, ...), subbab (1.1, 1.1.1), tabel dan gambar per bab (Gambar 1.1, Tabel 2.3) |
| Daftar isi, tabel, gambar | dibuat otomatis |

Proposal, seminar hasil, dan skripsi memakai ukuran, sampul, halaman depan, dan gaya bab yang sama; yang berbeda hanya tulisannya. Judul bab ditulis "BAB I" di tengah lalu judulnya, dan **setiap bab mulai di halaman baru** (halaman pertama bab bernomor tengah bawah, halaman berikutnya kanan atas).

# 10. Konversi ke Word

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

# 11. Lingkungan khusus yang tersedia

| Lingkungan | Fungsi |
|---|---|
| `tengah` | blok rata tengah satu spasi (sampul, judul halaman) |
| `kanan` | blok digeser ke kanan (penutup kata pengantar, tanda tangan) |
| `pustaka` | daftar pustaka (baris kedua menjorok, 1 spasi) |
| `tanpagaris` | tabel tanpa garis (tanda tangan, data) |
| `tabelpusat` | semua kolom tabel di dalamnya rata tengah (khusus Word) |
| `ruang` | jarak kosong vertikal, mis. `\begin{ruang}{2}\end{ruang}` = 2 cm |
| `daftarisi`, `daftartabel`, `daftargambar`, `daftarlampiran` | membuat daftar otomatis (daftar lampiran diisi dari perintah `\lampiran{n}{judul}`) |
| `\satubaris{nama}` | nama (dosen) selalu satu baris; bila kepanjangan, huruf diperkecil otomatis |
| `akhirsampul`, `akhirdepan` | penanda pergantian bagian (nomor halaman) |
| `halamanbaru` | pindah halaman (di Word jadi *page break*) |

# 12. Pemecahan masalah

| Gejala | Penyebab / solusi |
|---|---|
| `File 'skripsi.sty' not found` | LaTeX dijalankan di luar folder dokumen atau tanpa `latexmk`. Kompilasi **berkas utama** dengan `latexmk` (editor) atau pakai `./menu.sh` (bagian 3). |
| `fontspec ... requires XeTeX or LuaTeX` | editor memakai pdfLaTeX. Ganti ke `latexmk` (XeLaTeX); jangan pakai tombol *pdfLaTeX* langsung. |
| Berkas di dalam `bab/` dikompilasi sendiri dan galat | kompilasi berkas utama, bukan berkas bab. |
| `Undefined control sequence` | salah ketik perintah, atau lupa `\` pada karakter khusus (bagian 5.3). Lihat nomor baris pada pesan galat. |
| Kalimat tiba-tiba terpotong | ada `%` tanpa `\` di baris itu. Tulis `\%`. |
| Daftar isi kosong / nomor halaman salah | jalankan pembuatan PDF sekali lagi (daftar butuh dua putaran; menu sudah mengulang otomatis). |
| Daftar isi di Word hanya tulisan "Klik kanan..." | belum diperbarui; lihat bagian 10 butir 1. |
| Gambar tidak muncul | periksa nama dan lokasi berkas di `gambar/`; nama berkas peka huruf besar-kecil. |
| Teks tabel hilang di Word | hindari `>{\centering...}`, lihat bagian 10. |
| Menu: "gagal membuat PDF" | buka `build/<dokumen>-latex.log`; galat pertama diawali tanda `!`. |
| Menu: "gagal membuat Word" | buka `build/<dokumen>-word.log`. |
| Hasil tidak berubah | pastikan berkas yang diedit adalah berkas bab yang dipanggil `\input`, lalu buat ulang dokumen. |

# 13. Ringkasan alur kerja

1. Isi sampul dan data (bagian 6); atur dosen/peran (`./menu.sh peran`).
2. Tulis isi tiap bab di `bab/NN-....tex` (bagian 5).
3. Simpan gambar di `gambar/`.
4. `./menu.sh semua skripsi` → periksa `hasil/skripsi.pdf` dan `hasil/skripsi.docx`.
5. Perbaiki di `.tex`, ulangi langkah 4 sampai siap dikumpulkan.

# 14. Hasil analisis dokumen asli (kesesuaian format)

Dokumen asli yang dianalisis: *Pedoman Penulisan Skripsi*, *Template Proposal Skripsi*, dan *Formulir Pengajuan Judul* (berkas Word/PDF dari Prodi). Pengukuran dilakukan pada PDF-nya (ukuran kertas, margin, jenis huruf, jarak baris) lalu dibandingkan dengan aturan yang tertulis di Pedoman. Hasilnya dipakai untuk menetapkan format di folder ini.

## 14.1 Temuan pada dokumen asli

| No | Dokumen asli | Temuan | Keputusan pada template ini |
|--|-------|----------------------------|------------------------------|
| 1 | Pedoman | Margin tertulis kiri 4, kanan 3, bawah 3, **atas 3** cm | Margin **4/4/3/3** (kiri/atas/kanan/bawah) pada semua dokumen |
| 2 | Pedoman | Jarak baris teks tertulis **2 spasi** (isi PDF-nya memang 2 spasi), sedangkan Template Proposal memakai **1,5 spasi** | **1,5 spasi** untuk Pedoman, Proposal, Seminar Hasil, Skripsi; judul tabel/gambar, abstrak, daftar, daftar pustaka, lampiran 1 spasi |
| 3 | Pedoman | Alinea "tab stop 1,5" tanpa satuan jelas | Alinea menjorok **1 cm** |
| 4 | Pedoman | Penomoran gambar "Gambar 1." (urut), sedangkan Template Proposal "Tabel 2.1 / Gambar 2.1" (per bab) | Nomor **per bab** (Gambar 1.1, Tabel 2.3); lampiran memakai awalan lampiran (Tabel L2.1) |
| 5 | Pedoman | Penulisan mahasiswa memakai "NIM" | Diganti **NPM** di semua dokumen |
| 6 | Pedoman | Tidak ada aturan nomor halaman (hanya urutan lembar); judul tabel tidak ditegaskan posisinya | Ditetapkan: sampul, persetujuan, pengesahan, keaslian tanpa nomor; abstrak sampai daftar lampiran romawi; isi arab; awal bab tengah bawah, halaman berikutnya kanan atas; judul tabel **atas-tengah**, judul gambar **bawah-tengah** |
| 7 | Pedoman | Daftar urutan lembar memuat **Daftar Lampiran**, tetapi contohnya tidak diwajibkan di template | **Daftar Lampiran** ditambahkan pada Skripsi dan Seminar Hasil (dibuat otomatis dari `\lampiran{n}{judul}`) |
| 8 | Pedoman | Daftar pustaka bergaya Harvard lama ("Nama. Tahun. Judul."); Template Proposal menyebut **IEEE** | **APA edisi ke-7** (penulis--tahun) untuk semua dokumen, lengkap dengan tanggal akses untuk sumber web |
| 9 | Pedoman | Istilah tidak seragam: "Halaman Pengajuan" vs "Halaman Persetujuan"; bab penutup tertulis "BAB KESIMPULAN" tanpa angka; salah ketik ("sampur", "dengari", "Flow Chat") | Istilah diseragamkan: *Lembar Persetujuan* dan *Halaman Pengesahan*; bab ditulis "BAB V KESIMPULAN DAN SARAN"; salah ketik dibenahi |
| 10 | Template Proposal | Teks menyebut margin 2/2/2/2,5 cm dan pengukuran PDF 2,5 (kiri) / 2 (kanan) cm; bukan margin Pedoman | Margin **4/4/3/3** |
| 11 | Template Proposal | Desimal ditulis titik ("0.25") bertentangan dengan Pedoman (koma) | Desimal **koma** ("0,25") |
| 12 | Template Proposal | Judul bab "1. PENDAHULUAN"; tiap bab tidak selalu di halaman baru | "BAB I" + judul, **tiap bab di halaman baru** |
| 13 | Template Proposal | Tidak ada abstrak dan daftar isi; tabel tanpa garis penuh; jadwal bertahun "2018" | Ditambah **abstrak (Indonesia dan Inggris)** dan **daftar isi/tabel/gambar**; tabel **kotak penuh**; tahun jadwal "202x" |
| 14 | Template Proposal | Proposal terdiri atas empat bab (jadwal sebagai bab sendiri) | Proposal **hanya sampai Bab III**; jadwal pelaksanaan menjadi subbab Bab III |
| 15 | Template Proposal | Salah ketik ("propopsal", "gabar", "Tinjuan", "junal") | Dibenahi |
| 16 | Formulir | Ukuran kertas **Letter** (bukan A4), huruf Calibri padahal petunjuknya Arial, margin 2,5/1,9 cm | **A4**, **Arial**, margin seragam |
| 17 | Formulir | Kotak terpotong antarhalaman, judul bagian tertinggal di dasar halaman, penomoran daftar "1., 2., 3." berlanjut pada usulan 2 dan 3 | Satu tabel kotak penuh per usulan, satu halaman per usulan, penomoran tidak berlanjut |
| 18 | Formulir | "NIM", salah ketik ("dtulis", "d Bold", "masing-2", "Um. Buton") | "NPM", ejaan dan penulisan "UM Buton" dibenahi |

## 14.2 Daftar periksa kesesuaian (hasil pemeriksaan otomatis)

Pemeriksaan berikut dijalankan pada seluruh PDF hasil (Pedoman, Proposal, Seminar Hasil, Skripsi, dan contohnya):

| Aturan Pedoman | Status |
|------------------------------|--------------------|
| Kertas A4 | sesuai (juga pada berkas Word) |
| Margin 4/4/3/3 cm; teks, tabel, gambar tidak melewati margin | sesuai |
| Huruf Times New Roman 12 pt; judul bab 14 pt tebal kapital | sesuai (rumus memakai TeX Gyre Termes Math agar serasi) |
| Isi 1,5 spasi; abstrak, judul tabel/gambar, isi tabel, daftar, daftar pustaka, lampiran 1 spasi | sesuai |
| Rata kanan-kiri; alinea menjorok 1 cm | sesuai |
| Satu baris sendirian di awal/akhir halaman tidak boleh | sesuai (`\widowpenalty` dan `\clubpenalty` 10000) |
| Setiap bab mulai di halaman baru; judul subbab tidak sendirian di dasar halaman | sesuai |
| Tidak ada subbab tunggal (1.1 harus disertai 1.2) | sesuai pada semua dokumen |
| Tabel tidak terpotong antarhalaman (kecuali tabel panjang di lampiran) | sesuai; satu tabel panjang di Lampiran 6 Pedoman dibenarkan Pedoman |
| Judul tabel di atas, judul gambar di bawah, tanpa titik di akhir judul | sesuai |
| Nomor halaman: awal bab tengah bawah, selanjutnya kanan atas; depan romawi | sesuai |
| Nama pada lembar persetujuan/pengesahan satu baris | sesuai |

**Catatan keterbatasan:** tampilan berkas Word (`.docx`) diperiksa lewat struktur isinya (ukuran kertas, margin, huruf, gaya paragraf) dan tidak dirender ulang pada pengerjaan terakhir. Setelah membuka berkas Word, perbarui *field* (Ctrl+A, F9) agar daftar isi, daftar tabel, daftar gambar, dan daftar lampiran terisi, lalu periksa sekilas pemenggalan halaman.

Isi Bab IV Pedoman (tata cara pengajuan judul, bimbingan, seminar, dan ujian) bersifat umum karena Pedoman asli berhenti pada bab "Penutup". **Sesuaikan dengan ketentuan Program Studi** sebelum diberlakukan.


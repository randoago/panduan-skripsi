#!/usr/bin/env bash
# menu.sh -- menu untuk membuat PDF (LaTeX) dan Word (.docx) dari dokumen skripsi.
#
# Pemakaian interaktif :  ./menu.sh
# Pemakaian langsung   :  ./menu.sh pdf|word|semua|buka|bersih|cek  [pedoman|proposal|formulir|seminar-hasil|skripsi|semua]
#                         contoh:  ./menu.sh word proposal

set -u
cd "$(dirname "$0")"
ROOT="$(pwd)"
export TEXINPUTS="$ROOT/common//:${TEXINPUTS:-}"

DOKUMEN=(pedoman proposal formulir seminar-hasil skripsi)
# (macOS memakai bash 3.2: tanpa array asosiatif)
judul() {
  case "$1" in
    pedoman) echo "Pedoman Penulisan Skripsi";;
    proposal) echo "Template Proposal Skripsi";;
    formulir) echo "Formulir Pengajuan Judul";;
    seminar-hasil) echo "Format Seminar Hasil";;
    skripsi) echo "Format Skripsi";;
  esac
}

# ---------- tampilan ----------
if [ -t 1 ]; then B=$'\033[1m'; G=$'\033[32m'; R=$'\033[31m'; Y=$'\033[33m'; N=$'\033[0m'; else B=; G=; R=; Y=; N=; fi
ok()   { echo "${G}✔${N} $*"; }
gagal(){ echo "${R}✘${N} $*"; }
info() { echo "${Y}•${N} $*"; }

# ---------- pekerjaan ----------
cek_alat() {
  local semua=0
  for t in xelatex latexmk pandoc python3; do
    if command -v "$t" >/dev/null 2>&1; then ok "$t  ($(command -v "$t"))"
    else gagal "$t belum terpasang"; semua=1; fi
  done
  [ $semua -ne 0 ] && {
    echo
    info "Pasang yang kurang:  brew install pandoc   |   brew install --cask mactex-no-gui"
  }
  return $semua
}

buat_pdf() {  # $1 = nama dokumen
  local d="$1"
  info "PDF  ← $d  ($(judul "$d"))"
  if ! command -v latexmk >/dev/null 2>&1; then gagal "latexmk tidak ditemukan"; return 1; fi
  ( cd "$ROOT/$d" && latexmk -xelatex -interaction=nonstopmode -halt-on-error "$d.tex" >"$ROOT/build/$d-latex.log" 2>&1 )
  if [ -f "$ROOT/$d/$d.pdf" ] && ! grep -q '^!' "$ROOT/build/$d-latex.log"; then
    mkdir -p "$ROOT/hasil"; cp "$ROOT/$d/$d.pdf" "$ROOT/hasil/$d.pdf"
    ok "hasil/$d.pdf"
  else
    gagal "gagal membuat PDF — lihat build/$d-latex.log"; grep -m3 -A3 '^!' "$ROOT/build/$d-latex.log"; return 1
  fi
}

buat_word() {  # $1 = nama dokumen
  local d="$1"
  info "Word ← $d  ($(judul "$d"))"
  mkdir -p "$ROOT/hasil"
  if python3 "$ROOT/word/buat_word.py" "$d" -o "$ROOT/hasil/$d.docx" >/dev/null 2>"$ROOT/build/$d-word.log"; then
    ok "hasil/$d.docx"
    [ "$d" = pedoman ] && info "Buka di Word lalu pilih 'Yes/Ya' bila diminta memperbarui field (agar Daftar Isi terisi)."
  else
    gagal "gagal membuat Word — lihat build/$d-word.log"; tail -5 "$ROOT/build/$d-word.log"; return 1
  fi
}

untuk_dokumen() {  # $1 = fungsi, $2 = nama dokumen atau 'semua'
  local fn="$1" d="$2"
  mkdir -p "$ROOT/build"
  if [ "$d" = "semua" ]; then
    for x in "${DOKUMEN[@]}"; do "$fn" "$x"; done
  else
    "$fn" "$d"
  fi
}

buka_hasil() {  # $1 = dokumen
  local d="$1"
  local f
  for f in "$ROOT/hasil/$d.docx" "$ROOT/hasil/$d.pdf"; do
    [ -f "$f" ] && { open "$f" && ok "dibuka: ${f#$ROOT/}"; }
  done
  [ -f "$ROOT/hasil/$d.docx" ] || [ -f "$ROOT/hasil/$d.pdf" ] || gagal "belum ada hasil untuk $d — buat dulu."
}

bersih() {
  for d in "${DOKUMEN[@]}"; do
    ( cd "$ROOT/$d" && latexmk -C >/dev/null 2>&1; rm -f "$d.xdv" "$d.toc" )
  done
  rm -rf "$ROOT/build"
  ok "berkas sementara dihapus (folder hasil/ dibiarkan)"
}

# ---------- pilih dokumen ----------
pilih_dokumen() {
  echo >&2
  echo "${B}Pilih dokumen:${N}" >&2
  echo "  1) $(judul pedoman)" >&2
  echo "  2) $(judul proposal)" >&2
  echo "  3) $(judul formulir)" >&2
  echo "  4) $(judul seminar-hasil)" >&2
  echo "  5) $(judul skripsi)" >&2
  echo "  6) Semua dokumen" >&2
  read -r -p "Nomor [6]: " n
  case "${n:-6}" in
    1) echo pedoman;; 2) echo proposal;; 3) echo formulir;; 4) echo seminar-hasil;; 5) echo skripsi;; 6) echo semua;;
    *) echo semua;;
  esac
}

# ---------- mode perintah langsung ----------
if [ $# -ge 1 ]; then
  aksi="$1"; dok="${2:-semua}"
  case "$dok" in pedoman|proposal|formulir|seminar-hasil|skripsi|semua) ;; *) echo "dokumen tidak dikenal: $dok"; exit 2;; esac
  case "$aksi" in
    pdf)    untuk_dokumen buat_pdf  "$dok";;
    word)   untuk_dokumen buat_word "$dok";;
    semua)  untuk_dokumen buat_pdf "$dok"; untuk_dokumen buat_word "$dok";;
    buka)   [ "$dok" = semua ] && for x in "${DOKUMEN[@]}"; do buka_hasil "$x"; done || buka_hasil "$dok";;
    bersih) bersih;;
    cek)    cek_alat;;
    peran)  python3 "$ROOT/common/atur_peran.py";;
    *) echo "aksi tidak dikenal: $aksi  (pdf|word|semua|buka|bersih|cek)"; exit 2;;
  esac
  exit $?
fi

# ---------- menu interaktif ----------
while true; do
  echo
  echo "${B}═══════════════ MENU DOKUMEN SKRIPSI — FT UM Buton ═══════════════${N}"
  echo "  1) Buat PDF            (LaTeX → PDF)"
  echo "  2) Convert ke Word     (LaTeX → .docx)"
  echo "  3) Buat PDF + Word"
  echo "  4) Buka hasil          (hasil/*.docx, hasil/*.pdf)"
  echo "  5) Cek alat yang dibutuhkan"
  echo "  6) Bersihkan berkas sementara"
  echo "  7) Atur dosen / peran  (pembimbing, penguji, ketua prodi, dekan)"
  echo "  0) Keluar"
  read -r -p "Pilihan: " p
  case "$p" in
    1) d=$(pilih_dokumen); untuk_dokumen buat_pdf  "$d";;
    2) d=$(pilih_dokumen); untuk_dokumen buat_word "$d";;
    3) d=$(pilih_dokumen); untuk_dokumen buat_pdf "$d"; untuk_dokumen buat_word "$d";;
    4) d=$(pilih_dokumen); if [ "$d" = semua ]; then for x in "${DOKUMEN[@]}"; do buka_hasil "$x"; done; else buka_hasil "$d"; fi;;
    5) cek_alat;;
    6) bersih;;
    7) python3 "$ROOT/common/atur_peran.py";;
    0|q|Q) echo "Sampai jumpa."; exit 0;;
    *) gagal "pilihan tidak dikenal";;
  esac
done

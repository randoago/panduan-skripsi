#!/usr/bin/env python3
"""Atur peran dosen (pembimbing, penguji, ketua prodi, dekan) -> menulis ulang common/peran.tex.
Dipanggil dari menu.sh; berjalan interaktif. Data dosen dibaca dari common/dosen.tex."""
import re
from pathlib import Path

COMMON = Path(__file__).resolve().parent
PERAN = [("PembimbingI", "Pembimbing I"), ("PembimbingII", "Pembimbing II"),
         ("PengujiI", "Penguji I"), ("PengujiII", "Penguji II"),
         ("KetuaProdi", "Ketua Program Studi"), ("Dekan", "Dekan Fakultas Teknik")]
TITIK = "…………………"
TITIK_N = "…………………"


def baca_dosen():
    s = (COMMON / "dosen.tex").read_text(encoding="utf8")
    nama = dict(re.findall(r"\\newcommand\{\\dsn(\w+)\}\{([^}]*)\}", s))
    nidn = dict(re.findall(r"\\newcommand\{\\nidn(\w+)\}\{([^}]*)\}", s))
    return [(k, nama[k], nidn.get(k, "")) for k in nama]


def baca_peran():
    s = (COMMON / "peran.tex").read_text(encoding="utf8")
    cur = {}
    for key, _ in PERAN:
        m = re.search(r"\\newcommand\{\\%s\}\{\\dsn(\w+)\}" % key, s)
        cur[key] = m.group(1) if m else None
    return cur


def tulis(pilih):
    out = [
        "% =====================================================================",
        "%  PERAN DOSEN  --  dipakai otomatis di sampul, lembar persetujuan/pengesahan,",
        "%  kata pengantar, dan abstrak semua dokumen.",
        "%  Diatur lewat  ./menu.sh -> \"Atur dosen / peran\"  atau ubah manual dengan kunci dari dosen.tex",
        "%  (mis. \\dsnAwaluddin dan \\nidnAwaluddin).",
        "% =====================================================================",
    ]
    for key, _ in PERAN:
        k = pilih.get(key)
        if k:
            out.append("\\newcommand{\\%s}{\\dsn%s}\\newcommand{\\%snidn}{\\nidn%s}" % (key, k, key, k))
        else:
            out.append("\\newcommand{\\%s}{%s}\\newcommand{\\%snidn}{%s}" % (key, TITIK, key, TITIK_N))
    (COMMON / "peran.tex").write_text("\n".join(out) + "\n", encoding="utf8")


def main():
    dosen = baca_dosen()
    cur = baca_peran()
    print("\nDaftar dosen:")
    for i, (k, n, nd) in enumerate(dosen, 1):
        print("  %d) %s  (NIDN %s)" % (i, n, nd))
    print("\nPilih nomor dosen untuk tiap peran. Enter = tetap, 0 = kosongkan.\n")
    pilih = dict(cur)
    for key, label in PERAN:
        sekarang = next((n for k, n, _ in dosen if k == cur[key]), "(kosong)")
        ans = input("%-22s [%s]: " % (label, sekarang)).strip()
        if ans == "":
            continue
        if ans == "0":
            pilih[key] = None
        elif ans.isdigit() and 1 <= int(ans) <= len(dosen):
            pilih[key] = dosen[int(ans) - 1][0]
        else:
            print("  (nomor tidak valid, dilewati)")
    tulis(pilih)
    print("\ncommon/peran.tex diperbarui. Buat ulang dokumen dengan menu PDF/Word.")


if __name__ == "__main__":
    main()

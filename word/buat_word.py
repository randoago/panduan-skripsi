#!/usr/bin/env python3
"""Konversi dokumen LaTeX (pedoman / proposal / formulir) menjadi Word (.docx).

Alur:  1) buat reference.docx (gaya Word sesuai profil dokumen)
       2) pandoc  : .tex -> .docx  (dengan filter.lua)
       3) pasca-proses : section break, nomor halaman, margin, field daftar isi

Pemakaian:  python3 word/buat_word.py pedoman|proposal|formulir [-o hasil.docx]
Hanya memakai pustaka standar Python 3 + pandoc.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
ET.register_namespace("w", W)
ET.register_namespace("r", R)


def cm(x):
    return round(x * 567)          # cm -> twips


# --------------------------------------------------------------------------
#  PROFIL DOKUMEN
# --------------------------------------------------------------------------
PROFIL = {
    "pedoman": dict(
        tex="pedoman/pedoman.tex", font="Times New Roman", size=24,
        body_line=360, first_indent=567,                 # 1,5 spasi, alinea 1 cm (sama dengan template)
        margin=dict(l=cm(4), r=cm(3), t=cm(4), b=cm(3)),
        footer_align="center", chapter_page_break=True, chapter_align="center",
        h_sizes=(28, 24, 24, 24), gaya_bab="bab", nomor_gambar="per-bab-titik",
        # nomor halaman: awal bab tengah bawah, halaman berikutnya kanan atas
        chapter_sections=True,
        sections={"sampul": dict(footer=False),
                  "depan": dict(footer=True, fmt="lowerRoman", start=2),
                  "bab": dict(chapter=True)},
        final=dict(fmt="decimal", start=None, chapter=True), compact_line=240,
        table_borders="grid", list_line=360,
    ),
    "proposal": dict(
        tex="proposal/proposal.tex", font="Times New Roman", size=24,
        body_line=360, first_indent=567,                 # 1,5 spasi, alinea 1 cm
        margin=dict(l=cm(4), r=cm(3), t=cm(4), b=cm(3)),
        footer_align="right", chapter_page_break=False, chapter_align="left",
        h_sizes=(28, 24, 24, 24), gaya_bab="angka", nomor_gambar="per-bab",
        sections={"sampul": dict(footer=False),
                  "depan": dict(footer=True, fmt="lowerRoman", start=1)},
        final=dict(fmt="decimal", start=1), compact_line=240,
        table_borders="grid", list_line=360,
    ),
    "formulir": dict(
        tex="formulir/formulir.tex", font="Arial", size=24,
        body_line=276, first_indent=0, body_after=120,
        margin=dict(l=cm(2.5), r=cm(2.5), t=cm(2), b=cm(2)),
        footer_align="center", chapter_page_break=False, chapter_align="left",
        h_sizes=(24, 24, 24, 24), gaya_bab="angka", nomor_gambar="urut",
        sections={}, final=dict(fmt="decimal", start=1), compact_line=240,
        table_borders="grid", list_line=240,
    ),
}


# Seminar Hasil dan Skripsi: ukuran sama dengan Proposal (1,5 spasi, 4/4/3/3, huruf sama), judul 'BAB I', nomor halaman per bab
_SAMA_PROPOSAL = dict(body_line=360, first_indent=567, list_line=360, h_sizes=(28, 24, 24, 24),   # ukuran = proposal
                      # sampul + lembar persetujuan tanpa nomor; abstrak mulai angka romawi i
                      sections={"sampul": dict(footer=False),
                                "depan": dict(footer=True, fmt="lowerRoman", start=1),
                                "bab": dict(chapter=True)})
PROFIL["seminar-hasil"] = dict(PROFIL["pedoman"], tex="seminar-hasil/seminar-hasil.tex", **_SAMA_PROPOSAL)
PROFIL["skripsi"] = dict(PROFIL["pedoman"], tex="skripsi/skripsi.tex", **_SAMA_PROPOSAL)
PROFIL["proposal"] = dict(PROFIL["pedoman"], tex="proposal/proposal.tex", **_SAMA_PROPOSAL)   # sama dengan skripsi: BAB I, tiap bab halaman baru
# dokumen CONTOH terisi (folder contoh/): profil sama dengan dokumen aslinya
PROFIL["contoh-proposal"] = dict(PROFIL["proposal"], tex="contoh/proposal/proposal.tex")
PROFIL["contoh-hasil"] = dict(PROFIL["seminar-hasil"], tex="contoh/seminar-hasil/seminar-hasil.tex")
PROFIL["contoh-skripsi"] = dict(PROFIL["skripsi"], tex="contoh/skripsi/skripsi.tex")


# --------------------------------------------------------------------------
#  GAYA (styles.xml)
# --------------------------------------------------------------------------
def q(tag):
    return "{%s}%s" % (W, tag)


def frag(xml):
    """Parse potongan XML w: ke Element."""
    return ET.fromstring('<root xmlns:w="%s" xmlns:r="%s">%s</root>' % (W, R, xml))[0]


def para_style(sid, name, based="Normal", nxt=None, ppr="", rpr="", custom=False,
               qformat=True, link=None):
    s = '<w:style w:type="paragraph"%s w:styleId="%s"><w:name w:val="%s"/>' % (
        ' w:customStyle="1"' if custom else "", sid, name)
    if based:
        s += '<w:basedOn w:val="%s"/>' % based
    if nxt:
        s += '<w:next w:val="%s"/>' % nxt
    if qformat:
        s += "<w:qFormat/>"
    if ppr:
        s += "<w:pPr>%s</w:pPr>" % ppr
    if rpr:
        s += "<w:rPr>%s</w:rPr>" % rpr
    s += "</w:style>"
    return frag(s)


def spacing(before=0, after=0, line=240):
    return '<w:spacing w:before="%d" w:after="%d" w:line="%d" w:lineRule="auto"/>' % (before, after, line)


def table_style(sid, name, borders, custom=True):
    b = lambda side, sz: '<w:%s w:val="single" w:sz="%d" w:space="0" w:color="000000"/>' % (side, sz)
    none = lambda side: '<w:%s w:val="nil"/>' % side
    if borders == "three-line":
        tbl_b = "<w:tblBorders>%s%s</w:tblBorders>" % (b("top", 8), b("bottom", 8))
        first = ('<w:tblStylePr w:type="firstRow"><w:tcPr><w:tcBorders>%s</w:tcBorders></w:tcPr></w:tblStylePr>'
                 % b("bottom", 4))
    elif borders == "grid":
        tbl_b = "<w:tblBorders>%s</w:tblBorders>" % "".join(
            b(s, 4) for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
        first = ""   # judul kolom ditebalkan lewat \\textbf di sumber
    else:  # none
        tbl_b = "<w:tblBorders>%s</w:tblBorders>" % "".join(
            none(s) for s in ("top", "left", "bottom", "right", "insideH", "insideV"))
        first = ""
    xml = ('<w:style w:type="table"%s w:styleId="%s"><w:name w:val="%s"/><w:basedOn w:val="TableNormal"/>'
           '<w:uiPriority w:val="59"/><w:qFormat/><w:tblPr><w:tblInd w:w="85" w:type="dxa"/>%s'
           '<w:tblCellMar><w:top w:w="40" w:type="dxa"/><w:left w:w="85" w:type="dxa"/>'
           '<w:bottom w:w="40" w:type="dxa"/><w:right w:w="85" w:type="dxa"/></w:tblCellMar></w:tblPr>%s</w:style>'
           % (' w:customStyle="1"' if custom else "", sid, name, tbl_b, first))
    return frag(xml)


def build_styles(p, default_xml):
    root = ET.fromstring(default_xml)
    font, size = p["font"], p["size"]

    # bawaan dokumen
    dd = root.find(q("docDefaults"))
    for ch in list(dd):
        dd.remove(ch)
    dd.append(frag(
        '<w:rPrDefault><w:rPr><w:rFonts w:ascii="%s" w:hAnsi="%s" w:cs="%s" w:eastAsia="%s"/>'
        '<w:sz w:val="%d"/><w:szCs w:val="%d"/><w:lang w:val="id-ID" w:eastAsia="id-ID" w:bidi="ar-SA"/>'
        "</w:rPr></w:rPrDefault>" % (font, font, font, font, size, size)))
    dd.append(frag('<w:pPrDefault><w:pPr>%s</w:pPr></w:pPrDefault>' % spacing(0, 0, 240)))

    replace = {}

    def add(el):
        sid = el.get(q("styleId"))
        replace[sid] = el

    jb = '<w:jc w:val="both"/>'
    body_ppr = '%s%s<w:ind w:firstLine="%d"/>' % (spacing(0, p.get("body_after", 0), p["body_line"]), jb, p["first_indent"])
    add(para_style("BodyText", "Body Text", "Normal", ppr=body_ppr))
    add(para_style("FirstParagraph", "First Paragraph", "BodyText", nxt="BodyText", custom=True))
    add(para_style("Compact", "Compact", "Normal", ppr=spacing(0, 0, p["compact_line"]), custom=True))
    add(para_style("Butir", "Butir", "Normal", custom=True,
                   ppr="%s%s" % (spacing(0, 0, p["list_line"]), jb)))
    add(para_style("Tengah", "Tengah", "Normal", custom=True,
                   ppr='<w:keepLines/>%s<w:jc w:val="center"/>' % spacing(0, 120, 240)))
    add(para_style("SampulBesar", "Sampul Besar", "Tengah", custom=True, rpr='<w:b/><w:bCs/><w:sz w:val="32"/><w:szCs w:val="32"/>',
                   ppr=spacing(0, 160, 240)))
    add(para_style("SampulSedang", "Sampul Sedang", "Tengah", custom=True, rpr='<w:b/><w:bCs/><w:sz w:val="28"/><w:szCs w:val="28"/>',
                   ppr=spacing(0, 160, 240)))
    add(para_style("Abstrak", "Abstrak", "Normal", custom=True,
                   ppr='%s%s<w:ind w:firstLine="%d"/>' % (spacing(0, 120, 240), jb, p["first_indent"])))
    add(para_style("Kanan", "Kanan", "Normal", custom=True,
                   ppr='%s<w:ind w:left="%d"/>' % (spacing(0, 240, 240), cm(8))))
    add(para_style("DaftarPustaka", "Daftar Pustaka", "Normal", custom=True,
                   ppr='%s%s<w:ind w:left="720" w:hanging="720"/>' % (spacing(0, 240, 240), jb)))
    add(para_style("Kotak", "Kotak", "Normal", custom=True, ppr=spacing(0, 60, 276) + jb))
    add(para_style("Isian", "Isian", "Normal", custom=True, ppr="<w:keepNext/>" + spacing(120, 60, 240) + '<w:ind w:left="340"/>'))
    add(para_style("TOCNote", "TOC Note", "Normal", custom=True, ppr=spacing(0, 0, 240)))

    # judul
    h1_ppr = ('<w:keepNext/><w:keepLines/>%s%s<w:jc w:val="%s"/><w:outlineLvl w:val="0"/>' % (
        '<w:pageBreakBefore/>' if p["chapter_page_break"] else "",
        spacing(240 if not p["chapter_page_break"] else 0, 360, 240), p["chapter_align"]))
    add(para_style("Heading1", "heading 1", "Normal", nxt="BodyText", ppr=h1_ppr,
                   rpr='<w:b/><w:bCs/><w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (p["h_sizes"][0], p["h_sizes"][0])))
    hang = {2: 720, 3: 851, 4: 1021}
    for lv in (2, 3, 4):
        sz = p["h_sizes"][min(lv - 1, 3)]
        add(para_style("Heading%d" % lv, "heading %d" % lv, "Normal", nxt="BodyText",
                       ppr='<w:keepNext/><w:keepLines/>%s<w:ind w:left="%d" w:hanging="%d"/><w:outlineLvl w:val="%d"/>' % (
                           spacing(360 if lv < 4 else 240, 240 if lv < 4 else 120, 240), hang[lv], hang[lv], lv - 1),
                       rpr=('<w:b/><w:bCs/>' if lv < 4 else '<w:i/><w:iCs/>') + '<w:sz w:val="%d"/><w:szCs w:val="%d"/>' % (sz, sz)))

    # daftar isi
    tabs = lambda pos, extra="": '<w:tabs>%s<w:tab w:val="right" w:leader="dot" w:pos="%d"/></w:tabs>' % (extra, pos)
    text_w = 11906 - p["margin"]["l"] - p["margin"]["r"]
    add(para_style("TOC1", "toc 1", "Normal", nxt="Normal", ppr=tabs(text_w) + spacing(120, 0, 240), rpr="<w:b/>"))
    add(para_style("TOC2", "toc 2", "Normal", nxt="Normal",
                   ppr=tabs(text_w, '<w:tab w:val="left" w:pos="720"/>') + spacing(40, 0, 240) + '<w:ind w:left="0"/>'))
    add(para_style("TOC3", "toc 3", "Normal", nxt="Normal",
                   ppr=tabs(text_w, '<w:tab w:val="left" w:pos="1600"/>') + spacing(40, 0, 240) + '<w:ind w:left="720"/>'))

    # keterangan tabel / gambar
    add(para_style("TableCaption", "Table Caption", "Normal", nxt="Normal", custom=True,
                   ppr='<w:keepNext/>%s<w:jc w:val="center"/>' % spacing(120, 120, 240)))
    add(para_style("ImageCaption", "Image Caption", "Normal", nxt="BodyText", custom=True,
                   ppr='%s<w:jc w:val="center"/>' % spacing(120, 240, 240)))
    add(para_style("CaptionedFigure", "Captioned Figure", "Normal", nxt="ImageCaption", custom=True,
                   ppr='<w:keepNext/>%s<w:jc w:val="center"/>' % spacing(120, 0, 240)))
    add(para_style("Figure", "Figure", "Normal", custom=True, ppr='<w:jc w:val="center"/>' + spacing(120, 0, 240)))
    add(para_style("Footer", "footer", "Normal", ppr='<w:jc w:val="%s"/>' % p["footer_align"]))
    add(para_style("Header", "header", "Normal", ppr='<w:jc w:val="right"/>'))

    add(table_style("Table", "Table", p["table_borders"]))
    add(table_style("TabelTanpaGaris", "Tabel Tanpa Garis", "none"))

    # ganti / tambahkan
    for st in list(root.findall(q("style"))):
        sid = st.get(q("styleId"))
        if sid in replace:
            root.remove(st)
    for el in replace.values():
        root.append(el)
    if root.find(".//%s[@%s='TableNormal']" % (q("style"), q("styleId"))) is None:
        root.append(frag(
            '<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/>'
            '<w:uiPriority w:val="99"/><w:semiHidden/><w:unhideWhenUsed/><w:tblPr><w:tblInd w:w="0" w:type="dxa"/>'
            '<w:tblCellMar><w:top w:w="0" w:type="dxa"/><w:left w:w="108" w:type="dxa"/>'
            '<w:bottom w:w="0" w:type="dxa"/><w:right w:w="108" w:type="dxa"/></w:tblCellMar></w:tblPr></w:style>'))
    return ET.tostring(root, encoding="unicode", xml_declaration=False)


def build_reference(p, dest):
    """reference.docx = bawaan pandoc + styles.xml kita."""
    tmp = Path(tempfile.mkdtemp(prefix="ref-"))
    subprocess.run(["pandoc", "-o", str(tmp / "d.docx"), "--print-default-data-file", "reference.docx"], check=True)
    with zipfile.ZipFile(tmp / "d.docx") as z:
        items = {n: z.read(n) for n in z.namelist()}
    styles = build_styles(p, items["word/styles.xml"].decode("utf8"))
    items["word/styles.xml"] = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n' + styles).encode("utf8")
    # dokumen contoh: kosongkan isi, sisakan margin
    items["word/document.xml"] = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<w:document xmlns:w="%s" xmlns:r="%s"><w:body><w:p/>%s</w:body></w:document>'
        % (W, R, sect_pr(p, footer_rid=None, fmt=None, start=None))).encode("utf8")
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for n, d in items.items():
            z.writestr(n, d)
    shutil.rmtree(tmp, ignore_errors=True)


# --------------------------------------------------------------------------
#  PASCA-PROSES
# --------------------------------------------------------------------------
def sect_pr(p, footer_rid, fmt, start, chapter=None):
    """chapter = dict(hdr=, ftr_first=, ftr_empty=): halaman pertama bab bernomor di tengah bawah,
    halaman berikutnya di kanan atas."""
    m = p["margin"]
    s = "<w:sectPr>"
    if chapter:
        s += '<w:headerReference w:type="default" r:id="%s"/>' % chapter["hdr"]
        s += '<w:footerReference w:type="default" r:id="%s"/>' % chapter["ftr_empty"]
        s += '<w:footerReference w:type="first" r:id="%s"/>' % chapter["ftr_first"]
    elif footer_rid:
        s += '<w:footerReference w:type="default" r:id="%s"/>' % footer_rid
    s += '<w:type w:val="nextPage"/><w:pgSz w:w="11906" w:h="16838"/>'
    s += ('<w:pgMar w:top="%d" w:right="%d" w:bottom="%d" w:left="%d" w:header="851" w:footer="709" w:gutter="0"/>'
          % (m["t"], m["r"], m["b"], m["l"]))
    if fmt:
        s += '<w:pgNumType w:fmt="%s"%s/>' % (fmt, (' w:start="%d"' % start) if start else "")
    if chapter:
        s += "<w:titlePg/>"
    s += "</w:sectPr>"
    return s


FOOTER_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<w:ftr xmlns:w="%s" xmlns:r="%s"><w:p><w:pPr><w:pStyle w:val="Footer"/></w:pPr>'
              '<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
              '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r>'
              '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>' % (W, R))


HEADER_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<w:hdr xmlns:w="%s" xmlns:r="%s"><w:p><w:pPr><w:pStyle w:val="Header"/></w:pPr>'
              '<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
              '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r>'
              '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:hdr>' % (W, R))
FOOTER_EMPTY_XML = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                    '<w:ftr xmlns:w="%s" xmlns:r="%s"><w:p><w:pPr><w:pStyle w:val="Footer"/></w:pPr></w:p></w:ftr>' % (W, R))


def postprocess(p, path):
    with zipfile.ZipFile(path) as z:
        items = {n: z.read(n) for n in z.namelist()}
    doc = items["word/document.xml"].decode("utf8")

    # footer / header (nomor halaman)
    rid = "rIdFooterNomor"
    items["word/footer1.xml"] = FOOTER_XML.encode("utf8")
    parts = [("footer1.xml", rid, "footer")]
    chap = None
    if p.get("chapter_sections"):
        items["word/header1.xml"] = HEADER_XML.encode("utf8")
        items["word/footer2.xml"] = FOOTER_EMPTY_XML.encode("utf8")
        parts += [("header1.xml", "rIdHeaderNomor", "header"), ("footer2.xml", "rIdFooterKosong", "footer")]
        chap = dict(hdr="rIdHeaderNomor", ftr_first=rid, ftr_empty="rIdFooterKosong")
    rels = items["word/_rels/document.xml.rels"].decode("utf8")
    ct = items["[Content_Types].xml"].decode("utf8")
    for fname, frid, kind in parts:
        rels = rels.replace("</Relationships>",
                            '<Relationship Id="%s" Type="%s/%s" Target="%s"/></Relationships>' % (frid, R, kind, fname))
        if "/word/%s" % fname not in ct:
            ct = ct.replace("</Types>", '<Override PartName="/word/%s" ContentType='
                            '"application/vnd.openxmlformats-officedocument.wordprocessingml.%s+xml"/></Types>' % (fname, kind))
    items["word/_rels/document.xml.rels"] = rels.encode("utf8")
    items["[Content_Types].xml"] = ct.encode("utf8")

    # penanda seksi -> sectPr lengkap
    seen = {"bab": 0}
    def mark(mt):
        name = mt.group(1)
        cfg = p["sections"].get(name, dict(footer=False))
        if cfg.get("chapter"):
            seen["bab"] += 1
            # bab pertama (seksi pertama setelah bagian depan) memulai nomor halaman 1
            return sect_pr(p, None, "decimal", 1 if seen["bab"] == 1 else None, chap)
        return sect_pr(p, rid if cfg.get("footer") else None, cfg.get("fmt"), cfg.get("start"))
    doc = re.sub(r'<w:sectPr w:rsidR="MARK_(\w+)"\s*/>', mark, doc)

    # sectPr terakhir (seksi isi)
    final = sect_pr(p, rid, p["final"]["fmt"], p["final"]["start"], chap if p["final"].get("chapter") else None)
    new, n = re.subn(r"<w:sectPr\b(?:(?!<w:sectPr\b).)*?</w:sectPr>\s*</w:body>", final + "</w:body>", doc, flags=re.S)
    if n == 0:
        new = doc.replace("</w:body>", final + "</w:body>")
    doc = new
    items["word/document.xml"] = doc.encode("utf8")

    # baris tabel tidak boleh terpotong antar-halaman
    doc = doc.replace("<w:tr><w:trPr>", "<w:tr><w:trPr><w:cantSplit/>")
    doc = re.sub(r"<w:tr>(?!<w:trPr>)", "<w:tr><w:trPr><w:cantSplit/></w:trPr>", doc)
    # tabel: jaga satu halaman (keepNext di semua baris kecuali terakhir) + jarak sesudah tabel
    def keep_table(mt):
        tbl = mt.group(0)
        rows = re.split(r"(?=<w:tr>)", tbl)
        out = [rows[0]]
        for k, r in enumerate(rows[1:], 1):
            if k < len(rows) - 1:
                r = re.sub(r'(<w:pStyle w:val="[^"]+"\s*/>)', r"\1<w:keepNext />", r)
            out.append(r)
        return "".join(out)
    doc = re.sub(r"<w:tbl>.*?</w:tbl>", keep_table, doc, flags=re.S)
    doc = doc.replace("</w:tbl>", '</w:tbl><w:p><w:pPr><w:pStyle w:val="Compact"/><w:spacing w:before="0" w:after="0" w:line="200" w:lineRule="exact"/></w:pPr></w:p>')
    # jadwal: sel "No" dan "Deskripsi Kegiatan" pada judul dua baris digabung vertikal
    def gabung_judul(mt):
        tbl = mt.group(0)
        if "GANTTMARK" not in tbl:
            return tbl
        rows = re.split(r"(?=<w:tr>)", tbl)
        for ri, tag in ((1, "restart"), (2, "")):
            for _ in range(2):
                val = '<w:vMerge w:val="restart"/><w:vAlign w:val="center"/>' if tag else "<w:vMerge/>"
                rows[ri] = rows[ri].replace("<w:tcPr />", "<w:tcPr>%s</w:tcPr>" % val, 1)
        return "".join(rows)
    doc = re.sub(r"<w:tbl>.*?</w:tbl>", gabung_judul, doc, flags=re.S)
    # sel jadwal terisi -> diberi warna oranye
    def warna(mt):
        cell = mt.group(0).replace('<w:r><w:t>GANTTMARK</w:t></w:r>', '')
        return cell.replace('<w:tcPr />', '<w:tcPr><w:shd w:val="clear" w:color="auto" w:fill="FF9900"/></w:tcPr>', 1)
    doc = re.sub(r"<w:tc>(?:(?!</w:tc>).)*GANTTMARK.*?</w:tc>", warna, doc, flags=re.S)
    items["word/document.xml"] = doc.encode("utf8")

    # judul dokumen (properti)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for n in ["[Content_Types].xml"] + [k for k in items if k != "[Content_Types].xml"]:
            z.writestr(n, items[n])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dokumen", choices=sorted(PROFIL))
    ap.add_argument("-o", "--output")
    a = ap.parse_args()
    p = PROFIL[a.dokumen]

    if shutil.which("pandoc") is None:
        sys.exit("pandoc belum terpasang. Jalankan:  brew install pandoc")

    build = ROOT / "build"
    build.mkdir(exist_ok=True)
    ref = build / ("reference-%s.docx" % a.dokumen)
    build_reference(p, ref)

    out = Path(a.output) if a.output else build / ("%s.docx" % a.dokumen)
    src = ROOT / p["tex"]
    cmd = ["pandoc", str(src), "-f", "latex", "-t", "docx", "-o", str(out),
           "--reference-doc", str(ref), "--lua-filter", str(ROOT / "word" / "filter.lua"),
           "--resource-path", str(src.parent),
           "-M", "gaya-bab=%s" % p["gaya_bab"], "-M", "nomor-gambar=%s" % p["nomor_gambar"]]
    if p.get("chapter_sections"):
        cmd += ["-M", "bab-seksi=1"]
    # pandoc ikut membaca TEXINPUTS dan akan "membongkar" common/skripsi.sty; matikan agar
    # lingkungan seperti tengah/pustaka tetap menjadi gaya Word (lihat filter.lua)
    env = {k: v for k, v in os.environ.items() if k != "TEXINPUTS"}
    # cwd = folder sumber agar \\input{bab/...} relatif terbaca
    r = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=str(src.parent))
    if r.returncode != 0:
        sys.exit("pandoc gagal:\n" + r.stderr)
    if r.stderr.strip():
        print(r.stderr.strip(), file=sys.stderr)
    postprocess(p, out)
    print("Word dibuat:", out)


if __name__ == "__main__":
    main()

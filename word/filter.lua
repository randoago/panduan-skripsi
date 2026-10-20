-- filter.lua : menyesuaikan hasil baca LaTeX agar menjadi dokumen Word yang rapi.
-- Dipanggil oleh buat_word.py (pandoc --lua-filter).
-- Metadata yang dibaca (-M):
--   gaya-bab      = bab | angka        (BAB I / "1. JUDUL")
--   nomor-gambar  = urut | per-bab     (Gambar 1 / Gambar 2.1)

local STYLE   = 'bab'
local NUMMODE = 'urut'
local inbody, firstbab, babseksi = false, true, false
local lamp = nil   -- nomor lampiran aktif (gambar/tabel di lampiran bernomor L2.1)   -- seksi per bab (nomor halaman awal bab)

function Meta(m)
  if m['bab-seksi'] then babseksi = true end
  if m['gaya-bab'] then STYLE = pandoc.utils.stringify(m['gaya-bab']) end
  if m['nomor-gambar'] then NUMMODE = pandoc.utils.stringify(m['nomor-gambar']) end
end

local function rawb(x) return pandoc.RawBlock('openxml', x) end
local function rawi(x) return pandoc.RawInline('openxml', x) end
local TAB = rawi('<w:r><w:tab/></w:r>')

local function roman(n)
  local map = {{1000,'M'},{900,'CM'},{500,'D'},{400,'CD'},{100,'C'},{90,'XC'},
               {50,'L'},{40,'XL'},{10,'X'},{9,'IX'},{5,'V'},{4,'IV'},{1,'I'}}
  local s = ''
  for _, p in ipairs(map) do
    while n >= p[1] do s = s .. p[2]; n = n - p[1] end
  end
  return s
end

local c = {0, 0, 0, 0, 0}   -- penghitung judul per tingkat
local nTabel, nGambar = 0, 0

local TOC = [[<w:p><w:pPr><w:pStyle w:val="TOCNote"/></w:pPr><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \o "1-3" \h \z \u </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>Klik kanan di sini, lalu pilih “Update Field” untuk memuat daftar isi.</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>]]

local function seksi(nama)
  -- penanda; diganti dengan <w:sectPr> lengkap oleh buat_word.py
  return rawb('<w:p><w:pPr><w:pStyle w:val="Tengah"/><w:sectPr w:rsidR="MARK_' .. nama .. '"/></w:pPr></w:p>')
end

local function has(el, cls) return el.classes:includes(cls) end

local function bab_baru(h)
  -- tiap bab (judul tingkat 1 di bagian isi) memulai seksi baru agar nomor halamannya bisa berbeda
  if babseksi and inbody and h.level == 1 then
    if firstbab then firstbab = false; return nil end
    return seksi('bab')
  end
  return nil
end

function Header(h)
  local sb = bab_baru(h)
  if has(h, 'unnumbered') then
    if h.level == 1 then
      local n = pandoc.utils.stringify(h.content):match('^LAMPIRAN%s+(%d+)')
      lamp = n
      if n then nTabel, nGambar = 0, 0 end
    end
    if sb then return { sb, h } end
    return h
  end
  local lv = h.level
  c[lv] = c[lv] + 1
  for i = lv + 1, #c do c[i] = 0 end
  if lv == 1 then nTabel, nGambar = 0, 0; lamp = nil end
  local new = pandoc.Inlines({})
  if lv == 1 then
    if STYLE == 'bab' then
      new:insert(pandoc.Str('BAB ' .. roman(c[1])))
      new:insert(pandoc.LineBreak())
    else
      new:insert(pandoc.Str(c[1] .. '.'))
      new:insert(TAB)
    end
  else
    local parts = {}
    for i = 1, lv do parts[#parts + 1] = tostring(c[i]) end
    new:insert(pandoc.Str(table.concat(parts, '.')))
    new:insert(TAB)
  end
  new:extend(h.content)
  h.content = new
  if sb then return { sb, h } end
  return h
end

local function prefix_caption(cap, label)
  if not cap or not cap.long or #cap.long == 0 then return false end
  local first = cap.long[1]
  if first.content == nil then return false end
  local new = pandoc.Inlines({pandoc.Str(label), pandoc.Space()})
  new:extend(first.content)
  first.content = new
  return true
end

local function mark_filled_cells(t)
  local found = false
  -- sel jadwal terisi (\isi) = Strong berisi satu spasi tak-pecah -> penanda untuk diwarnai
  for _, body in ipairs(t.bodies) do
    for _, row in ipairs(body.body) do
      for _, cell in ipairs(row.cells) do
        if pandoc.utils.stringify(cell.contents):match('^%d+%-%d+$') then cell.contents = {} end   -- sisa \\cmidrule
        local b = cell.contents[1]
        if b and (b.t == 'Plain' or b.t == 'Para') and b.content[1] and b.content[1].t == 'Strong'
           and pandoc.utils.stringify(b.content[1]) == '\u{a0}' then
          cell.contents = { pandoc.Plain({ rawi('<w:r><w:t>GANTTMARK</w:t></w:r>') }) }
          found = true
        end
      end
    end
  end
end

local function fix_widths(t)
  -- lebar kolom: isi kolom tanpa lebar dengan sisa, lalu skalakan agar total = 100%
  local specs, known, nd = t.colspecs, 0, 0
  for _, cs in ipairs(specs) do
    if type(cs[2]) == 'number' then known = known + cs[2] else nd = nd + 1 end
  end
  if known == 0 then return end
  local fill = nd > 0 and math.max((1 - known) / nd, 0.08) or 0
  local total = known + fill * nd
  for i, cs in ipairs(specs) do
    local w = type(cs[2]) == 'number' and cs[2] or fill
    specs[i] = { cs[1], w / total }
  end
  t.colspecs = specs
end

local function nomor(n)
  if lamp then return 'L' .. lamp .. '.' .. n end
  if NUMMODE == 'per-bab' or NUMMODE == 'per-bab-titik' then return c[1] .. '.' .. n end
  return tostring(n)
end
local function akhiran() return (NUMMODE == 'per-bab') and '' or '.' end

function Table(t)
  mark_filled_cells(t)
  if #t.colspecs == 8 and t.bodies[1] and pandoc.utils.stringify(t.caption.long):match('Jadwal') then
    local w = {0.07, 0.35, 0.098, 0.098, 0.098, 0.098, 0.098, 0.098}
    for i, cs in ipairs(t.colspecs) do t.colspecs[i] = { cs[1], w[i] } end
  end
  fix_widths(t)
  if #t.caption.long == 0 then return t end
  nTabel = nTabel + 1
  prefix_caption(t.caption, 'Tabel ' .. nomor(nTabel) .. akhiran())
  return t
end

function Figure(f)
  nGambar = nGambar + 1
  prefix_caption(f.caption, 'Gambar ' .. nomor(nGambar) .. akhiran())
  return f
end

local STYLE_OF = {
  tengah = 'Tengah', kanan = 'Kanan', pustaka = 'Daftar Pustaka',
  kotak = 'Kotak', isian = 'Isian',
  sampulbesar = 'Sampul Besar', sampulsedang = 'Sampul Sedang', abstrak = 'Abstrak',
}

function Div(d)
  for cls, st in pairs(STYLE_OF) do
    if has(d, cls) then
      d.attributes['custom-style'] = st
      return d
    end
  end
  if has(d, 'tanpagaris') then
    local w = pandoc.walk_block(d, { Table = function(t)
      t.attr.attributes['custom-style'] = 'Tabel Tanpa Garis'; return t end })
    return w.content
  end
  if has(d, 'tabelpusat') then
    for _, b in ipairs(d.content) do
      if b.t == 'Table' then
        for i, cs in ipairs(b.colspecs) do b.colspecs[i] = { pandoc.AlignCenter, cs[2] } end
        for _, body in ipairs(b.bodies) do
          for _, row in ipairs(body.body) do
            for _, cell in ipairs(row.cells) do cell.alignment = pandoc.AlignCenter end
          end
        end
      end
    end
    return d.content
  end
  if has(d, 'daftarisi') then
    return { pandoc.Header(1, {pandoc.Str('DAFTAR'), pandoc.Space(), pandoc.Str('ISI')},
                           pandoc.Attr('', {'unnumbered'})), rawb(TOC) }
  end
  if has(d, 'daftartabel') or has(d, 'daftargambar') then
    local tabel = has(d, 'daftartabel')
    local judul = tabel and {pandoc.Str('DAFTAR'), pandoc.Space(), pandoc.Str('TABEL')}
                        or  {pandoc.Str('DAFTAR'), pandoc.Space(), pandoc.Str('GAMBAR')}
    local gaya = tabel and 'Table Caption' or 'Image Caption'
    local f = '<w:p><w:pPr><w:pStyle w:val="TOCNote"/></w:pPr><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r><w:r><w:instrText xml:space="preserve"> TOC \\h \\z \\t "' .. gaya .. ',1" </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>Klik kanan di sini, lalu pilih “Update Field” untuk memuat daftar.</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
    return { pandoc.Header(1, judul, pandoc.Attr('', {'unnumbered'})), rawb(f) }
  end
  if has(d, 'halamanbaru') then return { rawb('<w:p><w:r><w:br w:type="page"/></w:r></w:p>') } end
  if has(d, 'akhirsampul') then return { seksi('sampul') } end
  if has(d, 'akhirdepan')  then inbody = true; return { seksi('depan') } end
  if has(d, 'ruang') then
    local cm = tonumber(pandoc.utils.stringify(d.content)) or 1
    local tw = math.floor(cm * 567)
    return { rawb('<w:p><w:pPr><w:pStyle w:val="Tengah"/><w:spacing w:before="0" w:after="0" w:line="' .. tw .. '" w:lineRule="exact"/></w:pPr></w:p>') }
  end
  return nil
end

-- butir daftar memakai gaya "Butir" (justify, spasi sama dengan isi) bukan "Compact"
local function wrap_items(items)
  local out = {}
  for i, item in ipairs(items) do
    local blocks = {}
    for _, b in ipairs(item) do
      if b.t == 'Plain' then b = pandoc.Para(b.content) end
      blocks[#blocks + 1] = b
    end
    out[i] = { pandoc.Div(blocks, pandoc.Attr('', {}, {['custom-style'] = 'Butir'})) }
  end
  return out
end

function OrderedList(l) l.content = wrap_items(l.content); return l end
function BulletList(l)  l.content = wrap_items(l.content); return l end

return {
  { Meta = Meta },
  { traverse = 'topdown', Div = Div, Header = Header, Table = Table, Figure = Figure,
    OrderedList = OrderedList, BulletList = BulletList },
}

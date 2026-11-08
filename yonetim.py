"""Admin paneli için tablo/menü üreticileri (yalnızca arayüz; veri src/data/*.json'dan okunur)."""
import html, json, datetime, pathlib

SRC = pathlib.Path(__file__).parent / "src"
esc = html.escape
AYLAR = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]
SIDEBAR = [
    ("panel", "panel.html", "Panel", "ti-dashboard"),
    ("duyuru", "duyuru-ekle.html", "Duyurular", "ti-announcement"),
    ("eser", "eserler.html", "Eserler", "ti-gallery"),
    ("atolye", "atolyeler.html", "Atölyeler", "ti-brush-alt"),
    ("mesaj", "mesajlar.html", "Mesajlar", "ti-email"),
    ("istatistik", "istatistik.html", "İstatistik", "ti-bar-chart"),
]

def yukle(ad):
    return json.loads((SRC / "data" / ad).read_text(encoding="utf8"))

def tarih(iso):
    t = datetime.date.fromisoformat(iso)
    return f"{t.day} {AYLAR[t.month-1]} {t.year}"

def tl(n):
    return f"{n:,}".replace(",", ".") + " ₺"

def menu(aktif):
    out = []
    for anahtar, href, ad, ikon in SIDEBAR:
        cur = ' class="aktif" aria-current="page"' if anahtar == aktif else ""
        out.append(f'<li><a href="{href}"{cur}><span class="{ikon}" aria-hidden="true"></span>{ad}</a></li>')
    return "\n".join(out)

def _kayit(d):
    return esc(json.dumps(d, ensure_ascii=False), quote=True)

def _eylem():
    return ('<td class="eylem"><button type="button" class="btn-ikon" data-duzenle aria-label="Düzenle">Düzenle</button>'
            '<button type="button" class="btn-ikon tehlike" data-sil aria-label="Sil">Sil</button></td>')

def duyuru_satirlari():
    out = []
    for d in sorted(yukle("duyurular.json"), key=lambda x: x["tarih"], reverse=True):
        kayit = {"baslik": d["baslik"], "etiket": d["etiket"], "tarih": d["tarih"], "ozet": d["ozet"], "icerik": "\n\n".join(d["icerik"])}
        out.append(f'<tr data-kayit="{_kayit(kayit)}" data-ad="{esc(d["baslik"])}"><td>{tarih(d["tarih"])}</td><td><strong>{esc(d["baslik"])}</strong></td>'
                   f'<td><span class="rozet">{esc(d["etiket"])}</span></td><td><span class="rozet yesil">Yayında</span></td>{_eylem()}</tr>')
    return "\n".join(out)

def eser_satirlari():
    out = []
    for e in yukle("eserler.json"):
        kayit = {"baslik": e["baslik"], "sanatci": e["sanatci"], "kategori": e["kategori"], "yil": e["yil"], "teknik": e["teknik"], "olcu": e["olcu"], "fiyat": e["fiyat"], "aciklama": " ".join(e["aciklama"])}
        out.append(f'<tr data-kayit="{_kayit(kayit)}" data-ad="{esc(e["baslik"] + " " + e["sanatci"])}"><td><img class="kucuk-resim" src="../{e["gorsel"]}.svg" alt=""></td>'
                   f'<td><strong>{esc(e["baslik"])}</strong><br><small>{esc(e["sanatci"])}, {e["yil"]}</small></td><td>{esc(e["kategori"].capitalize())}</td>'
                   f'<td>{tl(e["fiyat"])}</td><td><span class="rozet yesil">Satışta</span></td>{_eylem()}</tr>')
    return "\n".join(out)

def atolye_satirlari():
    out = []
    for a in yukle("atolyeler.json"):
        kayit = {"baslik": a["baslik"], "kategori": a["kategori"], "seviye": a["seviye"], "sure": a["sure"], "takvim": a["takvim"], "ucret": a["ucret"], "kontenjan": a["kontenjan"], "egitmen": a["egitmen"], "aciklama": " ".join(a["aciklama"])}
        out.append(f'<tr data-kayit="{_kayit(kayit)}" data-ad="{esc(a["baslik"] + " " + a["egitmen"])}"><td><strong>{esc(a["baslik"])}</strong><br><small>{esc(a["egitmen"])}</small></td>'
                   f'<td>{esc(a["kategori"].capitalize())}</td><td>{esc(a["sure"])}<br><small>{esc(a["takvim"])}</small></td><td>{tl(a["ucret"])}</td>'
                   f'<td>{a["kontenjan"]} kişi</td>{_eylem()}</tr>')
    return "\n".join(out)

def mesaj_satirlari():
    out = []
    for m in yukle("mesajlar.json"):
        yeni = m["durum"] == "Yeni"
        out.append(f'<tr data-tur="{esc(m["tur"])}" data-ad="{esc(m["ad"] + " " + m["konu"])}" data-mesaj="{esc(m["mesaj"])}" data-kisi="{esc(m["ad"])} ({esc(m["eposta"])})" data-konu="{esc(m["konu"])}" data-tarih="{tarih(m["tarih"])}">'
                   f'<td>{tarih(m["tarih"])}</td><td><strong>{esc(m["ad"])}</strong><br><small>{esc(m["eposta"])}</small></td>'
                   f'<td><span class="rozet">{esc(m["tur"])}</span></td><td>{esc(m["konu"])}</td>'
                   f'<td><span class="rozet {"turuncu" if yeni else "yesil"}">{m["durum"]}</span></td>'
                   f'<td class="eylem"><button type="button" class="btn-ikon" data-oku>Oku</button></td></tr>')
    return "\n".join(out)

def ozet_degerleri():
    return {"admin_eser_sayisi": len(yukle("eserler.json")), "admin_atolye_sayisi": len(yukle("atolyeler.json")),
            "admin_yeni_mesaj": sum(1 for m in yukle("mesajlar.json") if m["durum"] == "Yeni")}

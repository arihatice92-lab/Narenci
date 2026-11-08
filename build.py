#!/usr/bin/env python3
"""Statik site derleyici: src/pages/*.html + src/partials/* -> kök dizinde HTML.

Kullanım:  python3 build.py
Header/footer/menü tek yerden (burada ve src/partials altında) yönetilir.
src/pages/<ad>.html dosyasının başındaki  ---  bloğu: title, description.
Menüde olup src/pages'te karşılığı olmayan sayfalar için 'hazırlanıyor' sayfası üretilir.
"""
import re, pathlib, html, json, datetime, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import uretici, yonetim

ROOT = pathlib.Path(__file__).parent
SRC = ROOT / "src"

SITE = {
    "name": "Narenci",                      # <-- platform adı tek yerden değişir
    "tagline": "Sanat Galerisi & Atölye Platformu",
    "address": "Alemdar Mah. Sanat Sk. No:12, İzmit / Kocaeli",
    "phone": "+90 262 000 00 00",
    "phone_href": "+902620000000",
    "email": "iletisim@fircavekil.example",
    "year": "2026",
    "designer": "Hatice ARI",                    # <-- kendi adınla değiştir
    "student_no": "241307071",                # <-- kendi numaranla değiştir
}

# (başlık, dosya, [alt menüler])
MENU = [
    ("Ana Sayfa", "index.html", None),
    ("Ürünlerimiz", "#", [("Resim", "resim.html"), ("Seramik", "seramik.html"), ("Heykel", "heykel.html")]),
    ("Birimlerimiz", "#", [("Sergi Salonu", "sergi-salonu.html"), ("Atölyeler", "atolyeler.html"), ("Eğitmenler", "egitmenler.html")]),
    ("Hakkımızda", "hakkimizda.html", None),
    ("Misyon-Vizyon", "misyon-vizyon.html", None),
    ("Duyurular", "duyurular.html", None),
    ("İletişim", "iletisim.html", None),
]
# Menüde olmayan ama sitede olacak sayfalar (yoksa 'hazırlanıyor' üretilir)
EXTRA_PAGES = {}

AYLAR = ["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"]

def tablo_satirlari(v, son=""):
    return "".join(f"<tr><th scope=\"row\">{html.escape(e)}</th><td>{son}{d:,}".replace(",", ".") + "</td></tr>" for e, d in zip(v["etiketler"], v["degerler"]))

def load(name):
    return json.loads((SRC / "data" / name).read_text(encoding="utf8"))

def duyurular_sirali():
    """Yeniden eskiye (tarih azalan) sıralı duyurular."""
    return sorted(load("duyurular.json"), key=lambda d: d["tarih"], reverse=True)

def duyuru_satirlari(items):
    out = []
    for d in items:
        t = datetime.date.fromisoformat(d["tarih"])
        out.append(
            f'<li><button type="button" class="duyuru-satir" data-bs-toggle="modal" data-bs-target="#duyuru-{d["id"]}">'
            f'<span class="duyuru-tarih"><b>{t.day}</b><small>{AYLAR[t.month-1][:3]} {t.year}</small></span>'
            f'<span class="duyuru-govde"><span class="duyuru-etiket">{html.escape(d["etiket"])}</span>'
            f'<span class="duyuru-baslik">{html.escape(d["baslik"])}</span>'
            f'<span class="duyuru-ozet">{html.escape(d["ozet"])}</span></span>'
            f'<span class="duyuru-git" aria-hidden="true">Oku &rarr;</span></button></li>')
    return "\n".join(out)

def duyuru_modallari(items, root):
    out = []
    for d in items:
        t = datetime.date.fromisoformat(d["tarih"])
        govde = "".join(f"<p>{html.escape(p)}</p>" for p in d["icerik"])
        out.append(f'''<div class="modal fade" id="duyuru-{d["id"]}" tabindex="-1" aria-labelledby="duyuru-{d["id"]}-baslik" aria-hidden="true">
<div class="modal-dialog modal-dialog-centered modal-dialog-scrollable modal-lg"><div class="modal-content">
<div class="modal-header"><div><span class="duyuru-etiket">{html.escape(d["etiket"])}</span>
<h2 class="modal-title" id="duyuru-{d["id"]}-baslik">{html.escape(d["baslik"])}</h2>
<p class="duyuru-meta">{t.day} {AYLAR[t.month-1]} {t.year}</p></div>
<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Kapat"></button></div>
<div class="modal-body">{govde}</div>
<div class="modal-footer"><a class="btn-outline-sanat" href="{root}duyurular.html">Tüm duyurular</a>
<button type="button" class="btn_one" data-bs-dismiss="modal">Kapat</button></div>
</div></div></div>''')
    return "\n".join(out)

def slider_html(root):
    items = load("slider.json")
    ind, slides = [], []
    for i, it in enumerate(items):
        act = " active" if i == 0 else ""
        cur = ' class="active" aria-current="true"' if i == 0 else ""
        ind.append(f'<button type="button" data-bs-target="#vitrin" data-bs-slide-to="{i}"{cur} aria-label="{i+1}. öğe: {html.escape(it["baslik"])}"></button>')
        oz = "".join(f"<div><dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd></div>" for k, v in it["ozellikler"])
        slides.append(f'''<div class="carousel-item{act}"><div class="container"><div class="row align-items-center">
<div class="col-lg-6 order-2 order-lg-1 vitrin-metin"><span class="section-kicker">{html.escape(it["tur"])}</span>
<h2>{html.escape(it["baslik"])}</h2><p>{html.escape(it["aciklama"])}</p><dl class="vitrin-ozellik">{oz}</dl>
<a href="{root}{it["href"]}" class="btn_one">{html.escape(it["buton"])}</a></div>
<div class="col-lg-6 order-1 order-lg-2"><img class="vitrin-gorsel" src="{root}{it["gorsel"]}" alt="{html.escape(it["alt"])}"></div>
</div></div></div>''')
    return f'''<section class="vitrin" aria-roledescription="carousel" aria-label="Öne çıkan eser ve atölyeler">
<h1 class="visually-hidden">{SITE["name"]} - {SITE["tagline"]}</h1>
<div id="vitrin" class="carousel slide" data-bs-ride="carousel" data-bs-interval="5500">
<div class="carousel-indicators">{"".join(ind)}</div>
<div class="carousel-inner">{"".join(slides)}</div>
<button class="carousel-control-prev" type="button" data-bs-target="#vitrin" data-bs-slide="prev" aria-label="Önceki"><span aria-hidden="true">&#8249;</span></button>
<button class="carousel-control-next" type="button" data-bs-target="#vitrin" data-bs-slide="next" aria-label="Sonraki"><span aria-hidden="true">&#8250;</span></button>
<button class="vitrin-durdur" type="button" id="vitrin-durdur" aria-pressed="false">Durdur</button>
</div></section>'''

def menu_html(root, mobile=False):
    out = []
    for title, href, subs in MENU:
        h = href if href == "#" else root + href
        if subs:
            if mobile:
                items = "".join(f'<li><a href="{root}{sh}">{st}</a></li>' for st, sh in subs)
                out.append(f'<li><a href="#">{title}</a><ul class="sub-menu">{items}</ul></li>')
            else:
                items = "".join(f'<li><a href="{root}{sh}">{st}</a></li>' for st, sh in subs)
                out.append(f'<li class="menu-item-has-children"><a href="#">{title}</a><ul>{items}</ul></li>')
        else:
            out.append(f'<li><a href="{h}">{title}</a></li>')
    return "\n".join(out)

def parse_page(text):
    meta = {"title": SITE["name"], "description": ""}
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text

def render(body, meta, root):
    ctx = {**SITE, "root": root, "menu": menu_html(root), "mobile_menu": menu_html(root, True),
           "title": html.escape(meta["title"]), "description": html.escape(meta["description"]),
           "body_class": meta.get("body_class", ""), "extra_head": meta.get("extra_head", ""),
           "extra_scripts": meta.get("extra_scripts", ""),
           "admin_grafik": ADMIN_GRAFIK.replace("{{root}}", root) if meta.get("grafik") == "1" else "", "admin_menu": yonetim.menu(meta.get("aktif", "")), "sayfa_baslik": html.escape(meta.get("baslik", meta["title"]))}
    ctx.update({"admin_duyuru_satirlari": yonetim.duyuru_satirlari(), "admin_eser_satirlari": yonetim.eser_satirlari(),
                "admin_atolye_satirlari": yonetim.atolye_satirlari(), "admin_mesaj_satirlari": yonetim.mesaj_satirlari()})
    ctx.update(yonetim.ozet_degerleri())
    ist = load("istatistik.json")
    ctx.update({"istatistik_json": json.dumps(ist, ensure_ascii=False),
                "sayac_eser": ist["sayaclar"]["eser"], "sayac_atolye": ist["sayaclar"]["atolye"],
                "sayac_egitmen": ist["sayaclar"]["egitmen"], "sayac_katilimci": ist["sayaclar"]["katilimci"],
                "tablo_katilimci": tablo_satirlari(ist["yillik_katilimci"]), "tablo_dal": tablo_satirlari(ist["dal_dagilimi"], "%"),
                "tablo_ziyaret": tablo_satirlari(ist["aylik_ziyaret"])})
    son5 = duyurular_sirali()[:5]
    tum = duyurular_sirali()
    ctx.update({"slider": slider_html(root),
                "duyuru_satirlari_5": duyuru_satirlari(son5), "duyuru_modallari_5": duyuru_modallari(son5, root),
                "duyuru_satirlari_hepsi": duyuru_satirlari(tum), "duyuru_modallari_hepsi": duyuru_modallari(tum, root)})
    layout = meta.get("layout", "site")
    sirali = {"site": ("head", "header", None, "footer", "scripts"),
              "admin": ("admin-head", "admin-ust", None, "admin-kapat", "admin-alt"),
              "admin-giris": ("admin-head", "admin-giris-ust", None, "admin-giris-kapat", "admin-alt")}[layout]
    parts = []
    for name in sirali:
        parts.append(body if name is None else (SRC / "partials" / f"{name}.html").read_text(encoding="utf8"))
    page = "\n".join(parts)
    for k, v in ctx.items():
        page = page.replace("{{" + k + "}}", str(v))
    return page

ADMIN_GRAFIK = '<script src="{{root}}assets/js/vendor/chart.umd.js"></script><script src="{{root}}assets/js/grafikler.js"></script>'

STUB = """<section class="page-banner"><div class="container"><h1>{title}</h1>
<p class="breadcrumb-line"><a href="{root}index.html">Ana Sayfa</a> / {title}</p></div></section>
<section class="section-padding"><div class="container text-center">
<p class="lead">Bu sayfa hazırlanıyor.</p><a class="btn_one" href="{root}index.html">Ana Sayfaya Dön</a></div></section>"""

def main():
    built = []
    pages = {}
    for f in sorted((SRC / "pages").rglob("*.html")):
        rel = f.relative_to(SRC / "pages").as_posix()
        pages[rel] = f
    uretilen = uretici.uret()          # veri dosyalarından gelen sayfalar
    wanted = {h: t for t, h, s in MENU if h != "#"}
    for t, h, subs in MENU:
        for st, sh in (subs or []):
            wanted[sh] = st
    wanted.update(EXTRA_PAGES)
    for it in load("slider.json"):
        wanted.setdefault(it["href"], it["baslik"])
    for rel, (meta, body) in uretilen.items():
        meta = {**meta, "title": meta["title"].replace("{{name}}", SITE["name"])}
        (ROOT / rel).write_text(render(body.replace("{{root}}", ""), meta, ""), encoding="utf8")
        built.append(rel)
    for rel, title in wanted.items():
        if rel not in pages and rel not in uretilen:
            out = ROOT / rel
            body = STUB.format(title=title, root="")
            out.write_text(render(body, {"title": f"{title} | {SITE['name']}", "description": ""}, ""), encoding="utf8")
            built.append(f"{rel} (hazırlanıyor)")
    for rel, f in pages.items():
        depth = rel.count("/")
        root = "../" * depth
        meta, body = parse_page(f.read_text(encoding="utf8"))
        body = body.replace("{{root}}", root)
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render(body, meta, root), encoding="utf8")
        built.append(rel)
    print("Üretilen sayfalar:", *built, sep="\n  ")

if __name__ == "__main__":
    main()

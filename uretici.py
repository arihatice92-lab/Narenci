"""Veri dosyalarından (src/data/*.json) sayfa üretir: koleksiyonlar, eser ve atölye detayları."""
import html, json, pathlib

SRC = pathlib.Path(__file__).parent / "src"
esc = html.escape

KATEGORILER = {
    "resim": ("Resim", "Yağlıboya, akrilik ve suluboya tablolar."),
    "seramik": ("Seramik", "El yapımı vazo, tabak ve çömlekler."),
    "heykel": ("Heykel", "Bronz, mermer ve taş heykeller."),
}

def yukle(ad):
    return json.loads((SRC / "data" / ad).read_text(encoding="utf8"))

def tl(n):
    return f"{n:,}".replace(",", ".") + " ₺"

def banner(baslik, yol):
    izler = " / ".join(f'<a href="{{{{root}}}}{h}">{esc(t)}</a>' for t, h in yol)
    return (f'<section class="page-banner"><div class="container"><h1>{esc(baslik)}</h1>'
            f'<p class="breadcrumb-line"><a href="{{{{root}}}}index.html">Ana Sayfa</a> / {izler + " / " if izler else ""}{esc(baslik)}</p></div></section>')

def eser_karti(e):
    return (f'<div class="col-lg-3 col-md-4 col-sm-6 urun-oge" data-ad="{esc(e["baslik"] + " " + e["sanatci"])}" data-fiyat="{e["fiyat"]}" data-sira="">'
            f'<a class="urun-kart" href="{{{{root}}}}eser-{e["slug"]}.html">'
            f'<span class="urun-resim"><img src="{{{{root}}}}{e["gorsel"]}.svg" alt="{esc(e["alt"])}" loading="lazy"></span>'
            f'<span class="urun-etiket">{KATEGORILER[e["kategori"]][0]}</span>'
            f'<span class="urun-ad">{esc(e["baslik"])}</span><span class="urun-alt">{esc(e["sanatci"])} &middot; {esc(e["olcu"])}</span>'
            f'<span class="urun-fiyat">{tl(e["fiyat"])}</span></a></div>')

def atolye_karti(a):
    return (f'<div class="col-lg-4 col-md-6 urun-oge" data-kat="{a["kategori"]}" data-ad="{esc(a["baslik"])}" data-fiyat="{a["ucret"]}">'
            f'<a class="urun-kart" href="{{{{root}}}}atolye-{a["slug"]}.html">'
            f'<span class="urun-resim"><img src="{{{{root}}}}{a["gorsel"]}.svg" alt="{esc(a["alt"])}" loading="lazy"></span>'
            f'<span class="urun-etiket">{KATEGORILER[a["kategori"]][0]} atölyesi</span>'
            f'<span class="urun-ad">{esc(a["baslik"])}</span>'
            f'<span class="urun-alt">{esc(a["seviye"])} &middot; {esc(a["sure"])} &middot; {esc(a["egitmen"])}</span>'
            f'<span class="urun-fiyat">{tl(a["ucret"])}</span></a></div>')

def kategori_sekmeleri(aktif):
    return '<nav class="kategori-sekme" aria-label="Koleksiyonlar">' + "".join(
        f'<a href="{{{{root}}}}{k}.html"{" aria-current=\"page\" class=\"aktif\"" if k == aktif else ""}>{v[0]}</a>' for k, v in KATEGORILER.items()) + '</nav>'

def koleksiyon_sayfasi(kat, eserler):
    ad, aciklama = KATEGORILER[kat]
    liste = [e for e in eserler if e["kategori"] == kat]
    govde = banner(ad, [("Ürünlerimiz", "resim.html")]) + f'''
<section class="section-padding koleksiyon">
<div class="container">
<p class="koleksiyon-giris">{esc(aciklama)} Ayrıntı ve fiyat bilgisi için bir esere tıklayın.</p>
{kategori_sekmeleri(kat)}
<div class="arac-cubugu">
<div class="arac"><label for="ara">Ara</label><input id="ara" type="search" placeholder="Eser veya sanatçı adı" autocomplete="off"></div>
<div class="arac"><label for="sirala">Sırala</label><select id="sirala"><option value="">Önerilen</option><option value="fiyat-art">Fiyat: düşükten yükseğe</option><option value="fiyat-azal">Fiyat: yüksekten düşüğe</option><option value="ad">Ada göre (A-Z)</option></select></div>
<p class="arac-sonuc" id="sonuc" role="status" aria-live="polite">{len(liste)} eser gösteriliyor</p>
</div>
<div class="row urun-izgara" id="izgara" data-birim="eser">
{"".join(eser_karti(e) for e in liste)}
</div>
<p class="bos-mesaj" id="bos" hidden>Aramanızla eşleşen eser bulunamadı.</p>
</div></section>
<script src="{{{{root}}}}assets/js/koleksiyon.js"></script>'''
    return {"title": f"{ad} Koleksiyonu | {{{{name}}}}", "description": f"Narenci galerisinde sergilenen {ad.lower()} eserleri."}, govde

def galeri(gorsel, alt, alt2):
    return f'''<div class="galeri">
<div class="galeri-ana"><img id="galeri-ana" src="{{{{root}}}}{gorsel}.svg" alt="{esc(alt)}"></div>
<div class="galeri-kucuk" role="group" aria-label="Görseller">
<button type="button" class="galeri-dugme aktif" data-src="{{{{root}}}}{gorsel}.svg" data-alt="{esc(alt)}" aria-pressed="true"><img src="{{{{root}}}}{gorsel}.svg" alt="Genel görünüm"></button>
<button type="button" class="galeri-dugme" data-src="{{{{root}}}}{gorsel}-detay.svg" data-alt="{esc(alt2)}" aria-pressed="false"><img src="{{{{root}}}}{gorsel}-detay.svg" alt="Yakından detay"></button>
</div></div>'''

def ozellik_listesi(cift):
    return '<dl class="ozellik-listesi">' + "".join(f"<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>" for k, v in cift) + "</dl>"

def eser_detay(e, eserler):
    kat = KATEGORILER[e["kategori"]][0]
    benzer = [x for x in eserler if x["kategori"] == e["kategori"] and x["slug"] != e["slug"]][:3]
    ozellik = [("Sanatçı", e["sanatci"]), ("Yıl", str(e["yil"])), ("Teknik / malzeme", e["teknik"]), ("Ölçü", e["olcu"])] + e["ozel"]
    govde = banner(e["baslik"], [("Ürünlerimiz", "resim.html"), (kat, f'{e["kategori"]}.html')]) + f'''
<section class="section-padding detay">
<div class="container"><div class="row">
<div class="col-lg-7">{galeri(e["gorsel"], e["alt"], e["baslik"] + " - yakından detay görünümü (örnek illüstrasyon)")}</div>
<div class="col-lg-5 detay-bilgi">
<span class="section-kicker">{kat}</span>
<h2>{esc(e["baslik"])}</h2>
<p class="detay-sanatci">{esc(e["sanatci"])}, {e["yil"]}</p>
<p class="detay-fiyat">{tl(e["fiyat"])}</p>
<p>{esc(e["ozet"])}</p>
{ozellik_listesi(ozellik)}
<div class="detay-eylem"><a class="btn_one" href="{{{{root}}}}iletisim.html?konu={esc(e["baslik"])}">Satın Alma / Bilgi İçin Yazın</a>
<a class="btn-outline-sanat" href="{{{{root}}}}{e["kategori"]}.html">Koleksiyona Dön</a></div>
</div></div>
<div class="row detay-aciklama"><div class="col-lg-8"><h3>Eser Hakkında</h3>{"".join(f"<p>{esc(p)}</p>" for p in e["aciklama"])}</div></div>
<div class="benzer"><h3>Bu Koleksiyondan Diğer Eserler</h3><div class="row urun-izgara">{"".join(eser_karti(x) for x in benzer)}</div></div>
</div></section>
<script src="{{{{root}}}}assets/js/galeri.js"></script>'''
    return {"title": f'{e["baslik"]} | {kat} | {{{{name}}}}', "description": e["ozet"]}, govde

def atolyeler_sayfasi(atolyeler):
    govde = banner("Atölyeler", [("Birimlerimiz", "atolyeler.html")]) + f'''
<section class="section-padding koleksiyon">
<div class="container">
<p class="koleksiyon-giris">Resim, seramik ve heykel atölyelerimizde küçük gruplarla uygulamalı eğitim veriyoruz.</p>
<div class="filtre-dugmeleri" role="group" aria-label="Atölye dalı">
<button type="button" class="filtre aktif" data-filtre="" aria-pressed="true">Tümü</button>
<button type="button" class="filtre" data-filtre="resim" aria-pressed="false">Resim</button>
<button type="button" class="filtre" data-filtre="seramik" aria-pressed="false">Seramik</button>
<button type="button" class="filtre" data-filtre="heykel" aria-pressed="false">Heykel</button></div>
<div class="arac-cubugu">
<div class="arac"><label for="ara">Ara</label><input id="ara" type="search" placeholder="Atölye adı" autocomplete="off"></div>
<div class="arac"><label for="sirala">Sırala</label><select id="sirala"><option value="">Önerilen</option><option value="fiyat-art">Ücret: düşükten yükseğe</option><option value="fiyat-azal">Ücret: yüksekten düşüğe</option><option value="ad">Ada göre (A-Z)</option></select></div>
<p class="arac-sonuc" id="sonuc" role="status" aria-live="polite">{len(atolyeler)} atölye gösteriliyor</p>
</div>
<div class="row urun-izgara" id="izgara" data-birim="atölye">
{"".join(atolye_karti(a) for a in atolyeler)}
</div>
<p class="bos-mesaj" id="bos" hidden>Seçiminizle eşleşen atölye bulunamadı.</p>
</div></section>
<script src="{{{{root}}}}assets/js/koleksiyon.js"></script>'''
    return {"title": "Atölyeler | {{name}}", "description": "Resim, seramik ve heykel atölyeleri; süre, seviye ve ücret bilgileri."}, govde

def atolye_detay(a, atolyeler):
    kat = KATEGORILER[a["kategori"]][0]
    benzer = [x for x in atolyeler if x["slug"] != a["slug"]]
    benzer = ([x for x in benzer if x["kategori"] == a["kategori"]] + [x for x in benzer if x["kategori"] != a["kategori"]])[:3]
    ozet = [("Seviye", a["seviye"]), ("Süre", a["sure"]), ("Gün ve saat", a["takvim"]), ("Kontenjan", f'{a["kontenjan"]} kişi'),
            ("Eğitmen", a["egitmen"]), ("Malzeme", a["dahil"])]
    govde = banner(a["baslik"], [("Birimlerimiz", "atolyeler.html"), ("Atölyeler", "atolyeler.html")]) + f'''
<section class="section-padding detay">
<div class="container"><div class="row">
<div class="col-lg-7">{galeri(a["gorsel"], a["alt"], a["baslik"] + " - atölye ortamı yakın görünüm (örnek illüstrasyon)")}</div>
<div class="col-lg-5 detay-bilgi">
<span class="section-kicker">{kat} atölyesi</span>
<h2>{esc(a["baslik"])}</h2>
<p class="detay-fiyat">{tl(a["ucret"])} <small>/ dönem</small></p>
<p>{esc(a["ozet"])}</p>
{ozellik_listesi(ozet)}
<div class="detay-eylem"><a class="btn_one" href="#on-kayit">Ön Kayıt Ol</a><a class="btn-outline-sanat" href="{{{{root}}}}atolyeler.html">Tüm Atölyeler</a></div>
</div></div>
<div class="row detay-aciklama">
<div class="col-lg-6"><h3>Atölye Hakkında</h3>{"".join(f"<p>{esc(p)}</p>" for p in a["aciklama"])}
<h3>Neler Öğreneceksiniz</h3><ul class="tik-listesi">{"".join(f"<li>{esc(k)}</li>" for k in a["kazanim"])}</ul></div>
<div class="col-lg-6"><h3>Haftalık Program</h3><ol class="program-listesi">{"".join(f"<li><span>{i}. hafta</span>{esc(p)}</li>" for i, p in enumerate(a["program"], 1))}</ol></div>
</div>
<div class="on-kayit" id="on-kayit"><h3>Ön Kayıt Formu</h3>
<p>Formu doldurun, size dönüş yapalım. (Bu örnek sitede form sunucuya gönderilmez.)</p>
<form class="site-formu" data-demo novalidate>
<div class="row">
<div class="col-md-6"><label for="ok-ad">Ad Soyad</label><input id="ok-ad" name="ad" type="text" required autocomplete="name"></div>
<div class="col-md-6"><label for="ok-eposta">E-posta</label><input id="ok-eposta" name="eposta" type="email" required autocomplete="email"></div>
<div class="col-md-6"><label for="ok-tel">Telefon</label><input id="ok-tel" name="tel" type="tel" autocomplete="tel"></div>
<div class="col-md-6"><label for="ok-atolye">Atölye</label><input id="ok-atolye" name="atolye" type="text" value="{esc(a["baslik"])}" readonly></div>
<div class="col-12"><label for="ok-not">Notunuz (isteğe bağlı)</label><textarea id="ok-not" name="not" rows="3"></textarea></div>
</div>
<button type="submit" class="btn_one">Ön Kaydı Gönder</button>
<p class="form-sonuc" role="status" aria-live="polite"></p>
</form></div>
<div class="benzer"><h3>Diğer Atölyeler</h3><div class="row urun-izgara">{"".join(atolye_karti(x) for x in benzer)}</div></div>
</div></section>
<script src="{{{{root}}}}assets/js/galeri.js"></script>
<script src="{{{{root}}}}assets/js/form-demo.js"></script>'''
    return {"title": f'{a["baslik"]} | Atölyeler | {{{{name}}}}', "description": a["ozet"]}, govde

def egitmenler_sayfasi(egitmenler, atolyeler):
    kartlar = []
    for g in egitmenler:
        verdigi = [a for a in atolyeler if a["egitmen"] == g["ad"]]
        liste = "".join(f'<li><a href="{{{{root}}}}atolye-{a["slug"]}.html">{esc(a["baslik"])}</a></li>' for a in verdigi)
        liste = f'<p class="kisi-etiket">Verdiği atölyeler</p><ul class="kisi-atolyeler">{liste}</ul>' if verdigi else '<p class="kisi-not">Bu dönem konuk sanatçı olarak seçili etkinliklerde yer alıyor.</p>'
        kartlar.append(f'''<div class="col-lg-4 col-md-6"><article class="kisi-kart">
<img src="{{{{root}}}}assets/img/narenci/egitmen-{g["slug"]}.svg" alt="{esc(g["ad"])} (örnek görsel)" loading="lazy">
<div class="kisi-govde"><span class="urun-etiket">{esc(g["brans"])}</span><h3>{esc(g["ad"])}</h3><p class="kisi-unvan">{esc(g["unvan"])} &middot; {esc(g["deneyim"])} deneyim</p>
<p>{esc(g["bio"])}</p>{liste}</div></article></div>''')
    govde = banner("Eğitmenler", [("Birimlerimiz", "atolyeler.html")]) + f'''
<section class="section-padding"><div class="container">
<p class="koleksiyon-giris">Atölyelerimizi alanında deneyimli sanatçılar yürütüyor. Gruplarımız küçük tutulur; her katılımcıyla birebir ilgilenilir.</p>
<div class="row urun-izgara">{"".join(kartlar)}</div></div></section>'''
    return {"title": "Eğitmenler | {{name}}", "description": "Narenci atölyelerini yürüten resim, seramik ve heykel eğitmenleri."}, govde

def sergi_salonu_sayfasi(sergiler, eserler):
    sozluk = {e["slug"]: e for e in eserler}
    renk = {"Devam ediyor": "devam", "Yakında": "yakinda", "Sona erdi": "bitti"}
    satirlar = []
    for g in sergiler:
        kucukler = "".join(f'<a href="{{{{root}}}}eser-{s}.html"><img src="{{{{root}}}}{sozluk[s]["gorsel"]}.svg" alt="{esc(sozluk[s]["baslik"])}" title="{esc(sozluk[s]["baslik"])}" loading="lazy"></a>' for s in g["eserler"])
        satirlar.append(f'''<article class="sergi-satir"><div class="row align-items-center">
<div class="col-lg-5"><img class="sergi-gorsel" src="{{{{root}}}}{g["gorsel"]}.svg" alt="{esc(g["alt"])}" loading="lazy"></div>
<div class="col-lg-7 sergi-metin"><span class="durum-rozet {renk[g["durum"]]}">{esc(g["durum"])}</span>
<h3>{esc(g["baslik"])}</h3><p class="sergi-tarih">{esc(g["dal"])} &middot; {esc(g["tarih"])}</p>
{"".join(f"<p>{esc(p)}</p>" for p in [g["ozet"]] + g["aciklama"])}
<p class="kisi-etiket">Sergilenen eserlerden</p><div class="sergi-kucukler">{kucukler}</div></div></div></article>''')
    bilgi = [("Adres", "Alemdar Mah. Sanat Sk. No:12, İzmit / Kocaeli"), ("Saatler", "Salı - Pazar 10.00 - 19.00 (Pazartesi kapalı)"),
             ("Giriş", "Ücretsiz"), ("Alan", "220 m², 2 salon"), ("Erişim", "Asansör ve engelli rampası mevcut"), ("Grup ziyareti", "Okullar ve gruplar için randevu ile rehberli tur")]
    govde = banner("Sergi Salonu", [("Birimlerimiz", "atolyeler.html")]) + f'''
<section class="section-padding"><div class="container">
<div class="row"><div class="col-lg-5"><h2 class="bolum-baslik">Salon Bilgileri</h2>{ozellik_listesi(bilgi)}
<a class="btn_one" href="{{{{root}}}}iletisim.html?konu=Grup ziyareti">Grup Ziyareti İçin Yazın</a></div>
<div class="col-lg-7"><h2 class="bolum-baslik">Sergiler</h2>{"".join(satirlar)}</div></div>
</div></section>'''
    return {"title": "Sergi Salonu | {{name}}", "description": "Narenci Sergi Salonu'nda devam eden, yaklaşan ve geçmiş sergiler."}, govde

def uret():
    """-> {dosya_adı: (meta, gövde)}"""
    eserler, atolyeler = yukle("eserler.json"), yukle("atolyeler.json")
    sayfalar = {}
    for k in KATEGORILER:
        sayfalar[f"{k}.html"] = koleksiyon_sayfasi(k, eserler)
    for e in eserler:
        sayfalar[f'eser-{e["slug"]}.html'] = eser_detay(e, eserler)
    sayfalar["atolyeler.html"] = atolyeler_sayfasi(atolyeler)
    sayfalar["egitmenler.html"] = egitmenler_sayfasi(yukle("egitmenler.json"), atolyeler)
    sayfalar["sergi-salonu.html"] = sergi_salonu_sayfasi(yukle("sergiler.json"), eserler)
    for a in atolyeler:
        sayfalar[f'atolye-{a["slug"]}.html'] = atolye_detay(a, atolyeler)
    return sayfalar

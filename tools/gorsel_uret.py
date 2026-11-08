#!/usr/bin/env python3
"""Geçici (örnek) eser ve atölye illüstrasyonlarını SVG olarak üretir.
Gerçek fotoğraflar hazır olunca assets/img/narenci/ altındaki dosyalar aynı adlarla değiştirilebilir
ya da src/data/*.json içindeki yollar güncellenir."""
import pathlib, re
OUT = pathlib.Path(__file__).resolve().parent.parent / "assets/img/narenci"
OUT.mkdir(parents=True, exist_ok=True)

HEAD = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 700" preserveAspectRatio="xMidYMid slice" role="img" aria-label="{alt}">'

def yaz(ad, svg):
    (OUT / f"{ad}.svg").write_text(svg, encoding="utf8")
    # detay görseli: aynı çizim, yakınlaştırılmış kırpma
    m = re.search(r'data-zoom="([^"]+)"', svg)
    z = m.group(1) if m else "225 175 450 350"
    d = svg.replace('viewBox="0 0 900 700"', f'viewBox="{z}"', 1)
    (OUT / f"{ad}-detay.svg").write_text(d, encoding="utf8")

def tuval_cerceve(sky, govde, alt, zoom="300 200 300 233"):
    s = HEAD.format(alt=alt).replace("<svg ", f'<svg data-zoom="{zoom}" ', 1)
    return s + f'''
<defs><linearGradient id="g" x1="0" y1="0" x2="0" y2="1">{"".join(f'<stop offset="{o}" stop-color="{c}"/>' for o,c in sky)}</linearGradient>
<clipPath id="t"><rect x="250" y="130" width="400" height="350"/></clipPath>
<filter id="s" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="14" stdDeviation="14" flood-color="#231f1c" flood-opacity=".28"/></filter></defs>
<rect width="900" height="700" fill="#eadccb"/><rect y="610" width="900" height="90" fill="#dccbb5"/>
<rect x="190" y="70" width="520" height="470" fill="#231f1c" filter="url(#s)"/>
<rect x="206" y="86" width="488" height="438" fill="none" stroke="#c9a24b" stroke-width="3"/>
<rect x="222" y="102" width="456" height="406" fill="#f7f3ec"/>
<g clip-path="url(#t)"><rect x="250" y="130" width="400" height="350" fill="url(#g)"/>{govde}</g>
<rect x="390" y="560" width="120" height="24" fill="#c9a24b"/><rect x="402" y="570" width="96" height="4" fill="#8f3f21" opacity=".6"/></svg>'''

def strokes(items):
    return '<g fill="none" stroke-linecap="round">' + "".join(
        f'<path d="{d}" stroke="{c}" stroke-width="{w}" opacity=".8"/>' for d, c, w in items) + '</g>'

def dots(pts, c):
    return f'<g fill="{c}">' + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in pts) + '</g>'

# ---------- RESİM ----------
yaz("eser-narenci-isigi", tuval_cerceve(
    [(0, "#f4d9a0"), (.55, "#e58f52"), (1, "#b5542f")],
    '<circle cx="450" cy="285" r="78" fill="#f9e7b8"/>'
    '<path d="M250 360 C320 300 390 330 450 345 C520 360 580 300 650 330 L650 480 L250 480Z" fill="#8f3f21"/>'
    '<path d="M250 405 C330 365 400 395 470 400 C540 405 590 372 650 390 L650 480 L250 480Z" fill="#6d2f1b"/>'
    '<path d="M250 445 C340 420 420 445 500 442 C560 440 610 425 650 432 L650 480 L250 480Z" fill="#8a9a7b"/>'
    + strokes([("M275 300 C320 280 360 290 400 270", "#c9a24b", 9), ("M500 235 C540 215 580 225 625 200", "#f7e3b0", 8),
               ("M470 455 C520 440 570 452 625 435", "#c9a24b", 7)])
    + dots([(330, 395, 16), (372, 388, 14), (560, 398, 15), (598, 404, 12)], "#e98a2b"),
    "Gün batımı manzarası, yağlıboya tablo (örnek illüstrasyon)"))
yaz("eser-mavi-saat", tuval_cerceve(
    [(0, "#1f3b5c"), (.6, "#4f7fa8"), (1, "#cfe0ea")],
    '<circle cx="520" cy="230" r="52" fill="#eef4f7"/><circle cx="540" cy="218" r="46" fill="#2c5278" opacity=".55"/>'
    '<path d="M250 380 C320 330 380 350 450 365 C520 380 590 330 650 350 L650 480 L250 480Z" fill="#1b2f4a"/>'
    '<path d="M250 430 C340 400 430 430 520 425 C580 422 620 410 650 415 L650 480 L250 480Z" fill="#12202f"/>'
    + strokes([("M270 330 C330 315 380 320 430 305", "#cfe0ea", 6), ("M270 455 C340 440 420 452 500 440", "#4f7fa8", 7)])
    + dots([(300, 190, 4), (360, 160, 3), (420, 215, 4), (580, 170, 3), (610, 250, 4), (330, 260, 3)], "#e3c071"),
    "Mavi tonlarda gece manzarası tablosu (örnek illüstrasyon)"))
yaz("eser-zeytin-bahcesi", tuval_cerceve(
    [(0, "#f3e7b4"), (1, "#d9c36a")],
    '<circle cx="330" cy="215" r="48" fill="#fff3c4"/>'
    '<path d="M250 340 C330 310 400 335 470 330 C540 325 600 300 650 320 L650 480 L250 480Z" fill="#8a9a7b"/>'
    '<path d="M250 400 C330 375 420 400 500 395 C560 392 610 380 650 385 L650 480 L250 480Z" fill="#6c7a45"/>'
    '<g stroke="#4d5a30" stroke-width="8" stroke-linecap="round"><path d="M340 420 V370"/><path d="M450 430 V365"/><path d="M570 420 V360"/></g>'
    + dots([(340, 355, 30), (450, 345, 36), (570, 342, 32), (410, 360, 22), (520, 355, 22)], "#4d5a30")
    + strokes([("M270 460 C340 450 420 462 500 452", "#f3e7b4", 7)]),
    "Zeytin ağaçlarının olduğu bahçe tablosu (örnek illüstrasyon)"))
yaz("eser-kiyida-sabah", tuval_cerceve(
    [(0, "#f6d6d0"), (.5, "#f2b8a0"), (.5, "#7ea9b4"), (1, "#3f6f80")],
    '<circle cx="450" cy="300" r="60" fill="#fde7c8"/><rect x="250" y="305" width="400" height="175" fill="#5b8a99"/>'
    '<path d="M250 305 H650" stroke="#fde7c8" stroke-width="3"/><path d="M380 320 H520 M400 340 H500 M420 360 H480" stroke="#fde7c8" stroke-width="5" stroke-linecap="round" opacity=".7"/>'
    '<path d="M300 400 L360 400 L345 425 L315 425Z" fill="#b5542f"/><path d="M330 400 V350 L355 395Z" fill="#f7f3ec"/>'
    + strokes([("M270 450 C340 440 420 452 500 442 C560 435 610 445 640 440", "#cfe6ea", 6)]),
    "Deniz kıyısında sabah manzarası tablosu (örnek illüstrasyon)"))

# ---------- SERAMİK ----------
def raf(sekil, alt):
    s = HEAD.format(alt=alt).replace("<svg ", '<svg data-zoom="225 175 450 350" ', 1)
    return s + f'''<defs><linearGradient id="i" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff7e0" stop-opacity=".75"/><stop offset="1" stop-color="#fff7e0" stop-opacity="0"/></linearGradient></defs>
<rect width="900" height="700" fill="#dfe5d6"/><polygon points="520,0 780,0 580,700 240,700" fill="url(#i)"/>
<rect x="140" y="480" width="620" height="22" fill="#8f6a4a"/><rect x="140" y="502" width="620" height="8" fill="#6d4f35"/>
<rect y="610" width="900" height="90" fill="#cdd5c0"/>{sekil}
<ellipse cx="450" cy="484" rx="150" ry="8" fill="#000" opacity=".18"/></svg>'''
yaz("eser-nar-vazo", raf(
    '<path d="M450 480 C340 470 320 360 380 320 C405 303 405 290 400 270 L396 250 L504 250 L500 270 C495 290 495 303 520 320 C580 360 560 470 450 480Z" fill="#8a2b22"/>'
    '<path d="M396 250 L408 228 L428 246 L450 222 L472 246 L492 228 L504 250Z" fill="#8a2b22"/>'
    '<g fill="#c9a24b"><circle cx="410" cy="380" r="7"/><circle cx="450" cy="400" r="7"/><circle cx="490" cy="380" r="7"/><circle cx="430" cy="430" r="6"/><circle cx="470" cy="430" r="6"/><circle cx="450" cy="350" r="6"/></g>',
    "Nar biçimli kırmızı seramik vazo (örnek illüstrasyon)"))
yaz("eser-kil-comlek", raf(
    '<path d="M450 480 C350 478 330 390 365 340 C380 320 400 312 410 300 L490 300 C500 312 520 320 535 340 C570 390 550 478 450 480Z" fill="#b5542f"/>'
    '<path d="M370 340 C320 340 315 400 355 410 M530 340 C580 340 585 400 545 410" fill="none" stroke="#b5542f" stroke-width="14" stroke-linecap="round"/>'
    '<path d="M352 380 C420 395 480 395 548 380 M358 420 C420 435 480 435 542 420" fill="none" stroke="#6d2f1b" stroke-width="4" opacity=".7"/>'
    '<rect x="404" y="290" width="92" height="14" rx="6" fill="#8f3f21"/>', "Kulplu el yapımı kil çömlek (örnek illüstrasyon)"))
yaz("eser-cini-tabak", raf(
    '<g><circle cx="450" cy="330" r="165" fill="#f7f3ec" stroke="#b5542f" stroke-width="6"/>'
    '<circle cx="450" cy="330" r="135" fill="none" stroke="#2f5d8a" stroke-width="10"/><circle cx="450" cy="330" r="100" fill="none" stroke="#b5542f" stroke-width="4"/>'
    '<g fill="#2f5d8a"><circle cx="450" cy="330" r="30"/>' + "".join(
        f'<ellipse cx="{450+70*__import__("math").cos(a*0.7854):.0f}" cy="{330+70*__import__("math").sin(a*0.7854):.0f}" rx="14" ry="26" transform="rotate({a*45+90} {450+70*__import__("math").cos(a*0.7854):.0f} {330+70*__import__("math").sin(a*0.7854):.0f})"/>' for a in range(8)) +
    '</g><circle cx="450" cy="330" r="12" fill="#c9a24b"/></g><path d="M385 480 L450 400 L515 480Z" fill="#8f6a4a"/>', "Çini desenli seramik tabak (örnek illüstrasyon)"))
yaz("eser-mat-surahi", raf(
    '<path d="M450 480 C370 480 355 390 392 340 C408 318 412 300 408 275 L398 245 C420 232 470 232 492 245 L496 262 C520 252 540 262 535 280 L500 285 C495 310 505 322 520 340 C555 390 530 480 450 480Z" fill="#efe6da" stroke="#d6c9b6" stroke-width="3"/>'
    '<path d="M530 300 C585 295 590 395 520 400" fill="none" stroke="#efe6da" stroke-width="16" stroke-linecap="round"/>'
    '<path d="M378 395 C430 410 470 410 522 395 M382 425 C430 440 470 440 518 425" fill="none" stroke="#231f1c" stroke-width="8"/>', "Mat beyaz seramik sürahi (örnek illüstrasyon)"))

# ---------- HEYKEL ----------
def kaide(sekil, alt):
    s = HEAD.format(alt=alt).replace("<svg ", '<svg data-zoom="260 170 380 295" ', 1)
    return s + f'''<defs><radialGradient id="sp" cx=".5" cy="0" r="1"><stop offset="0" stop-color="#fff2cf" stop-opacity=".55"/><stop offset="1" stop-color="#fff2cf" stop-opacity="0"/></radialGradient>
<linearGradient id="br" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#e3c071"/><stop offset=".55" stop-color="#b5542f"/><stop offset="1" stop-color="#6d2f1b"/></linearGradient>
<linearGradient id="mr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#bdb5aa"/></linearGradient></defs>
<rect width="900" height="700" fill="#2b2623"/><polygon points="450,0 250,640 650,640" fill="url(#sp)"/>
<rect x="0" y="640" width="900" height="60" fill="#1c1917"/>
<rect x="340" y="450" width="220" height="190" fill="#efe6da"/><rect x="326" y="436" width="248" height="20" fill="#f7f3ec"/>{sekil}
<ellipse cx="450" cy="643" rx="150" ry="9" fill="#000" opacity=".35"/></svg>'''
yaz("eser-anka", kaide(
    '<path d="M450 436 C372 396 362 312 424 262 C468 226 524 242 524 290 C524 338 474 346 486 382 C494 406 528 392 556 360 C548 412 504 442 450 436Z" fill="url(#br)"/>'
    '<path d="M430 270 C405 220 430 180 470 160 C455 190 462 220 490 245Z" fill="url(#br)"/>'
    '<path d="M505 262 C540 232 575 236 600 214 C592 252 560 278 520 290Z" fill="url(#br)"/>', "Soyut bronz anka heykeli (örnek illüstrasyon)"))
yaz("eser-denge", kaide(
    '<ellipse cx="450" cy="412" rx="95" ry="26" fill="#4a4440"/><ellipse cx="455" cy="360" rx="72" ry="22" fill="#b5542f"/>'
    '<ellipse cx="448" cy="318" rx="52" ry="18" fill="#6d6a66"/><ellipse cx="452" cy="285" rx="34" ry="14" fill="#c9a24b"/>', "Üst üste dengelenmiş taşlardan oluşan heykel (örnek illüstrasyon)"))
yaz("eser-dalga", kaide(
    '<path d="M345 436 C340 360 390 300 450 300 C500 300 520 340 500 372 C486 394 450 380 452 352 C454 335 478 338 480 352" fill="none" stroke="url(#mr)" stroke-width="34" stroke-linecap="round"/>'
    '<path d="M345 436 C340 360 390 300 450 300" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round" opacity=".6"/>', "Mermer dalga heykeli (örnek illüstrasyon)"))
yaz("eser-sarmal", kaide(
    '<path d="M450 400 C450 400 500 400 500 360 C500 320 440 320 430 355 C420 395 485 420 530 380 C580 330 520 270 450 280 C390 290 360 340 380 385" fill="none" stroke="url(#br)" stroke-width="22" stroke-linecap="round"/>', "Sarmal biçimli bronz heykel (örnek illüstrasyon)"))

# ---------- ATÖLYE SAHNELERİ ----------
def sahne(sekil, alt, bg="#f1e6d6"):
    s = HEAD.format(alt=alt).replace("<svg ", '<svg data-zoom="225 175 450 350" ', 1)
    return s + f'<rect width="900" height="700" fill="{bg}"/><rect y="560" width="900" height="140" fill="#e3d3bd"/>{sekil}</svg>'
yaz("atolye-resim", sahne(
    '<g stroke="#8f6a4a" stroke-width="12" stroke-linecap="round"><path d="M450 560 L330 250 M450 560 L570 250 M450 560 V330"/></g>'
    '<rect x="340" y="190" width="220" height="190" fill="#f7f3ec" stroke="#231f1c" stroke-width="6"/>'
    '<path d="M350 340 C400 290 440 330 480 300 C510 280 540 310 552 300 V372 H350Z" fill="#b5542f"/><circle cx="500" cy="240" r="26" fill="#c9a24b"/>'
    '<ellipse cx="650" cy="470" rx="70" ry="40" fill="#efe6da" stroke="#8f6a4a" stroke-width="5"/>'
    '<g><circle cx="620" cy="460" r="12" fill="#b5542f"/><circle cx="655" cy="448" r="12" fill="#c9a24b"/><circle cx="685" cy="470" r="12" fill="#2f5d8a"/><circle cx="640" cy="490" r="12" fill="#8a9a7b"/></g>'
    '<path d="M240 560 V470 M262 560 V455 M284 560 V478" stroke="#231f1c" stroke-width="8" stroke-linecap="round"/>', "Tuval ve palet bulunan resim atölyesi (örnek illüstrasyon)"))
yaz("atolye-heykel", sahne(
    '<rect x="360" y="430" width="180" height="130" fill="#8f6a4a"/><rect x="345" y="418" width="210" height="18" fill="#6d4f35"/>'
    '<path d="M450 418 C395 410 385 340 405 300 C418 270 482 270 495 300 C515 340 505 410 450 418Z" fill="#b5542f"/>'
    '<ellipse cx="450" cy="268" rx="48" ry="58" fill="#c46a43"/><path d="M425 262 q10 -8 20 0 M455 262 q10 -8 20 0 M440 300 q10 8 20 0" stroke="#6d2f1b" stroke-width="5" fill="none" stroke-linecap="round"/>'
    '<g stroke="#231f1c" stroke-width="8" stroke-linecap="round"><path d="M600 560 L650 430"/><path d="M640 560 L700 450"/></g><circle cx="650" cy="425" r="12" fill="#c9a24b"/><circle cx="700" cy="445" r="12" fill="#c9a24b"/>', "Kil portre ve modelaj aletleri olan heykel atölyesi (örnek illüstrasyon)"))
print("üretilen dosya:", len(list(OUT.glob('*.svg'))))

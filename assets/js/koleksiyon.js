/* Koleksiyon ve atölye listeleri: arama, sıralama, dal filtresi (sunucu gerektirmez) */
(function () {
	'use strict';
	var izgara = document.getElementById('izgara');
	if (!izgara) return;
	var ogeler = [].slice.call(izgara.querySelectorAll('.urun-oge'));
	var ara = document.getElementById('ara'), sirala = document.getElementById('sirala');
	var sonuc = document.getElementById('sonuc'), bos = document.getElementById('bos');
	var birim = izgara.getAttribute('data-birim') || 'öğe', filtre = '';
	ogeler.forEach(function (o, i) { o.setAttribute('data-sira', i); });

	function kucuk(s) { return (s || '').toLocaleLowerCase('tr'); }

	function uygula() {
		var q = kucuk(ara.value).trim(), gorunen = 0;
		ogeler.forEach(function (o) {
			var uygun = (!q || kucuk(o.getAttribute('data-ad')).indexOf(q) > -1) && (!filtre || o.getAttribute('data-kat') === filtre);
			o.hidden = !uygun;
			if (uygun) gorunen++;
		});
		var k = sirala.value;
		ogeler.slice().sort(function (a, b) {
			if (k === 'fiyat-art') return a.getAttribute('data-fiyat') - b.getAttribute('data-fiyat');
			if (k === 'fiyat-azal') return b.getAttribute('data-fiyat') - a.getAttribute('data-fiyat');
			if (k === 'ad') return a.getAttribute('data-ad').localeCompare(b.getAttribute('data-ad'), 'tr');
			return a.getAttribute('data-sira') - b.getAttribute('data-sira');
		}).forEach(function (o) { izgara.appendChild(o); });
		sonuc.textContent = gorunen + ' ' + birim + ' gösteriliyor';
		bos.hidden = gorunen > 0;
	}

	ara.addEventListener('input', uygula);
	sirala.addEventListener('change', uygula);
	[].slice.call(document.querySelectorAll('.filtre')).forEach(function (d) {
		d.addEventListener('click', function () {
			filtre = d.getAttribute('data-filtre');
			[].slice.call(document.querySelectorAll('.filtre')).forEach(function (x) {
				var a = x === d; x.classList.toggle('aktif', a); x.setAttribute('aria-pressed', a);
			});
			uygula();
		});
	});
})();

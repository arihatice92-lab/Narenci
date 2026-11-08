/* Narenci grafikleri (Chart.js). Ana sayfa ve admin panelinde ortak kullanılır.
   Veri: <script type="application/json" id="istatistik-veri"> içinden okunur (sunucu gerekmez). */
(function () {
	'use strict';
	if (!window.Chart) return;
	var RENK = { terrakota: '#b0512d', altin: '#c9a24b', adacayi: '#8a9a7b', murekkep: '#231f1c', izgara: '#e3d9cc', metin: '#4a4440' };
	var azalt = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
	Chart.defaults.font.family = '"Jost", sans-serif';
	Chart.defaults.font.size = 14;
	Chart.defaults.color = RENK.metin;
	Chart.defaults.animation = azalt ? false : { duration: 900 };
	var sayi = function (v) { return Number(v).toLocaleString('tr-TR'); };

	function eksenler(ad) {
		return {
			x: { grid: { display: false } },
			y: { beginAtZero: true, grid: { color: RENK.izgara }, ticks: { callback: sayi }, title: ad ? { display: true, text: ad } : undefined }
		};
	}
	var araclar = {
		cizgi: function (cv, v, ad) {
			return new Chart(cv, { type: 'line', data: { labels: v.etiketler, datasets: [{ label: ad, data: v.degerler, borderColor: RENK.terrakota, backgroundColor: 'rgba(176,81,45,.14)', fill: true, tension: .3, borderWidth: 3, pointRadius: 5, pointBackgroundColor: RENK.terrakota, pointBorderColor: '#fff', pointBorderWidth: 2 }] },
				options: { maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return ' ' + sayi(c.parsed.y) + ' ' + ad.toLowerCase(); } } } }, scales: eksenler('') } });
		},
		cubuk: function (cv, v, ad) {
			return new Chart(cv, { type: 'bar', data: { labels: v.etiketler, datasets: [{ label: ad, data: v.degerler, backgroundColor: RENK.terrakota, hoverBackgroundColor: RENK.altin, borderRadius: 4, maxBarThickness: 46 }] },
				options: { maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return ' ' + sayi(c.parsed.y) + ' ' + ad.toLowerCase(); } } } }, scales: eksenler('') } });
		},
		yatay: function (cv, v, ad) {
			return new Chart(cv, { type: 'bar', data: { labels: v.etiketler, datasets: [{ label: ad, data: v.degerler, backgroundColor: RENK.adacayi, hoverBackgroundColor: RENK.terrakota, borderRadius: 4, maxBarThickness: 30 }] },
				options: { indexAxis: 'y', maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { callbacks: { label: function (c) { return ' %' + c.parsed.x + ' ' + ad.toLowerCase(); } } } }, scales: { x: { beginAtZero: true, max: 100, grid: { color: RENK.izgara }, ticks: { callback: function (v) { return '%' + v; } } }, y: { grid: { display: false } } } } });
		},
		halka: function (cv, v, ad, birim) {
			return new Chart(cv, { type: 'doughnut', data: { labels: v.etiketler, datasets: [{ label: ad, data: v.degerler, backgroundColor: [RENK.terrakota, RENK.adacayi, RENK.murekkep, RENK.altin, '#d9b8a4'], borderColor: '#fff', borderWidth: 3, hoverOffset: 8 }] },
				options: { maintainAspectRatio: false, cutout: '62%', plugins: { legend: { position: 'bottom', labels: { padding: 18, usePointStyle: true } }, tooltip: { callbacks: { label: function (c) { return ' ' + c.label + ': ' + (birim === '%' ? '%' + c.parsed : sayi(c.parsed) + (birim ? ' ' + birim : '')); } } } } } });
		}
	};
	window.NarenciGrafik = araclar;

	var veriEl = document.getElementById('istatistik-veri');
	if (!veriEl) return;
	var d = JSON.parse(veriEl.textContent);
	var ornekler = {};
	function kur(id, fn, anahtar, ad, birim) { var cv = document.getElementById(id); if (cv && d[anahtar]) ornekler[id] = fn(cv, d[anahtar], ad, birim); }
	kur('g-katilimci', araclar.cizgi, 'yillik_katilimci', 'Kayıtlı katılımcı');
	kur('g-dal', araclar.halka, 'dal_dagilimi', 'Dal dağılımı', '%');
	kur('g-sergi', araclar.cubuk, 'sergi_yillik', 'Sergi');
	kur('g-eser', araclar.halka, 'eser_dal', 'Eser', 'eser');
	kur('g-yas', araclar.cubuk, 'yas_dagilimi', 'Katılımcı (%)');
	kur('g-seviye', araclar.halka, 'seviye_dagilimi', 'Seviye', '%');
	kur('g-memnuniyet', araclar.yatay, 'memnuniyet', 'Memnuniyet');
	kur('g-ziyaret', araclar.cubuk, 'aylik_ziyaret', 'Ziyaretçi');
	kur('g-onkayit', araclar.cubuk, 'aylik_on_kayit', 'Ön kayıt');
	window.NarenciGrafikOrnekleri = ornekler;
	window.NarenciVeri = d;
})();

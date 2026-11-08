/* İletişim formu: ?konu=... ile gelinirse konu alanını ve mesaj türünü doldurur */
(function () {
	'use strict';
	var konu = '';
	try { konu = new URLSearchParams(window.location.search).get('konu') || ''; } catch (e) { return; }
	if (!konu) return;
	var k = document.getElementById('f-konu'), t = document.getElementById('f-tur');
	if (k) k.value = konu;
	if (t) t.value = 'Bilgi talebi';
	var form = document.getElementById('form');
	if (form && form.scrollIntoView) form.scrollIntoView({ block: 'start' });
})();

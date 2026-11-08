/* Detay sayfası görsel galerisi: küçük resme tıklayınca ana görsel değişir */
(function () {
	'use strict';
	var ana = document.getElementById('galeri-ana');
	if (!ana) return;
	var dugmeler = [].slice.call(document.querySelectorAll('.galeri-dugme'));
	dugmeler.forEach(function (d) {
		d.addEventListener('click', function () {
			ana.src = d.getAttribute('data-src');
			ana.alt = d.getAttribute('data-alt');
			dugmeler.forEach(function (x) { var a = x === d; x.classList.toggle('aktif', a); x.setAttribute('aria-pressed', a); });
		});
	});
})();

/* Örnek formlar: sunucuya göndermez, doğrulama yapıp onay mesajı gösterir */
(function () {
	'use strict';
	[].slice.call(document.querySelectorAll('form[data-demo]')).forEach(function (f) {
		f.addEventListener('submit', function (e) {
			e.preventDefault();
			var s = f.querySelector('.form-sonuc');
			if (!f.checkValidity()) {
				f.reportValidity();
				s.textContent = 'Lütfen zorunlu alanları doldurun.';
				s.className = 'form-sonuc hata';
				return;
			}
			var ap = f.querySelector('.eposta-onizleme');
			if (ap && f.getAttribute('data-alici')) {
				var v = function (n) { return f.elements[n] ? f.elements[n].value : ''; };
				ap.innerHTML = '';
				var bas = document.createElement('strong'); bas.textContent = 'Müşteri ilişkilerine iletilecek e-posta (önizleme)'; ap.appendChild(bas);
				[['Kime', f.getAttribute('data-alici')], ['Kimden', v('eposta')], ['Konu', '[' + v('tur') + '] ' + v('konu')], ['Mesaj', v('mesaj')]].forEach(function (r) {
					var d = document.createElement('div'); var b = document.createElement('b'); b.textContent = r[0] + ': '; d.appendChild(b); d.appendChild(document.createTextNode(r[1])); ap.appendChild(d);
				});
				ap.hidden = false;
			}
			s.textContent = 'Teşekkürler, mesajınız müşteri ilişkileri temsilcisine e-posta ile iletilecek şekilde alındı. (Örnek site: gerçek e-posta gönderilmedi.)';
			s.className = 'form-sonuc basari';
			f.reset();
		});
	});
})();

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
			s.textContent = 'Teşekkürler, bilgileriniz alındı. (Örnek site: form sunucuya gönderilmedi.)';
			s.className = 'form-sonuc basari';
			f.reset();
		});
	});
})();

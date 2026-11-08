/* Narenci yönetim paneli: yalnızca arayüz etkileşimleri (veri sunucuya kaydedilmez) */
(function () {
	'use strict';
	var $ = function (s, k) { return (k || document).querySelector(s); };
	var $$ = function (s, k) { return [].slice.call((k || document).querySelectorAll(s)); };

	function toast(metin) {
		var alan = $('#toast-alani'); if (!alan) return;
		var d = document.createElement('div'); d.className = 'toast-oge'; d.textContent = metin;
		alan.appendChild(d); setTimeout(function () { d.remove(); }, 3600);
	}
	window.NarenciToast = toast;

	/* Mobil yan menü */
	var dugme = $('#menu-dugme'), yan = $('#yan-menu');
	if (dugme && yan) {
		dugme.addEventListener('click', function () {
			var a = yan.classList.toggle('acik'); dugme.setAttribute('aria-expanded', a);
		});
		document.addEventListener('keydown', function (e) { if (e.key === 'Escape') { yan.classList.remove('acik'); dugme.setAttribute('aria-expanded', 'false'); } });
	}

	/* Giriş (demo) */
	var giris = $('#giris-formu');
	if (giris) {
		var goz = $('#sifre-goster'), sf = $('#g-sifre');
		goz.addEventListener('click', function () {
			var gizli = sf.type === 'password'; sf.type = gizli ? 'text' : 'password';
			goz.textContent = gizli ? 'Gizle' : 'Göster'; goz.setAttribute('aria-pressed', gizli);
		});
		giris.addEventListener('submit', function (e) {
			e.preventDefault();
			if (!giris.checkValidity()) { giris.reportValidity(); return; }
			$('#giris-not').textContent = 'Giriş yapılıyor… (demo: doğrulama yapılmaz)';
			setTimeout(function () { location.href = 'panel.html'; }, 600);
		});
	}

	/* Tablo araması */
	$$('[data-ara]').forEach(function (kutu) {
		var tablo = $(kutu.getAttribute('data-ara')); if (!tablo) return;
		var filtre = $(kutu.getAttribute('data-filtre') || '#yok');
		function uygula() {
			var q = kutu.value.toLocaleLowerCase('tr').trim(), tur = filtre ? filtre.value : '', say = 0;
			$$('tbody tr', tablo).forEach(function (tr) {
				var ok = (tr.getAttribute('data-ad') || tr.textContent).toLocaleLowerCase('tr').indexOf(q) > -1 && (!tur || tr.getAttribute('data-tur') === tur);
				tr.hidden = !ok; if (ok) say++;
			});
			var bos = $(kutu.getAttribute('data-bos')); if (bos) bos.hidden = say > 0;
		}
		kutu.addEventListener('input', uygula); if (filtre) filtre.addEventListener('change', uygula);
	});

	/* Silme onayı (ortak modal) */
	var silModal = $('#silModal'), silHedef = null, bsModal = null;
	if (silModal && window.bootstrap) bsModal = new bootstrap.Modal(silModal);
	document.addEventListener('click', function (e) {
		var b = e.target.closest('[data-sil]'); if (!b || !bsModal) return;
		silHedef = b.closest('tr');
		$('#silMetin').textContent = '"' + (silHedef.getAttribute('data-ad') || 'Bu kayıt') + '" silinecek. Bu işlem geri alınamaz (demo).';
		bsModal.show();
	});
	var onay = $('#silOnay');
	if (onay) onay.addEventListener('click', function () {
		if (silHedef) { silHedef.remove(); toast('Kayıt silindi (demo).'); silHedef = null; }
		bsModal.hide();
	});

	/* Karakter sayacı */
	$$('[data-sayac]').forEach(function (alan) {
		var hedef = $(alan.getAttribute('data-sayac')), max = +alan.getAttribute('maxlength') || 160;
		function g() { hedef.textContent = alan.value.length + ' / ' + max; }
		alan.addEventListener('input', g); g();
	});

	/* Dosya yükleme: tür/boyut denetimi + önizleme */
	$$('input[type=file][data-onizleme]').forEach(function (inp) {
		var kap = $(inp.getAttribute('data-onizleme')), hata = $(inp.getAttribute('data-hata'));
		var izinli = (inp.getAttribute('data-turler') || '').split(',');
		var azami = (+inp.getAttribute('data-mb') || 5) * 1024 * 1024;
		inp.addEventListener('change', function () {
			kap.innerHTML = ''; hata.textContent = '';
			var hatalar = [];
			[].slice.call(inp.files).forEach(function (f) {
				var uz = f.name.split('.').pop().toLowerCase();
				if (izinli.indexOf(uz) < 0) { hatalar.push(f.name + ': desteklenmeyen tür (' + izinli.join(', ').toUpperCase() + ')'); return; }
				if (f.size > azami) { hatalar.push(f.name + ': boyut ' + (azami / 1048576) + ' MB sınırını aşıyor'); return; }
				if (/^image\//.test(f.type)) {
					var im = document.createElement('img'); im.alt = f.name + ' önizleme'; im.src = URL.createObjectURL(f); kap.appendChild(im);
				} else {
					var s = document.createElement('span'); s.className = 'dosya-ad'; s.textContent = f.name + ' (' + Math.ceil(f.size / 1024) + ' KB)'; kap.appendChild(s);
				}
			});
			if (hatalar.length) { hata.textContent = hatalar.join(' • '); if (!kap.children.length) inp.value = ''; }
		});
	});

	/* Kayıt formu: kaydet / düzenle / önizle (demo) */
	var form = $('form[data-yonetim]');
	if (form) {
		var bant = $('#duzenleme-bandi'), baslik = $('#kayit-baslik');
		function doldur(k) {
			Object.keys(k).forEach(function (ad) { var el = form.elements[ad]; if (el) { el.value = k[ad]; el.dispatchEvent(new Event('input')); } });
		}
		document.addEventListener('click', function (e) {
			var b = e.target.closest('[data-duzenle]'); if (!b) return;
			var tr = b.closest('tr'); doldur(JSON.parse(tr.getAttribute('data-kayit')));
			if (bant) { bant.classList.add('acik'); $('strong', bant).textContent = tr.getAttribute('data-ad'); }
			form.scrollIntoView({ behavior: 'smooth', block: 'start' });
			var ilk = form.querySelector('input[type=text]'); if (ilk) ilk.focus({ preventScroll: true });
		});
		var iptal = $('#duzenleme-iptal');
		if (iptal) iptal.addEventListener('click', function () { form.reset(); bant.classList.remove('acik'); $$('[data-sayac]', form).forEach(function (a) { a.dispatchEvent(new Event('input')); }); });
		form.addEventListener('reset', function () { setTimeout(function () { $$('.onizleme', form).forEach(function (o) { o.innerHTML = ''; }); }, 0); });
		form.addEventListener('submit', function (e) {
			e.preventDefault();
			if (!form.checkValidity()) { form.reportValidity(); toast('Lütfen zorunlu alanları doldurun.'); return; }
			toast('Kaydedildi (demo: sunucuya gönderilmedi).');
			form.reset(); if (bant) bant.classList.remove('acik');
		});
		var onizleBtn = $('#onizle-btn');
		if (onizleBtn) onizleBtn.addEventListener('click', function () {
			var m = new bootstrap.Modal($('#onizleModal'));
			$('#onizleBaslik').textContent = form.elements.baslik.value || '(Başlık girilmedi)';
			$('#onizleEtiket').textContent = form.elements.etiket ? form.elements.etiket.value : '';
			$('#onizleMetin').textContent = form.elements.icerik.value || form.elements.ozet.value || '(İçerik girilmedi)';
			m.show();
		});
	}

	/* Atölye programı: dinamik satırlar */
	var prog = $('#program-liste'), ekle = $('#program-ekle');
	if (prog && ekle) {
		var n = prog.children.length;
		ekle.addEventListener('click', function () {
			n++;
			var d = document.createElement('div'); d.className = 'prog-satir';
			d.innerHTML = '<input type="text" aria-label="Hafta ' + n + ' başlık" placeholder="Hafta ' + n + ' – başlık">' +
				'<input type="text" aria-label="Hafta ' + n + ' içerik" placeholder="Konu ve kazanımlar">' +
				'<button type="button" class="btn-ikon tehlike" aria-label="Satırı kaldır">Kaldır</button>';
			prog.appendChild(d); d.querySelector('input').focus();
		});
		prog.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) b.parentNode.remove(); });
	}

	/* Mesaj okuma */
	document.addEventListener('click', function (e) {
		var b = e.target.closest('[data-oku]'); if (!b) return;
		var tr = b.closest('tr'), m = new bootstrap.Modal($('#mesajModal'));
		$('#mesajKisi').textContent = tr.getAttribute('data-kisi');
		$('#mesajMeta').textContent = tr.getAttribute('data-tarih') + ' • ' + tr.getAttribute('data-tur');
		$('#mesajKonu').textContent = tr.getAttribute('data-konu');
		$('#mesajMetin').textContent = tr.getAttribute('data-mesaj');
		var r = $('.rozet', tr.children[4]); if (r) { r.textContent = 'Okundu'; r.className = 'rozet yesil'; }
		m.show();
	});
	var yanit = $('#mesaj-yanitla');
	if (yanit) yanit.addEventListener('click', function () { toast('Yanıt penceresi demo amaçlıdır.'); });

	/* İstatistik düzenleme: tablodaki değerler grafiği canlı günceller */
	var duzen = $$('table[data-grafik]');
	if (duzen.length && window.NarenciVeri && window.NarenciGrafikOrnekleri) {
		duzen.forEach(function (t) {
			var ch = window.NarenciGrafikOrnekleri[t.getAttribute('data-grafik')]; if (!ch) return;
			t.addEventListener('input', function (e) {
				if (!e.target.matches('input')) return;
				var dz = $$('tbody tr', t).map(function (tr) { return Math.max(0, +tr.querySelector('input').value || 0); });
				ch.data.datasets[0].data = dz; ch.update();
			});
		});
		$$('[data-kaydet]').forEach(function (b) { b.addEventListener('click', function () { toast('Değerler güncellendi (demo: yalnızca bu sayfada).'); }); });
	}
})();

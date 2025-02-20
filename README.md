API README :
📖 FastAPI Tabanlı Telemetri & Kilitlenme API - README

Bu proje, FastAPI kullanılarak geliştirilmiş bir telemetri, QR, kamikaze ve kilitlenme verisi yönetim API’sidir. MongoDB ile entegre edilmiştir ve kullanıcı kimlik doğrulama işlemlerini destekler.

🚀 Kurulum ve Çalıştırma

1️⃣ Gereksinimler

Bu API’yi çalıştırmak için aşağıdaki yazılımlar sisteminizde kurulu olmalıdır:
	•	Python 3.8+
	•	MongoDB (Atlas veya Yerel)
	•	pip paket yöneticisi

2️⃣ Bağımlılıkları Yükleme

Gerekli Python kütüphanelerini yüklemek için aşağıdaki komutu çalıştırın:

pip install fastapi uvicorn pymongo pydantic

3️⃣ API’yi Çalıştırma

Aşağıdaki komut ile FastAPI sunucusunu başlatabilirsiniz:

python api.py

API, localhost üzerinde 8001 portunda çalışacaktır. Tarayıcıda Swagger UI’ye erişmek için:

http://127.0.0.1:8001/docs

📌 API Bitiş Noktaları (Endpoints)

1️⃣ Kullanıcı Girişi
	•	URL: /api/giris
	•	Metod: POST
	•	Açıklama: Kullanıcı adı ve şifre ile oturum açmayı sağlar.

🔹 Örnek İstek

{
  "kadi": "iktuavarac1",
  "sifre": "123456"
}

✅ Başarılı Yanıt

{
  "message": "Giriş başarılı!",
  "kadi": "iktuavarac1"
}

❌ Başarısız Yanıt

{
  "detail": "Kullanıcı adı veya şifre hatalı."
}

2️⃣ Sunucu Saatini Alma
	•	URL: /api/sunucusaati
	•	Metod: GET
	•	Açıklama: Sunucunun UTC saatini döner.

✅ Başarılı Yanıt

{
  "gun": 21,
  "saat": 14,
  "dakika": 30,
  "saniye": 12,
  "milisaniye": 456
}

3️⃣ Telemetri Verisi Gönderme
	•	URL: /api/telemetri_gonder
	•	Metod: POST
	•	Açıklama: İHA’nın anlık uçuş verilerini sunucuya iletir.

🔹 Örnek İstek

{
  "takim_numarasi": 1,
  "iha_enlem": 41.508775,
  "iha_boylam": 36.118335,
  "iha_irtifa": 38,
  "iha_dikilme": 7,
  "iha_yonelme": 210,
  "iha_yatis": -30,
  "iha_hiz": 28,
  "iha_batarya": 50,
  "iha_otonom": 1,
  "iha_kilitlenme": 1,
  "hedef_merkez_X": 300,
  "hedef_merkez_Y": 230,
  "hedef_genislik": 30,
  "hedef_yukseklik": 43,
  "gps_saati": {"saat": 11, "dakika": 38, "saniye": 37, "milisaniye": 654}
}

✅ Başarılı Yanıt

{
  "message": "Telemetri başarıyla kaydedildi.",
  "sunucusaati": {
    "gun": 21,
    "saat": 14,
    "dakika": 32,
    "saniye": 5,
    "milisaniye": 987
  }
}

❌ Hata - Hız Sınırı Aşıldı

{
  "detail": "Hız sınırı aşıldı! Maksimum 50 m/s olmalı."
}

4️⃣ Kilitlenme Verisi Gönderme
	•	URL: /api/kilitlenme_gonder
	•	Metod: POST
	•	Açıklama: Kilitlenme olaylarını sunucuya kaydeder.

🔹 Örnek İstek

{
  "kilitlenmeBaslangicZamani": {"saat": 11, "dakika": 40, "saniye": 51, "milisaniye": 478},
  "kilitlenmeBitisZamani": {"saat": 11, "dakika": 41, "saniye": 3, "milisaniye": 141},
  "otonom_kilitlenme": 1
}

✅ Başarılı Yanıt

{
  "message": "Kilitlenme verisi başarıyla kaydedildi.",
  "sunucusaati": {
    "gun": 21,
    "saat": 14,
    "dakika": 35,
    "saniye": 15,
    "milisaniye": 342
  },
  "kilitlenmeVerisi": {
    "kilitlenmeBaslangicZamani": {"saat": 11, "dakika": 40, "saniye": 51, "milisaniye": 478},
    "kilitlenmeBitisZamani": {"saat": 11, "dakika": 41, "saniye": 3, "milisaniye": 141},
    "otonom_kilitlenme": 1
  }
}

5️⃣ Tüm Kilitlenme Verilerini Alma
	•	URL: /api/kilitlenme_verileri
	•	Metod: GET
	•	Açıklama: Tüm kaydedilmiş kilitlenme verilerini getirir.

✅ Başarılı Yanıt

[
  {
    "kilitlenmeBaslangicZamani": {"saat": 11, "dakika": 40, "saniye": 51, "milisaniye": 478},
    "kilitlenmeBitisZamani": {"saat": 11, "dakika": 41, "saniye": 3, "milisaniye": 141},
    "otonom_kilitlenme": 1
  }
]

❌ Veri Yoksa

{
  "message": "Kilitlenme verisi bulunamadı."
}

🔧 Geliştirme ve Debugging
	•	FastAPI geliştirme modunda çalıştırmak için:

uvicorn api:app --reload --host 0.0.0.0 --port 8001


	•	API’ye yapılan tüm çağrıları Swagger UI’de test edebilirsiniz:

http://127.0.0.1:8001/docs

📌 Notlar
	•	API, MongoDB Atlas üzerinde çalışmaktadır. Eğer yerel bir MongoDB kullanacaksanız, MongoDB bağlantı URI’sini değiştirmelisiniz.
	•	Yetkilendirme sistemi basit bir kullanıcı adı ve şifre doğrulama mekanizmasına sahiptir.
	•	Hız limiti gibi bazı güvenlik kontrolleri API içerisinde uygulanmıştır.

Bu API, Teknofest yarışmaları ve otonom İHA projeleri için telemetri, kilitlenme ve kamikaze verisi yönetimini sağlamak amacıyla geliştirilmiştir.




--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


CLİENT

API Test Script - README

Bu belge, API test scriptinin nasıl çalıştırılacağını ve hangi fonksiyonları içerdiğini açıklamaktadır.

📌 Gereksinimler
	•	Python 3.x yüklü olmalıdır.
	•	requests modülü yüklü olmalıdır. (Yüklemek için: pip install requests)
	•	API sunucusu çalışır durumda olmalıdır.

🚀 Kullanım

1️⃣ Scripti Çalıştırma

Terminal veya komut istemcisinde aşağıdaki komutu çalıştırın:

python test_api.py

Eğer giriş başarılı olursa, tüm testler otomatik olarak çalışacaktır.

📜 API Test Fonksiyonları

1. Giriş (Authentication)
	•	Fonksiyon: authenticate()
	•	Endpoint: /api/giris
	•	Açıklama: Kullanıcı adı ve şifre ile API’ye giriş yapar.

2. Sunucu Saati Testi
	•	Fonksiyon: test_sunucusaati()
	•	Endpoint: /api/sunucusaati
	•	Açıklama: API sunucusunun saatini kontrol eder.

3. Telemetri Verisi Gönderme Testi
	•	Fonksiyon: test_telemetri_gonder()
	•	Endpoint: /api/telemetri_gonder
	•	Açıklama: İHA’nın konum, hız, batarya gibi telemetri verilerini API’ye gönderir.

4. QR Verisi Gönderme Testi
	•	Fonksiyon: test_qr_gonder()
	•	Endpoint: /api/qr_gonder
	•	Açıklama: QR koddan alınan konum verilerini API’ye gönderir.

5. Kamikaze Verisi Gönderme Testi
	•	Fonksiyon: test_kamikaze_gonder()
	•	Endpoint: /api/kamikaze_gonder
	•	Açıklama: Kamikaze başlangıç/bitiş zamanlarını ve QR metnini API’ye gönderir.

6. Kilitlenme Verisi Gönderme Testi
	•	Fonksiyon: test_kilitlenme_gonder()
	•	Endpoint: /api/kilitlenme_gonder
	•	Açıklama: Kilitlenme başlangıç/bitiş zamanlarını API’ye gönderir.

7. Kilitlenme Verilerini Getirme Testi
	•	Fonksiyon: test_kilitlenme_verileri()
	•	Endpoint: /api/kilitlenme_verileri
	•	Açıklama: API’de kayıtlı olan kilitlenme verilerini getirir.

8. Alan Bilgisi Alma Testi
	•	Fonksiyon: test_alanbilgileri()
	•	Endpoint: /api/alanbilgileri
	•	Açıklama: Alan bilgilerini API’den çeker.

⚠️ Olası Hatalar ve Çözümler
	1.	Bağlantı Hatası:
	•	API sunucusunun çalıştığından emin olun.
	•	BASE_URL adresini kontrol edin.
	2.	Kimlik Doğrulama Başarısız:
	•	Kullanıcı adı ve şifreyi doğrulayın.
	3.	Yanıt Alınamıyor:
	•	API endpoint’lerinin doğru çalıştığını test edin.

Bu test scripti, API’nin tüm temel fonksiyonlarını test etmek için tasarlanmıştır. Hata durumlarında yanıt kodlarını ve mesajlarını kontrol ederek gerekli düzeltmeleri yapabilirsiniz.



























import requests

# API Sunucu Adresi
BASE_URL = 'http://127.0.0.1:8001'


# 1. Giriş (Authentication)
def authenticate():
    url = f'{BASE_URL}/api/giris'
    payload = {
        'kadi': 'iktuavarac1',
        'sifre': '123456'
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Giriş başarılı:", response.json())
        return True
    else:
        print("❌ Giriş hatası:", response.status_code, response.text)
        return False


# 2. Sunucu Saati Testi
def test_sunucusaati():
    url = f'{BASE_URL}/api/sunucusaati'
    response = requests.get(url)
    if response.status_code == 200:
        print("✅ Sunucu Saati:", response.json())
    else:
        print("❌ Sunucu Saati Hatası:", response.status_code, response.text)


# 3. Telemetri Verisi Gönderme Testi
def test_telemetri_gonder():
    url = f'{BASE_URL}/api/telemetri_gonder'
    payload = {
        'takim_numarasi': 1,
        'iha_enlem': 41.508775,
        'iha_boylam': 36.118335,
        'iha_irtifa': 38,
        'iha_dikilme': 7,
        'iha_yonelme': 210,
        'iha_yatis': -30,
        'iha_hiz': 28,
        'iha_batarya': 50,
        'iha_otonom': 1,
        'iha_kilitlenme': 1,
        'hedef_merkez_X': 300,
        'hedef_merkez_Y': 230,
        'hedef_genislik': 30,
        'hedef_yukseklik': 43,
        'gps_saati': {"saat": 11, "dakika": 38, "saniye": 37, "milisaniye": 654}
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Telemetri Gönderme Başarılı:", response.json())
    else:
        print("❌ Telemetri Hatası:", response.status_code, response.text)


# 4. QR Verisi Gönderme Testi
def test_qr_gonder():
    url = f'{BASE_URL}/api/qr_gonder'
    payload = {
        "qrEnlem": 41.51238882,
        "qrBoylam": 36.11935778
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ QR Verisi Gönderme Başarılı:", response.json())
    else:
        print("❌ QR Gönderme Hatası:", response.status_code, response.text)


# 5. Kamikaze Verisi Gönderme Testi
def test_kamikaze_gonder():
    url = f'{BASE_URL}/api/kamikaze_gonder'
    payload = {
        "kamikazeBaslangicZamani": {"saat": 11, "dakika": 44, "saniye": 13, "milisaniye": 361},
        "kamikazeBitisZamani": {"saat": 11, "dakika": 44, "saniye": 27, "milisaniye": 874},
        "qrMetni": "teknofest2024"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Kamikaze Gönderme Başarılı:", response.json())
    else:
        print("❌ Kamikaze Hatası:", response.status_code, response.text)


# 6. Kilitlenme Verisi Gönderme Testi
def test_kilitlenme_gonder():
    url = f'{BASE_URL}/api/kilitlenme_gonder'
    payload = {
        "kilitlenmeBaslangicZamani": {"saat": 11, "dakika": 40, "saniye": 51, "milisaniye": 478},
        "kilitlenmeBitisZamani": {"saat": 11, "dakika": 41, "saniye": 3, "milisaniye": 141},
        "otonom_kilitlenme": 1
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("✅ Kilitlenme Gönderme Başarılı:", response.json())
    else:
        print("❌ Kilitlenme Gönderme Hatası:", response.status_code, response.text)


# 7. Kilitlenme Verilerini Getirme Testi
def test_kilitlenme_verileri():
    url = f'{BASE_URL}/api/kilitlenme_verileri'
    response = requests.get(url)
    if response.status_code == 200:
        print("✅ Kilitlenme Verileri:", response.json())
    else:
        print("❌ Kilitlenme Verisi Alma Hatası:", response.status_code, response.text)


# 8. Alan Bilgisi Alma Testi
def test_alanbilgileri():
    url = f'{BASE_URL}/api/alanbilgileri'
    response = requests.get(url)
    if response.status_code == 200:
        print("✅ Alan Bilgileri Başarılı:", response.json())
    else:
        print("❌ Alan Bilgileri Hatası:", response.status_code, response.text)


if __name__ == '__main__':
    if authenticate():
        test_sunucusaati()
        test_telemetri_gonder()
        test_qr_gonder()
        test_kamikaze_gonder()
        test_kilitlenme_gonder()
        test_kilitlenme_verileri()
        test_alanbilgileri()
    else:
        print("Testlere başlanamadı; giriş yapılamadı.")
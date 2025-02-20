from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import uvicorn
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# MongoDB connection
uri = "mongodb+srv://taharidvanozturk:YqSjxwHRahCkpGQS@savasan.l6fyssf.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.savasan
takim_collection = db["takimbilgileri"]
telemetri_collection = db["telemetri"]
qr_collection = db["qr_verileri"]
kamikaze_collection = db["kamikaze"]
kilitlenme_collection = db["kilitlenme"]
hss_collection = db["hss_koordinatlari"]
alan_bilgileri_collection = db["yarisma_alan_bilgileri"]


class GirisData(BaseModel):
    kadi: str
    sifre: str


class TelemetriData(BaseModel):
    takim_numarasi: int = Field(..., gt=0)
    iha_enlem: float
    iha_boylam: float
    iha_irtifa: float
    iha_dikilme: float = Field(..., ge=-90, le=90)
    iha_yonelme: float = Field(..., ge=0, le=360)
    iha_yatis: float = Field(..., ge=-90, le=90)
    iha_hiz: float = Field(..., ge=0)
    iha_batarya: int = Field(..., ge=0, le=100)
    iha_otonom: int = Field(..., ge=0, le=1)
    iha_kilitlenme: int = Field(..., ge=0, le=1)
    hedef_merkez_X: int = Field(0, ge=0)
    hedef_merkez_Y: int = Field(0, ge=0)
    hedef_genislik: int = Field(0, ge=0)
    hedef_yukseklik: int = Field(0, ge=0)
    gps_saati: dict


class QRData(BaseModel):
    qrEnlem: float
    qrBoylam: float


class KamikazeData(BaseModel):
    kamikazeBaslangicZamani: dict
    kamikazeBitisZamani: dict
    qrMetni: str


class KilitlenmeData(BaseModel):
    kilitlenmeBaslangicZamani: dict
    kilitlenmeBitisZamani: dict
    otonom_kilitlenme: int = Field(..., ge=0, le=1)


class UserSession:
    def __init__(self):
        self.authenticated_user = None

    def authenticate_user(self, kadi: str, sifre: str):
        query = {"kadi": kadi, "sifre": sifre}
        result = takim_collection.find_one(query)
        if result:
            self.authenticated_user = result["kadi"]
            return True
        else:
            return False

    def is_authenticated(self):
        return self.authenticated_user is not None

    def get_authenticated_user(self):
        return self.authenticated_user


user_session = UserSession()
app = FastAPI()


# Giriş (Authentication) endpoint'i
@app.post("/api/giris")
async def giris(giris_data: GirisData):
    if user_session.authenticate_user(giris_data.kadi, giris_data.sifre):
        return {"message": "Giriş başarılı!", "kadi": giris_data.kadi}
    else:
        raise HTTPException(status_code=401, detail="Kullanıcı adı veya şifre hatalı.")


def get_current_user():
    if not user_session.is_authenticated():
        raise HTTPException(status_code=401, detail="Yetkisiz giriş denemesi!")
    return user_session.get_authenticated_user()


@app.get("/api/sunucusaati")
async def sunucu_saati():
    now = datetime.utcnow()
    return {
        "gun": now.day,
        "saat": now.hour,
        "dakika": now.minute,
        "saniye": now.second,
        "milisaniye": now.microsecond // 1000
    }


@app.post("/api/telemetri_gonder")
async def telemetri_gonder(telemetri_verisi: TelemetriData, current_user: str = Depends(get_current_user)):
    now = datetime.utcnow()
    telemetri_verisi = telemetri_verisi.dict()
    telemetri_verisi["timestamp"] = now

    takim_no = telemetri_verisi["takim_numarasi"]
    if not takim_no:
        raise HTTPException(status_code=400, detail="Takım numarası eksik.")

    if telemetri_verisi["iha_hiz"] > 50:
        raise HTTPException(status_code=400, detail="Hız sınırı aşıldı! Maksimum 50 m/s olmalı.")

    telemetri_collection.insert_one(telemetri_verisi)

    return {
        "message": "Telemetri başarıyla kaydedildi.",
        "sunucusaati": await sunucu_saati(),
    }


@app.post("/api/kilitlenme_gonder")
async def kilitlenme_gonder(kilitlenme_verisi: KilitlenmeData, current_user: str = Depends(get_current_user)):
    now = datetime.utcnow()
    kilitlenme_verisi = kilitlenme_verisi.dict()
    kilitlenme_verisi["timestamp"] = now

    kilitlenme_collection.insert_one(kilitlenme_verisi)

    return {
        "message": "Kilitlenme verisi başarıyla kaydedildi.",
        "sunucusaati": await sunucu_saati(),
        "kilitlenmeVerisi": kilitlenme_verisi
    }


@app.get("/api/kilitlenme_verileri")
async def get_kilitlenme_verileri(current_user: str = Depends(get_current_user)):
    results = list(kilitlenme_collection.find({}, {"_id": 0}))
    return results if results else {"message": "Kilitlenme verisi bulunamadı."}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="info")
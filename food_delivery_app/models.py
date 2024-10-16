from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class UserType:
    NORMAL_USER = 'normal_user'
    RESTAURANT_OWNER = 'restaurant_owner'
    KURYE_USER = "kurye_user"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique = True)
    email = email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    tel_no = db.Column(db.Integer)
    surname = db.Column(db.String(100))
    siparisler = db.relationship("Siparis", backref="user")
    adresler = db.relationship("Adres", backref="user")
    bakiye = db.Column(db.Float)

class Restoran(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique = True)
    kod = db.Column(db.String(100), unique = True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    tel_no = db.Column(db.Integer)
    siparisler = db.relationship("Siparis", backref="Restoran")
    urunler = db.relationship("Urun", backref="Restoran")
    adres = db.relationship("Restoran_adres", backref="Restoran")
    user_type = UserType.RESTAURANT_OWNER

class Kurye(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, unique = True)
    email = email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    tel_no = db.Column(db.Integer)
    user_type = UserType.KURYE_USER

class Siparis(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique = True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    restoran_id = db.Column(db.Integer, db.ForeignKey("restoran.id"))
    urun_id = db.Column(db.Integer)
    durum = db.Column(db.String)
    fiyat = db.Column(db.Integer)
    odeme_yontemi = db.Column(db.String)
    is_active = db.Column(db.Boolean)

class Urun(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique = True)
    restoran_id = db.Column(db.Integer, db.ForeignKey("restoran.id"))
    urun_adı = db.Column(db.String(100))
    acıklaması = db.Column(db.String(100))
    fiyat = db.Column(db.Integer)
    img_source = db.Column(db.String)

class Adres(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique = True)
    baslık = db.Column(db.String(100))
    il = db.Column(db.String(100))
    ilce = db.Column(db.String(100))
    acıklama = db.Column(db.String(150))
    aktiflik = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = True)

class Restoran_adres(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique = True)
    il = db.Column(db.String(100))
    ilce = db.Column(db.String(100))
    acıklama = db.Column(db.String(150))
    restoran_id = db.Column(db.Integer, db.ForeignKey("restoran.id"), nullable = False)
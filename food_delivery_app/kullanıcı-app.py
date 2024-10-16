from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from models import User, db, Adres, Restoran, Restoran_adres, Urun, Siparis
import datetime
from flask_socketio import SocketIO, send, emit
# create the extension
# Users db = db2
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SECRET_KEY"] = "gizli-anahtar"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# initialize the app with the extension
db.init_app(app)

socketio = SocketIO(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view= "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    with app.app_context():
        return db.session.query(User).get(int(user_id))

sepet = []
sepet_toplam = []

@app.route("/")
@login_required
def index():
    currrent_time = datetime.datetime.now().time()
    currrent_time = str(currrent_time)
    a, b = currrent_time.split(".")
    saat, dakika, saniye = a.split(":")
    saat=int(saat)

    adres = Adres.query.filter_by(user_id = current_user.id, aktiflik = True).first()
    name = current_user.name
    index_restoran = []
    restoran_adresses = Restoran_adres.query.filter_by(ilce=adres.ilce).all()
    for adress in restoran_adresses:
        restoran = Restoran.query.filter_by(id=adress.restoran_id).first()
        index_restoran.append(restoran)
    return render_template("index.html", name=name, adres=adres, index_restoran=index_restoran, sepet=sepet, restoran=Restoran, saat=saat)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method=="POST":
        if request.form.get("user_email") and request.form.get("user_password"):
            email = request.form.get("user_email")
            password = request.form.get("user_password")
            user = User.query.filter_by(email=email).first()
            if user.email == email and user.password == password:
                login_user(user)
                return redirect(url_for("index"))
    return render_template("kullanıcı_login.html", user = current_user)

@app.route("/adres_ekle_kayıt", methods=["GET", "POST"])
@login_required
def adres_ekle_kayıt():
    if request.method=="POST":
        baslık = request.form.get("baslık")
        il = request.form.get("il")
        ilce = request.form.get("ilce")
        acıklama = request.form.get("acıklama")

        new_adress = Adres(
            baslık=baslık,
            il=il,
            ilce=ilce,
            acıklama=acıklama,
            aktiflik = True,
            user_id=current_user.id
        )
        db.session.add(new_adress)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("kullanıcı-kayıt-adres.html")


@app.route("/kullanıcı_kayıt", methods = ["GET", "POST"])
def kullanıcı_kayıt():
    if request.method=="POST":
        name = request.form.get("kullanıcı_ad")
        surname = request.form.get("kullanıcı_soyad")
        email = request.form.get("kullanıcı_kayıt_email")
        password = request.form.get("kullanıcı_kayıt_password")
        telefon = request.form.get("kullanıcı_telefon")
        
        new_user = User(
            email = email,
            password = password,
            name = name,
            tel_no = telefon,
            surname = surname,
            bakiye = 0
        )

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        return redirect(url_for("adres_ekle_kayıt"))
    return render_template("kullanıcı_kayıt.html", user=current_user)

@app.route("/profilim/<int:id>", methods = ["GET", "POST"])
@login_required
def profilim(id):
    user = db.session.query(User).filter_by(id=int(id)).first()
    return render_template("kullanıcı-profil.html", user=user)

@app.route("/logout")
@login_required
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/adreslerim")
@login_required
def adreslerim():
    adresses = Adres.query.filter_by(user_id = current_user.id)
    return render_template("kullanıcı-adres.html", adresses=adresses)

@app.route("/adres_ekle", methods = ["POST", "GET"])
@login_required
def adres_ekle():
    il = request.form.get("il")
    ilce = request.form.get("ilce")
    baslık = request.form.get("baslık")
    acıklama = request.form.get("acıklama")
    if not Adres.query.filter_by(user_id=current_user.id).first():
        aktiflik = True
    else:
        aktiflik = False
    new_adress = Adres(baslık=baslık, il=il, ilce=ilce, aktiflik = aktiflik, user_id = current_user.id, acıklama=acıklama)
    db.session.add(new_adress)
    db.session.commit()
    return redirect(url_for("adreslerim"))

@app.route("/adres_sil/<int:id>")
@login_required
def adres_sil(id):
    adres = Adres.query.filter_by(id=id).first()
    db.session.delete(adres)
    db.session.commit()
    return redirect(url_for("adreslerim"))

@app.route("/aktive_et/<int:id>")
@login_required
def aktive_et(id):
    if Adres.query.filter_by(aktiflik = True).first():
        aktif_adres = Adres.query.filter_by(aktiflik = True).first()
        aktif_adres.aktiflik = False
        db.session.commit()
    yeni_aktif=Adres.query.filter_by(id=id).first()
    yeni_aktif.aktiflik = True
    db.session.commit()
    return redirect(url_for("adreslerim"))

@app.route("/restoran/<int:id>", methods=["POST", "GET"])
@login_required
def restoran(id):
    restoran = Restoran.query.filter_by(id=id).first()
    urunler = Urun.query.filter_by(restoran_id=id).all()
    return render_template("kullanıcı-urunler.html", restoran=restoran, urunler=urunler, sepet=sepet)

@app.route("/sepete_ekle/<int:id>", methods=["GET", "POST"])
@login_required
def sepete_ekle(id):
    urun = Urun.query.filter_by(id=id).first()
    sepet.append(urun)
    fiyat = Urun.query.filter_by(id=urun.id).first().fiyat
    sepet_toplam.append(fiyat)
    return redirect(url_for("restoran", id=urun.restoran_id))

@app.route("/sepetten_cıkar/<int:id>", methods=["POST", "GET"])
@login_required
def sepetten_cıkar(id):
    id=int(id)
    id = id-1
    del sepet[id]
    return redirect(url_for("index"))


@app.route("/siparis_ver", methods = ["POST", "GET"])
@login_required
def siparis_ver():
    odeme_yontemi = request.form.get("odeme_yontemi")
    for urun in sepet:
        siparis = Siparis(
            user_id = current_user.id,
            restoran_id = urun.restoran_id,
            urun_id = urun.id,
            durum = "Sipariş alındı",
            fiyat = urun.fiyat,
            is_active = True,
            odeme_yontemi = odeme_yontemi
        )
        db.session.add(siparis)
        db.session.commit()
    return redirect(url_for("index"))

@app.route("/siparislerim", methods=["POST", "GET"])
@login_required
def siparislerim():
    siparisler = Siparis.query.filter_by(user_id = current_user.id, is_active=True).all()
    return render_template("kullanıcı-siparisler.html", siparisler=siparisler, restoran=Restoran, urun=Urun, adres=Adres)

@app.route("/iptal_et/<int:i>", methods=["POST", "GET"])
@login_required
def iptal_et(i):
    siparis = Siparis.query.filter_by(id=i).first()
    db.session.delete(siparis)
    db.session.commit()
    return redirect(url_for("siparislerim"))

@app.route("/ara", methods = ["POST", "GET"])
@login_required
def ara():
    arama_içeriği = request.form.get("arama")
    arama_içeriği  = arama_içeriği.strip().lower()
    user_adres = Adres.query.filter_by(user_id=current_user.id, aktiflik=True).first()
    restoran_adresleri = Restoran_adres.query.filter_by(il=user_adres.il).all()
    for restoran_adres in restoran_adresleri:
        restoran = Restoran.query.filter_by(id=restoran_adres.restoran_id).first()
        restoran_ad  = str(restoran.name).strip().lower()
        if restoran_ad == arama_içeriği:
            return redirect(url_for("restoran", id=restoran.id))


if __name__ == "__main__":
    app.run(debug=True)
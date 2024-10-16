from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_user, LoginManager, login_required, current_user, logout_user
from code_maker import generate_random_code
from models import User, Restoran, db, Restoran_adres, Urun, Adres, Siparis
# Users db = db2
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SECRET_KEY"] = "gizli-anahtar"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.login_view= "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(restoran_id):
    return Restoran.query.get(int(restoran_id))

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method=="POST":
        if request.form.get("restoran_email") and request.form.get("restoran_password"):
            email = request.form.get("restoran_email")
            password = request.form.get("restoran_password")
            user = Restoran.query.filter_by(email=email).first()
            if user.email == email and user.password == password:
                login_user(user)
                return redirect(url_for("index"))
    return render_template("restoran-login.html", user = current_user)

@app.route("/restoran_kayıt", methods = ["GET", "POST"])
def restoran_kayıt():
    if request.method=="POST":
        name = request.form.get("restoran_ad")
        email = request.form.get("restoran_email")
        password = request.form.get("restoran_sifre")
        telefon = request.form.get("restoran_telefon")

        restoran_kod=generate_random_code()
        
        new_restoran = Restoran(
            email = email,
            password = password,
            name = name,
            tel_no = telefon,
            kod = restoran_kod
        )
        db.session.add(new_restoran)
        db.session.commit()
        login_user(new_restoran)
        return redirect(url_for("restoran_adres_ekle"))
    return render_template("restoran_kayıt.html", new_restoran = current_user)

@app.route("/restoran_adres_ekle", methods=["GET", "POST"])
@login_required
def restoran_adres_ekle():
    if request.method=="POST":
        il = request.form.get("il")
        ilce = request.form.get("ilce")
        acıklama = request.form.get("acıklama")

        adress = Restoran_adres(
            il=il,
            ilce=ilce,
            acıklama=acıklama,
            restoran_id=current_user.id
        )
        db.session.add(adress)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("restoran_adres.html")

@app.route("/")
@login_required
def index():
    user = Restoran.query.filter_by(id=current_user.id).first()
    adress = Restoran_adres.query.filter_by(restoran_id=current_user.id).first()
    return render_template("restoran_profil.html", user=user, adress=adress)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/urunler", methods=["POST", "GET"])
@login_required
def urunler():
    urunler = Urun.query.filter_by(restoran_id=current_user.id).all()
    return render_template("restoran-urunler.html", urunler=urunler)

@app.route("/urun_ekle", methods=["POST", "GET"])
@login_required
def urun_ekle():
    if request.method=="POST":
        urun_ad = request.form.get("urun-ad")
        urun_acıklama = request.form.get("urun-acıklama")
        urun_fiyat = request.form.get("urun-fiyat")
        urun_img = request.form.get("urun-img")
        
        new_product = Urun(
            restoran_id = current_user.id,
            urun_adı = urun_ad,
            acıklaması= urun_acıklama,
            fiyat = int(urun_fiyat),
            img_source = urun_img
        )
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("urunler"))
    return render_template("restoran-urun-ekle.html")

@app.route("/urun_sil/<int:id>", methods=["POST", "GET"])
@login_required
def urun_sil(id):
    urun = Urun.query.filter_by(id=id).first()
    db.session.delete(urun)
    db.session.commit()
    return redirect(url_for("urunler"))

@app.route("/urun_guncelle/<int:id>", methods=["POST", "GET"])
@login_required
def guncelle(id):
    urun = Urun.query.filter_by(id=id).first()
    if request.method=="POST":
        urun_ad = request.form.get("urun-ad")
        urun_acıklama = request.form.get("urun-acıklama")
        urun_fiyat = request.form.get("urun-fiyat")
        urun_img = request.form.get("urun-img")
    
        urun.urun_adı = urun_ad
        urun.acıklaması = urun_acıklama
        urun.fiyat = int(urun_fiyat)
        urun.img_source = urun_img
        db.session.commit()
        return redirect(url_for("urunler"))
    return render_template("restoran-urun-guncelle.html", urun=urun)

@app.route("/siparislerim", methods=["POST", "GET"])
@login_required
def siparisler():
    siparislerim = Siparis.query.filter_by(restoran_id= current_user.id, is_active=True).all()
    return render_template("restoran_siparis.html", siparis=Siparis, urun=Urun, user=User, siparislerim=siparislerim, adres=Adres)

@app.route("/siparis_guncelle/<int:id>", methods =["POST", "GET"])
@login_required
def siparis_guncele(id):
    siparis = Siparis.query.filter_by(id=id).first()
    yeni_durum = request.form.get("durum")
    print(yeni_durum)
    siparis.durum = yeni_durum
    db.session.commit()
    return redirect(url_for("siparisler"))

@app.route("/iptal_et/<int:i>", methods=["GET", "POST"])
@login_required
def iptal_et(i):
    siparis = Siparis.query.filter_by(id=i).first()
    siparis.durum = "İptal edildi"
    db.session.commit()
    return redirect(url_for("siparisler"))

if __name__ == "__main__":
    app.run(debug=True)
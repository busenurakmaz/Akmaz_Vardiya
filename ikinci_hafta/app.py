from flask import Flask, render_template, redirect, url_for, request, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import locale
import os
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'gelistirme_anahtari'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Türkçe tarih ayarı
try:
    locale.setlocale(locale.LC_TIME, 'tr_TR.UTF-8')
except locale.Error:
    pass  # Sistem desteklemiyorsa geç

# MODELLER

class Vardiya(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    baslangic = db.Column(db.String(10), nullable=False)  # Örn: '08:00'
    bitis = db.Column(db.String(10), nullable=False)       # Örn: '16:00'
    personel_id = db.Column(db.Integer, db.ForeignKey('personel.id'), nullable=False)
    tarih = db.Column(db.Date, nullable=False)

    personel = db.relationship('Personel', backref=db.backref('vardiyalar', lazy=True))

    def __repr__(self):
        return f"{self.tarih} - {self.baslangic}-{self.bitis}"

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

class Personel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ad_soyad = db.Column(db.String(200), nullable=False)
    departman = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'ad_soyad': self.ad_soyad,
            'departman': self.departman
        }

class GirisKaydi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tarih_saat = db.Column(db.DateTime, nullable=False)
    cikis_saat = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('giris_kayitlari', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'tarih_saat': self.tarih_saat.strftime('%Y-%m-%d %H:%M:%S'),
            'cikis_saat': self.cikis_saat.strftime('%Y-%m-%d %H:%M:%S') if self.cikis_saat else None,
            'user_id': self.user_id
        }

# LOGIN
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def before_request():
    g.user = current_user

# ROUTE'LER

@app.route("/vardiya/sil/<int:vardiya_id>", methods=["POST"])
def vardiya_sil(vardiya_id):
    vardiya = Vardiya.query.get_or_404(vardiya_id)
    db.session.delete(vardiya)
    db.session.commit()
    flash("Vardiya başarıyla silindi.", "success")
    return redirect(url_for("vardiya_listesi"))

@app.route('/vardiya/listesi')
@login_required
def vardiya_listesi():
    vardiyalar = Vardiya.query.order_by(Vardiya.tarih.desc()).all()
    return render_template('vardiya_listesi.html', vardiyalar=vardiyalar)

@app.route("/vardiya/ata", methods=["GET", "POST"])
def vardiya_ata():
    personeller = Personel.query.all()
    if request.method == "POST":
        personel_id = request.form["personel_id"]
        tarih_str = request.form["tarih"]
        tarih = datetime.strptime(tarih_str, "%Y-%m-%d").date()  # DÜZENLENDİ
        vardiya = request.form["vardiya"]
        baslangic, bitis = vardiya.split("-")

        yeni_vardiya = Vardiya(
            personel_id=personel_id,
            tarih=tarih,
            baslangic=baslangic,
            bitis=bitis
        )
        db.session.add(yeni_vardiya)
        db.session.commit()
        flash("Vardiya başarıyla atandı.", "success")
        return redirect(url_for("vardiya_listesi"))

    return render_template("vardiya_ata.html", personeller=personeller)


@app.route('/personel/sil/<int:id>', methods=['POST'])
@login_required
def personel_sil(id):
    personel = Personel.query.get_or_404(id)
    db.session.delete(personel)
    db.session.commit()
    flash('Personel başarıyla silindi!', 'success')
    return redirect(url_for('personel_listesi'))

@app.route('/json_dosya_olustur')
@login_required
def json_dosya_olustur():
    kullanicilar = User.query.all()

    veri = []
    for user in kullanicilar:
        kayitlar = GirisKaydi.query.filter_by(user_id=user.id).all()
        veri.append({
            'user': user.to_dict(),
            'giris_kayitlari': [k.to_dict() for k in kayitlar]
        })

    dosya_adi = 'kullanici_giris_kayitlari.json'
    with open(dosya_adi, 'w', encoding='utf-8') as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)

    return f"JSON dosyası oluşturuldu: {dosya_adi}"


@app.route('/')
def base():
    return render_template('index.html')

@app.route('/index')
def index():
    return redirect(url_for('base'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(name=name).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            giris_kaydi = GirisKaydi(tarih_saat=datetime.now(), user_id=user.id)
            db.session.add(giris_kaydi)
            db.session.commit()
            flash('Giriş başarılı!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Giriş başarısız. Lütfen kullanıcı adı ve şifreyi kontrol edin.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('username')

        if User.query.filter_by(email=email).first():
            flash('Bu e-posta zaten kayıtlı!', 'danger')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Kayıt başarılı! Giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.name)

@app.route('/logout')
@login_required
def logout():
    # En son giriş yapan kaydı bul ve çıkış saatini güncelle
    son_kayit = GirisKaydi.query.filter_by(user_id=current_user.id).order_by(GirisKaydi.tarih_saat.desc()).first()
    if son_kayit and not son_kayit.cikis_saat:
        son_kayit.cikis_saat = datetime.now()
        db.session.commit()

    logout_user()
    return redirect(url_for('base'))

@app.route('/personel/listesi')
@login_required
def personel_listesi():
    personeller = Personel.query.all()
    return render_template('personel_listesi.html', personeller=personeller)

@app.route('/personel/ekle', methods=['GET', 'POST'])
@login_required
def personel_ekle():
    if request.method == 'POST':
        ad_soyad = request.form.get('ad_soyad')
        departman = request.form.get('departman')
        yeni_personel = Personel(ad_soyad=ad_soyad, departman=departman)
        db.session.add(yeni_personel)
        db.session.commit()
        flash('Personel başarıyla eklendi!', 'success')
        return redirect(url_for('personel_listesi'))
    return render_template('personel_ekle.html')

@app.route('/personel/duzenle/<int:id>', methods=['GET', 'POST'])
@login_required
def personel_duzenle(id):
    personel = Personel.query.get_or_404(id)
    if request.method == 'POST':
        personel.ad_soyad = request.form.get('ad_soyad')
        personel.departman = request.form.get('departman')
        db.session.commit()
        flash('Personel başarıyla güncellendi!', 'success')
        return redirect(url_for('personel_listesi'))
    return render_template('personel_duzenle.html', personel=personel)

@app.route('/giris/kayitlari')
@login_required
def giris_kayitlari():
    kayitlar = GirisKaydi.query.order_by(GirisKaydi.tarih_saat.desc()).all()
    giris_kayitlari = []

    for kayit in kayitlar:
        giris_kayitlari.append({
            'ad_soyad': kayit.user.name,
            'tarih': kayit.tarih_saat.strftime('%d %B %Y'),
            'giris_saati': kayit.tarih_saat.strftime('%H:%M:%S'),
            'cikis_saati': kayit.cikis_saat.strftime('%H:%M:%S') if kayit.cikis_saat else '---'
        })

    return render_template('giris_kayitlari.html', giris_kayitlari=giris_kayitlari)

import os
if__name__=="__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",5000)))


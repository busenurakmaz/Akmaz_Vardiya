from flask import Flask, render_template, request, redirect, url_for
import locale
from datetime import datetime

app = Flask(__name__)


locale.setlocale(locale.LC_TIME, 'turkish')

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == '1234':
            return redirect(url_for('dashboard')) 
        else:
            return render_template('login.html', error="Geçersiz kullanıcı adı veya şifre") 

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/personel/listesi')
def personel_listesi():
   
    return render_template('personel_listesi.html', personeller=[])

@app.route('/personel/ekle', methods=['GET', 'POST'])
def personel_ekle():
    return render_template('personel_ekle.html')

@app.route('/personel/duzenle/<int:id>', methods=['GET', 'POST'])
def personel_duzenle(id):
   
    return render_template('personel_duzenle.html', personel={"id": id, "ad_soyad": "", "departman": ""})

@app.route('/giris/kayitlari')
def giris_kayitlari():
    now = datetime.now().strftime('%d %B %Y, %H:%M:%S')
    return render_template('giris_kayitlari.html', giris_kayitlari=[], current_time=now)

if __name__ == '__main__':
    app.run(debug=True)

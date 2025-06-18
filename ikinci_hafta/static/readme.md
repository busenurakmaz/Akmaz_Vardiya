# Akmaz Yazılım Vardiya Sistemi - CSS Yapısı

Bu klasör, Flask web uygulamasının stil dosyalarını içerir. Tüm CSS dosyaları modern ve responsive tasarım prensiplerine göre oluşturulmuştur.

## Dosya Yapısı

```
static/
│
├── css/
│   ├── main.css            # Temel stiller ve global tanımlamalar
│   ├── auth.css            # Giriş/Kayıt sayfaları stilleri
│   ├── dashboard.css       # Ana panel stilleri
│   ├── personnel.css       # Personel yönetimi stilleri
│   ├── shifts.css          # Vardiya yönetimi stilleri
│   └── responsive.css      # Responsive düzenlemeler
│
└── images/                 # Tüm görsel asset'ler
```

## Temel Özellikler

### 1. Tema ve Renk Paleti
```css
:root {
  --primary-color: #c82333;      /* Ana kırmızı renk */
  --primary-dark: #a71d2a;       /* Koyu kırmızı */
  --primary-light: #ffebee;      /* Açık kırmızı */
  --background: #f8f9fa;         /* Arkaplan rengi */
  --card-bg: #ffffff;            /* Kart arkaplanları */
  --text-dark: #495057;          /* Koyu metin */
  --text-light: #6c757d;         /* Açık metin */
}
```

### 2. Responsive Grid Sistemi
```css
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 15px;
}

.row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -15px;
}

.col {
  flex: 1;
  padding: 0 15px;
}
```

### 3. Tipografi
```css
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: var(--text-dark);
}

h1, h2, h3 {
  color: var(--primary-color);
  margin-bottom: 1rem;
  font-weight: 600;
}

h1 { font-size: 2rem; }
h2 { font-size: 1.75rem; }
h3 { font-size: 1.5rem; }
```

## Bileşenler

### 1. Kart (Card) Yapısı
```css
.card {
  background: var(--card-bg);
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
  transition: transform 0.3s ease;
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}
```

### 2. Butonlar
```css
.btn {
  display: inline-block;
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 500;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: var(--primary-color);
  color: white;
  border: none;
}

.btn-primary:hover {
  background: var(--primary-dark);
  transform: translateY(-2px);
}
```

### 3. Form Elementleri
```css
.form-control {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  margin-bottom: 15px;
  transition: border 0.3s;
}

.form-control:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(200, 35, 51, 0.1);
}
```

## Kullanım Kılavuzu

1. **Yeni bir sayfa için CSS ekleme**:
   ```html
   {% block styles %}
   <link rel="stylesheet" href="{{ url_for('static', filename='css/yeni-sayfa.css') }}">
   {% endblock %}
   ```

2. **Tema renklerini kullanma**:
   ```css
   .element {
     color: var(--primary-color);
     background: var(--card-bg);
   }
   ```

3. **Responsive tasarım**:
   ```css
   @media (max-width: 768px) {
     .column {
       flex: 100%;
     }
   }
   ```

## Best Practices

1. **Global stiller** için `main.css` dosyasını kullanın
2. **Sayfa özel stilleri** için yeni CSS dosyaları oluşturun
3. **Bileşen tabanlı** yaklaşım kullanın
4. **CSS değişkenleri** ile tutarlı bir tema sağlayın
5. **Mobile-first** yaklaşımını benimseyin

## Geliştirme Notları

1. CSS dosyalarını minify edin (production için)
2. Kullanılmayan CSS'leri temizleyin
3. Class isimlendirmelerinde BEM metodolojisini kullanın
4. Büyük projelerde CSS preprocessor (SASS/LESS) kullanmayı düşünün

## Katkıda Bulunma

1. Yeni bileşenler eklerken mevcut tema ile uyumlu olmasına dikkat edin
2. CSS değişikliklerini açıklayan PR'lar oluşturun
3. Responsive testleri unutmayın

## Lisans

Proje MIT lisansı altında dağıtılmaktadır.

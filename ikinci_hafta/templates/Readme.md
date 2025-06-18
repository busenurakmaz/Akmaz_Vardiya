
# Akmaz Yazılım Vardiya Sistemi - Templates

Bu klasör, Flask web uygulamasının şablon (template) dosyalarını içerir. HTML şablonları Jinja2 template engine kullanılarak oluşturulmuştur.

## Şablon Yapısı

```
templates/
│
├── base.html          # Ana şablon, tüm sayfalar buradan extend edilir
├── dashboard.html     # Ana sayfa/panel
├── login.html         # Giriş sayfası
├── register.html      # Kayıt sayfası
├── personel_listesi.html  # Personel listesi
├── personel_ekle.html     # Yeni personel ekleme
├── giris_kayitlari.html   # Giriş kayıtları
├── vardiya_ata.html       # Vardiya atama
└── vardiya_listesi.html   # Vardiya listesi
```

## Temel Kullanım

### base.html
Tüm sayfaların temelini oluşturan ana şablon. İçerir:
- Site başlığı ve meta tag'ler
- Navigasyon menüsü
- Dinamik title yönetimi (`{% block title %}`)
- İçerik alanı (`{% block content %}`)

Örnek kullanım:
```html
{% extends "base.html" %}

{% block title %}Sayfa Başlığı{% endblock %}

{% block content %}
<!-- Sayfa içeriği buraya -->
{% endblock %}
```

## Özellikler

1. **Template Inheritance**:
   - Tüm sayfalar `base.html`'den extend edilir
   - Ortak elemanlar tek bir yerde yönetilir

2. **Dinamik İçerik**:
   - Kullanıcı giriş durumuna göre menü değişimi
   - Flask'tan gelen verilerin gösterimi

3. **Tutarlı Tasarım**:
   - Tüm sayfalarda kırmızı-beyaz tema
   - Responsive tasarım

4. **Bloklar**:
   - `title`: Sayfa başlığı için
   - `content`: Ana içerik için

## CSS Entegrasyonu

Her sayfa kendi özel CSS'ini şu şekilde yükler:
```html
{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', filename='sayfa_adi.css') }}">
{% endblock %}
```

## Geliştirme Notları

1. Yeni bir sayfa eklerken mutlaka `base.html`'den extend edin
2. Sayfa başlıklarını `{% block title %}` içinde belirtin
3. Tasarım bütünlüğü için mevcut CSS yapısını koruyun
4. Mobil uyumluluğu test edin

## Katkıda Bulunma

1. Yeni özellikler için ayrı template dosyaları oluşturun
2. CSS değişikliklerini ilgili static dosyalarda yapın
3. Büyük değişiklikler öncesinde issue açın

## Lisans

Proje MIT lisansı altında dağıtılmaktadır.

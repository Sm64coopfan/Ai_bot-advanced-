# Ai_bot-advanced-
this is an advanced bot

markdown# 3D Baskı Hata Algılama Sistemi (3D Printing Fail Detection)

Bu proje, Teachable Machine veya benzeri platformlar kullanılarak eğitilmiş bir derin öğrenme (Keras/TensorFlow) modelini kullanarak 3D yazıcı baskı süreçlerini analiz eder. Görüntü işleme teknikleriyle baskıdaki hataları (spaghetti, katman kayması, tabandan ayrılma vb.) gerçek zamanlıya yakın tespit etmeyi amaçlar.

## 🚀 Özellikler

* **Teachable Machine Uyumluluğu:** Google Teachable Machine çıktısı olan `.h5` model formatını doğrudan destekler.
* **Görüntü Ön İşleme:** Görüntüleri otomatik olarak modelin istediği boyuta (224x224) getirir ve normalize eder.
* **Akıllı Hata Filtreleme:** Anahtar kelime taraması (`hata`, `fail`, `spaghetti`, `bozuk`, `ayrılma`, `kayma`, `tıkanma`) yardımıyla baskı durumunu otomatik sınıflandırır.
* **Güven Eşiği (Confidence Threshold):** Yanlış alarmları önlemek için %70 güven oranının altındaki tahminleri "kararsız" olarak işaretler.

## 🛠️ Gereksinimler

Projenin çalışması için aşağıdaki Python kütüphanelerinin yüklü olması gerekir:

```bash
pip install opencv-python numpy pillow tensorflow
```

> **Not:** TensorFlow kurulumu sisteminize ve Python sürümünüze göre değişiklik gösterebilir. Python 3.9+ sürümleri için uyumluluğu kontrol ediniz.

## 📂 Dosya Yapısı

Proje dizininizin aşağıdaki yapıda olması beklenmektedir:

```text
├── keras_model.h5      # Eğitilmiş Keras model dosyası
├── labels.txt          # Sınıf etiketlerinin bulunduğu dosya (örn: "0 Başarılı", "1 Spaghetti")
├── main.py             # Analiz kodunun bulunduğu Python dosyası
└── baski_test.jpg      # Analiz edilmek istenen örnek test görseli
```

## 💻 Kullanım

Sınıflandırma fonksiyonunu projenize dahil edip model, etiket ve görsel yollarını parametre olarak göndererek çalıştırabilirsiniz:

```python
from main import get_class

# Fonksiyonu çağırma
class_name, confidence = get_class(
    model_path="keras_model.h5",
    labels_path="labels.txt",
    image_path="baski_test.jpg"
)
```

### Örnek Çıktı

Model görseli başarıyla analiz ettiğinde terminalde aşağıdaki gibi bir çıktı üretir:

```text
========================================
     3D BASKI ANALİZ SONUCU
========================================
Tahmin Edilen Durum : Spaghetti
Güven Oranı         : %92.45
Durum Tespiti       : ❌ Baskıda hata algılandı!
========================================
```

## 🛠️ Geliştirme ve Katkıda Bulunma



import cv2
import numpy as np
from PIL import Image, ImageOps
from tensorflow.keras.models import load_model

def get_class(model_path , labels_path , image_path):

    # 1. Modeli ve Etiketleri Yükleyin
    model = load_model("keras_model.h5", compile=False)
    with open("labels.txt", "r", encoding="utf-8") as f:
        class_names = [line.strip() for line in f.readlines()]

    # 2. Analiz Edilecek Fotoğrafın Yolunu Girin
    image_path = "baski_test.jpg"  # <--- Kontrol etmek istediğiniz resmin adını yazın

    try:
        # Resmi yükleyin ve RGB formatına dönüştürün
        image = Image.open(image_path).convert("RGB")
    except FileNotFoundError:
        print(f"Hata: '{image_path}' dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")
        exit()

    # 3. Resmi Model Boyutuna Getirin (224x224)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # Resmi numpy dizisine çevirin ve normalize edin
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Model için veri dizisini hazırlayın (1, 224, 224, 3)
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array

    # 4. Model Tahmini
    prediction = model.predict(data, verbose=0)
    index = np.argmax(prediction)
    class_name = class_names[index][2:]  # Etiketin başındaki "0 " veya "1 " kısmını temizler
    confidence_score = float(prediction[0][index])

    # 5. Sonuçları Değerlendirme ve Ekrana Yazdırma
    print("\n" + "="*40)
    print("     3D BASKI ANALİZ SONUCU")
    print("="*40)
    print(f"Tahmin Edilen Durum : {class_name}")
    print(f"Güven Oranı         : %{confidence_score * 100:.2f}")

    # Güven eşiği kontrolü (%70)
    if confidence_score > 0.70:
        # Etikette hata belirten anahtar kelimeler aranır
        hata_kelimeleri = ["hata", "fail", "spaghetti", "bozuk", "ayrılma", "kayma","tıkanma"]
        if any(kelime in class_name.lower() for kelime in hata_kelimeleri):
            print("\n🚨 UYARI: Baskıda kritik bir hata tespit edildi!")
            # TODO: Buraya bir API tetikleyicisi veya mail/Telegram bildirim kodu eklenebilir.
        else:
            print("\n✅ Durum Normal: Baskı sorunsuz ilerliyor.")
    else:
        print("\n⚠️ Not: Yapay zeka sonuçtan tam emin olamadı (Güven oranı düşük).")
    print("="*40)

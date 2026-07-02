import os
import discord
from discord.ext import commands
# Yapay zeka fonksiyonumuzu import ediyoruz (Aynı klasörde olduklarını varsayıyoruz)
from main import get_class  

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='.', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot başarıyla başlatıldı: {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def selamın_aleyküm(ctx):
    await ctx.send(f'Aleyküm Selam {ctx.author.mention}!')

@bot.command()
async def heh(ctx, count_heh: int = 5): # Veri tipini int olarak belirlemek hatayı önler
    await ctx.send("he" * count_heh)

@bot.command()
async def check(ctx):
    # DÜZELTME: attachmend değil attachments olmalı
    if ctx.message.attachments:
        for attachment in ctx.message.attachment:
            file_name = attachment.filename
            
            # Sadece resim dosyalarını kabul etmek için kontrol
            if any(file_name.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
                await ctx.send('🔄 Resim indiriliyor ve analiz ediliyor, lütfen bekleyin...')
                
                # Resmi yerel dizine kaydet
                await attachment.save(f'./{file_name}')
                
                # Yapay zeka modelini çalıştır (Dosya yollarını kendinize göre güncelleyin)
                class_name, confidence_score = get_class(
                    model_path="keras_model.h5",
                    labels_path="labels.txt",
                    image_path=f'./{file_name}'
                )
                
                # Model sonucuna göre Discord'a mesaj gönder
                if class_name:
                    sonuc_mesaji = (
                        f"📊 **3D BASKI ANALİZ SONUCU** 📊\n"
                        f"**Tahmin Edilen Durum:** {class_name}\n"
                        f"**Güven Oranı:** %{confidence_score * 100:.2f}\n"
                    )
                    
                    if confidence_score > 0.70:
                        hata_kelimeleri = ["hata", "fail", "spaghetti", "bozuk", "ayrılma", "kayma", "tıkanma"]
                        if any(kelime in class_name.lower() for kelime in hata_kelimeleri):
                            sonuc_mesaji += "🚨 **Durum Tespiti:** Baskıda hata algılandı!"
                        else:
                            sonuc_mesaji += "✅ **Durum Tespiti:** Baskı sorunsuz ilerliyor."
                    else:
                        sonuc_mesaji += "⚠️ **Durum Tespiti:** Düşük güven oranı! Net bir karar verilemedi."
                        
                    await ctx.send(sonuc_mesaji)
                else:
                    await ctx.send("❌ Yapay zeka analizi sırasında bir hata oluştu.")
                
                # Analiz bittikten sonra yerel diski temizlemek için resmi siliyoruz
                if os.path.exists(f'./{file_name}'):
                    os.remove(f'./{file_name}')
            else:
                await ctx.send('❌ Lütfen sadece geçerli bir resim dosyası (.jpg, .png vb.) yükleyin.')
    else:
        await ctx.send('⚠️ Fotoğraf eklemeyi unuttunuz! Komutu kullanırken bir resim yükleyin.')       

# Discord Bot Tokeninizi buraya girin

bot.run("TOKEN_İS_HERE")

# Insider Onsite Experiment Pop-up Test Senaryoları

## Test Senaryoları Tablosu 
| Test ID | Test Kategorisi | Test Başlığı | Ön Koşullar | Test Adımları | Beklenen Sonuç | Öncelik | Test Tipi |
|---------|----------------|--------------|-------------|---------------|----------------|---------|-----------|
| TC001 | Pozitif | Pop-up Görüntüleme Testi | Tarayıcı açık, test URL'si yüklü | 1. Test panelinde "SHOW INSTANTLY" butonuna tıkla | Pop-up başarıyla görüntülenir, İngilizce içerik doğru görünür | Yüksek | Fonksiyonel |
| TC002 | Pozitif | Pop-up X Butonu ile Kapatma | Pop-up görüntüleniyor | 1. Pop-up sağ üst köşesindeki X butonuna tıkla | Pop-up kapanır, ana sayfa görünür | Yüksek | Fonksiyonel |
| TC003 | Pozitif | Pop-up Dışına Tıklayarak Kapatma | Pop-up görüntüleniyor | 1. Pop-up dışındaki herhangi bir alana tıkla | Pop-up kapanır, ana sayfa görünür | Yüksek | Fonksiyonel |
| TC004 | Pozitif | Pop-up İçerik Doğrulama | Pop-up görüntüleniyor | 1. Pop-up içeriğini kontrol et | Pop-up İngilizce içeriği doğru şekilde görüntülenir | Orta | Fonksiyonel |
| TC005 | Pozitif | Pop-up Tekrar Görüntüleme | Pop-up kapatıldı | 1. "SHOW INSTANTLY" butonuna tekrar tıkla | Pop-up tekrar başarıyla görüntülenir | Orta | Fonksiyonel |
| TC006 | Pozitif | Test Panel Durum Göstergesi | Test paneli açık | 1. Pop-up durumunu kontrol et | "Visible" veya "Not Visible" durumu doğru gösterilir | Orta | Fonksiyonel |
| TC007 | Negatif | Çoklu Pop-up Açma Testi | Pop-up zaten açık | 1. "SHOW INSTANTLY" butonuna tekrar tıkla | Yeni pop-up açılmaz, mevcut pop-up korunur | Orta | Negatif |
| TC008 | Negatif | Pop-up Kapatma Sonrası Durum | Pop-up kapatıldı | 1. Pop-up elementlerinin varlığını kontrol et | Pop-up elementleri DOM'da görünmez durumda | Orta | Negatif |
| TC009 | Negatif | Pop-up'ın Sadece Ürün Sayfalarında Doğal Olarak Tetiklenmesi | Tarayıcı açık | 1. Ana Sayfa'ya git ve bekle<br>2. Kategori Sayfası'na git ve bekle<br>3. Alışveriş Sepeti'ne git ve bekle | Pop-up bu sayfaların hiçbirinde kendi kendine görünmemelidir | Yüksek | Fonksiyonel |
| TC010 | Pozitif | Pop-up İçeriğinin Sayfadaki Ürünle Eşleşmesi | Ürün detay sayfası | 1. "Mug" ürününün detay sayfasına git<br>2. Pop-up göründüğünde ürün adını kontrol et | Pop-up'ın içindeki ürün adı, sayfa başlığındaki "Mug" ürün adıyla aynı olmalıdır | Yüksek | Fonksiyonel |
| TC011 | Edge Case | Hızlı Açma-Kapatma Testi | Test paneli açık | 1. "SHOW INSTANTLY" butonuna tıkla<br>2. Hemen X butonuna tıkla | Pop-up açılır ve hemen kapanır, hata oluşmaz | Düşük | Edge Case |
| TC012 | Edge Case | Sayfa Yenileme Sonrası Durum | Pop-up açık | 1. Sayfayı yenile (F5) | Pop-up kapanır, sayfa normal duruma döner | Düşük | Edge Case |
| TC013 | UI/UX | Pop-up Görsel Tasarım Testi | Pop-up görüntüleniyor | 1. Pop-up tasarımını kontrol et | Pop-up merkezi konumda, uygun boyutta görüntülenir | Orta | UI/UX |
| TC014 | UI/UX | Pop-up Overlay Testi | Pop-up görüntüleniyor | 1. Arka plan overlay'ini kontrol et | Arka plan karartılır, pop-up ön planda görünür | Orta | UI/UX |
| TC015 | Performans | Pop-up Açılma Süresi | Test paneli açık | 1. "SHOW INSTANTLY" butonuna tıkla<br>2. Açılma süresini ölç | Pop-up 1 saniye içinde açılır | Düşük | Performans |
| TC016 | Performans | Pop-up Kapanma Süresi | Pop-up açık | 1. X butonuna tıkla<br>2. Kapanma süresini ölç | Pop-up 0.5 saniye içinde kapanır | Düşük | Performans |
| TC017 | Tarayıcı Uyumluluğu | Chrome Tarayıcı Testi | Chrome tarayıcısı | 1. Tüm pop-up fonksiyonlarını test et | Tüm özellikler Chrome'da çalışır | Yüksek | Uyumluluk |
| TC018 | Tarayıcı Uyumluluğu | Firefox Tarayıcı Testi | Firefox tarayıcısı | 1. Tüm pop-up fonksiyonlarını test et | Tüm özellikler Firefox'ta çalışır | Yüksek | Uyumluluk |
| TC019 | Tarayıcı Uyumluluğu | Safari Tarayıcı Testi | Safari tarayıcısı | 1. Tüm pop-up fonksiyonlarını test et | Tüm özellikler Safari'de çalışır | Yüksek | Uyumluluk |
| TC020 | Responsive | Mobil Görünüm Testi | Mobil cihaz/emülatör | 1. Pop-up'ı mobil görünümde test et | Pop-up mobil ekranda uygun şekilde görüntülenir | Orta | Responsive |
| TC021 | Responsive | Tablet Görünüm Testi | Tablet cihaz/emülatör | 1. Pop-up'ı tablet görünümde test et | Pop-up tablet ekranda uygun şekilde görüntülenir | Orta | Responsive |
| TC022 | Erişilebilirlik | Klavye Navigasyon Testi | Pop-up açık | 1. Tab tuşu ile navigasyon yap<br>2. Enter ile kapatmayı dene | Klavye ile pop-up kapatılabilir | Düşük | Erişilebilirlik |

## Test Senaryoları Özeti

**Toplam Test Sayısı:** 22
- **Pozitif Testler:** 7
- **Negatif Testler:** 3
- **Edge Case Testler:** 2
- **UI/UX Testler:** 2
- **Performans Testler:** 2
- **Tarayıcı Uyumluluk Testler:** 3
- **Responsive Testler:** 2
- **Erişilebilirlik Testler:** 1

**Öncelik Dağılımı:**
- **Yüksek Öncelik:** 9 test
- **Orta Öncelik:** 10 test
- **Düşük Öncelik:** 3 test

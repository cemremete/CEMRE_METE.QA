# Bug Raporu Şablonu - Insider Onsite Experiment Pop-up

## Bug Raporu Tablosu 

| Bug ID | Başlık | Açıklama | Tekrarlama Adımları | Beklenen Sonuç | Gerçek Sonuç | Önem Derecesi | Öncelik | Test Ortamı | Tarayıcı | OS | Bulunan Tarih | Durumu | Atanan Kişi | Ekran Görüntüsü |
|--------|--------|----------|-------------------|----------------|---------------|---------------|---------|-------------|----------|----|-----------|---------|-----------|--------------| 
| BUG001 | Production Blocker - URL Parameter Dependency | System only works with specific URL parameters, making it inaccessible in normal conditions | 1. Navigate to base URL without parameters<br>2. Try to trigger pop-up<br>3. Observe system behavior | Pop-up should work on all product pages | Pop-up completely non-functional without specific URL parameters | Critical | P1 | Test | Chrome 120 | Windows 11 | 30.08.2025 | Open | Dev Team | screenshot_bug001.png |
| BUG002 | Add to Cart Button Not Working | Add to Cart functionality in pop-up is completely broken | 1. Navigate to test URL<br>2. Trigger pop-up<br>3. Click "Add to Cart" button<br>4. Check cart status | Product should be added to cart | Add to Cart button non-responsive, no cart update | Critical | P1 | Test | Chrome 120 | Windows 11 | 30.08.2025 | Open | Dev Team | screenshot_bug002.png |
| BUG003 | Price Update Error - Discounts Not Reflecting | Product prices and discounts are not displaying correctly in pop-up | 1. Navigate to product with discount<br>2. Trigger pop-up<br>3. Compare prices with product page | Pop-up should show correct prices and discounts | Incorrect pricing, discounts not applied | Critical | P1 | Test | Chrome 120 | Windows 11 | 30.08.2025 | Open | Dev Team | screenshot_bug003.png |
| BUG004 | Mobile/Tablet 0% Functionality | Pop-up completely non-functional on mobile and tablet devices | 1. Open site on mobile device<br>2. Try to trigger pop-up<br>3. Test all functionality | Pop-up should work on all devices | 0% functionality on mobile/tablet | Critical | P1 | Test | Mobile Safari | iOS 17 | 30.08.2025 | Open | Dev Team | screenshot_bug004.png |
| BUG005 | Firefox/Safari Complete Failure | Pop-up system completely fails on Firefox and Safari browsers | 1. Open site in Firefox/Safari<br>2. Try to trigger pop-up<br>3. Test functionality | Pop-up should work across all browsers | Complete failure in Firefox and Safari | Critical | P1 | Test | Firefox 119 | Windows 11 | 30.08.2025 | Open | Dev Team | screenshot_bug005.png |
| BUG006 | Performance Critical - 4.49s Load Delay | Pop-up takes 4.49 seconds to load, exceeding 2-second standard | 1. Trigger pop-up<br>2. Measure load time<br>3. Compare with performance standards | Pop-up should load within 2 seconds | 4.49 second delay detected | High | P2 | Test | Chrome 120 | Windows 11 | 30.08.2025 | Open | Dev Team | performance_bug006.png |
| BUG007 | Content Critical - 90% Incorrect Product Mapping | Pop-up shows wrong products 90% of the time | 1. Navigate to specific product page<br>2. Trigger pop-up<br>3. Compare product in pop-up vs page | Pop-up should show same product as page | 90% incorrect product mapping | Critical | P1 | Test | Chrome 120 | Windows 11 | 30.08.2025 | Open | Dev Team | screenshot_bug007.png |
| BUG008 | UX Critical - Pop-up Close Buttons Not Working | Pop-up close buttons (X and outside click) are non-functional | 1. Trigger pop-up<br>2. Try clicking X button<br>3. Try clicking outside pop-up | Pop-up should close with both methods | Close buttons completely non-functional | High | P2 | Test | Chrome 120 | Windows 11 | 30.08.2025 | Open | Dev Team | screenshot_bug008.png |
| BUG009 | Memory Critical - Memory Leak Detected | System shows memory leak after multiple pop-up interactions | 1. Open/close pop-up 50 times<br>2. Monitor memory usage<br>3. Check for memory increase | Memory should remain stable | Significant memory leak detected | High | P2 | Test | Chrome 120 | Windows 11 | 30.08.2025 | Open | Dev Team | memory_bug009.png |
| BUG010 | Overlay Critical - Background Overlay Missing | Pop-up lacks proper background overlay for proper UX | 1. Trigger pop-up<br>2. Check background overlay<br>3. Verify visual design | Background should be darkened with overlay | No background overlay present | High | P2 | Test | Chrome 120 | Windows 11 | 30.08.2025 | Open | Dev Team | screenshot_bug010.png |

## Bug Raporu Alanları Açıklaması

### Bug ID
- **Format:** BUG + 3 haneli numara (BUG001, BUG002, vb.)
- **Amaç:** Her bug için benzersiz tanımlayıcı

### Başlık
- **Format:** Kısa ve açıklayıcı başlık (maksimum 100 karakter)
- **Örnek:** "Pop-up X butonu çalışmıyor", "Pop-up yanlış konumda görüntüleniyor"

### Açıklama
- **İçerik:** Bug'ın detaylı açıklaması
- **Dahil edilmesi gerekenler:** Ne olduğu, hangi koşullarda oluştuğu

### Tekrarlama Adımları
- **Format:** Numaralı liste halinde
- **İçerik:** Bug'ı tekrarlamak için gereken tüm adımlar
- **Detay seviyesi:** Başka bir kişinin aynı hatayı tekrarlayabilecek kadar detaylı

### Beklenen Sonuç
- **İçerik:** Sistemin nasıl davranması gerektiği
- **Referans:** Gereksinimler veya tasarım dokümanları

### Gerçek Sonuç
- **İçerik:** Sistemin gerçekte nasıl davrandığı
- **Detay:** Hata mesajları, yanlış davranışlar

### Önem Derecesi (Severity)
- **Critical:** Sistem çalışmıyor, ana fonksiyon kullanılamıyor
- **High:** Önemli fonksiyon çalışmıyor, workaround yok
- **Medium:** Fonksiyon çalışmıyor ama workaround var
- **Low:** Kozmetik hatalar, küçük UI sorunları

### Öncelik (Priority)
- **P1:** Hemen düzeltilmeli (24 saat içinde)
- **P2:** Bir sonraki release'de düzeltilmeli
- **P3:** Gelecek release'lerde düzeltilebilir
- **P4:** Düzeltilmesi zorunlu değil

### Test Ortamı
- **Değerler:** Development, Test, Staging, Production
- **Amaç:** Bug'ın hangi ortamda bulunduğunu belirtir

### Tarayıcı
- **Format:** Tarayıcı adı + versiyon numarası
- **Örnekler:** Chrome 120, Firefox 119, Safari 17, Edge 119

### OS (İşletim Sistemi)
- **Format:** OS adı + versiyon
- **Örnekler:** Windows 11, macOS 14, Ubuntu 22.04, iOS 17, Android 14

### Bulunan Tarih
- **Format:** DD.MM.YYYY
- **Amaç:** Bug'ın ne zaman keşfedildiğini takip etmek

### Durumu (Status)
- **Open:** Yeni açılan bug
- **In Progress:** Üzerinde çalışılıyor
- **Fixed:** Düzeltildi, test bekliyor
- **Verified:** Test edildi, düzeltme onaylandı
- **Closed:** Kapatıldı
- **Rejected:** Geçerli bug değil
- **Duplicate:** Başka bir bug'ın kopyası

### Atanan Kişi
- **İçerik:** Bug'ı düzeltmekle sorumlu kişi/takım
- **Format:** İsim veya takım adı

### Ekran Görüntüsü
- **Format:** Dosya adı (screenshot_001.png, video_001.mp4)
- **İçerik:** Bug'ı gösteren görsel kanıt
- **Konum:** screenshots/ klasörü altında saklanmalı

## Örnek Bug Raporları

### Örnek 1: Kritik Bug
| Bug ID | Başlık | Açıklama | Tekrarlama Adımları | Beklenen Sonuç | Gerçek Sonuç | Önem Derecesi | Öncelik |
|--------|--------|----------|-------------------|----------------|---------------|---------------|---------|
| BUG002 | Pop-up hiç görüntülenmiyor | SHOW INSTANTLY butonuna tıklandığında pop-up açılmıyor | 1. Test URL'sine git<br>2. SHOW INSTANTLY butonuna tıkla<br>3. Sayfayı kontrol et | Pop-up görüntülenmeli | Hiçbir şey olmuyor | Critical | P1 |

### Örnek 2: UI Bug
| Bug ID | Başlık | Açıklama | Tekrarlama Adımları | Beklenen Sonuç | Gerçek Sonuç | Önem Derecesi | Öncelik |
|--------|--------|----------|-------------------|----------------|---------------|---------------|---------|
| BUG003 | Pop-up metni yanlış hizalanmış | Pop-up içindeki "Turkish" metni merkezi değil | 1. Pop-up'ı aç<br>2. Metin hizalamasını kontrol et | Metin ortalanmış olmalı | Metin sola hizalanmış | Low | P3 |

## Bug Raporu Süreci

1. **Bug Keşfi:** Test sırasında bug bulunur
2. **Doğrulama:** Bug tekrarlanabilir mi kontrol edilir
3. **Raporlama:** Bu şablon kullanılarak bug raporu oluşturulur
4. **Önceliklendirme:** Önem derecesi ve öncelik belirlenir
5. **Atama:** Sorumlu kişi/takım atanır
6. **Düzeltme:** Bug düzeltilir
7. **Test:** Düzeltme test edilir
8. **Kapatma:** Bug kapatılır

## Notlar

- Her bug için mutlaka ekran görüntüsü alınmalıdır
- Tekrarlama adımları başka bir kişi tarafından takip edilebilecek kadar detaylı olmalıdır
- Bug raporları düzenli olarak gözden geçirilmeli ve güncellenmelidir
- Benzer bug'lar için duplicate kontrolü yapılmalıdır

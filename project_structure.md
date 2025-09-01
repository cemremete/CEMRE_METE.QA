# Insider Test Automation Project - POM Dizin Yapısı

## Proje Dizin Yapısı

```
insider_test_automation/
│
├── pages/                          # Page Object Model sınıfları
│   ├── __init__.py
│   ├── base_page.py                # Temel sayfa sınıfı
│   ├── popup_page.py               # Pop-up sayfası sınıfı
│   └── product_page.py             # Ürün sayfası sınıfı
│
├── tests/                          # Test dosyaları
│   ├── __init__.py
│   ├── conftest.py                 # Pytest konfigürasyonu ve fixtures
│   ├── test_popup_functionality.py # Pop-up fonksiyonalite testleri
│   ├── test_popup_ui.py            # Pop-up UI testleri
│   └── test_popup_negative.py      # Pop-up negatif testleri
│
├── utils/                          # Yardımcı fonksiyonlar
│   ├── __init__.py
│   ├── driver_manager.py           # WebDriver yönetimi
│   ├── screenshot_helper.py        # Ekran görüntüsü yardımcıları
│   └── test_data.py                # Test verileri
│
├── reports/                        # Test raporları
│   ├── html/                       # HTML raporları
│   └── json/                       # JSON raporları
│
├── screenshots/                    # Ekran görüntüleri
│   ├── passed/                     # Başarılı testler
│   └── failed/                     # Başarısız testler
│
├── config/                         # Konfigürasyon dosyaları
│   ├── __init__.py
│   ├── settings.py                 # Genel ayarlar
│   └── locators.py                 # Element locator'ları
│
├── requirements.txt                # Python bağımlılıkları
├── pytest.ini                     # Pytest konfigürasyonu
├── .gitignore                      # Git ignore dosyası
├── README.md                       # Proje dokümantasyonu
└── run_tests.py                    # Test çalıştırma scripti
```

## Dizin Açıklamaları

### 📁 pages/
Page Object Model desenine uygun sayfa sınıflarını içerir:
- **base_page.py:** Tüm sayfa sınıflarının miras aldığı temel sınıf
- **popup_page.py:** Pop-up ile ilgili tüm elementler ve metodlar
- **product_page.py:** Ürün sayfası elementleri ve metodları

### 📁 tests/
Test dosyalarını kategorilere göre organize eder:
- **conftest.py:** Pytest fixtures, setup/teardown metodları
- **test_popup_functionality.py:** Temel fonksiyonalite testleri (TC001-TC010)
- **test_popup_ui.py:** UI/UX ve responsive testler (TC013-TC021)
- **test_popup_negative.py:** Negatif ve edge case testler (TC007-TC012)

### 📁 utils/
Yardımcı fonksiyonlar ve araçlar:
- **driver_manager.py:** WebDriver başlatma, kapatma, konfigürasyon
- **screenshot_helper.py:** Otomatik ekran görüntüsü alma
- **test_data.py:** Test verilerini merkezi olarak yönetme

### 📁 reports/
Test sonuçları ve raporlar:
- **html/:** Pytest-html ile oluşturulan HTML raporları
- **json/:** JSON formatında test sonuçları

### 📁 screenshots/
Ekran görüntüleri organizasyonu:
- **passed/:** Başarılı testlerin ekran görüntüleri
- **failed/:** Başarısız testlerin ekran görüntüleri (otomatik)

### 📁 config/
Konfigürasyon ve ayar dosyaları:
- **settings.py:** URL'ler, timeout değerleri, tarayıcı ayarları
- **locators.py:** Tüm element locator'larını merkezi yönetim

## POM Tasarım Deseni Avantajları

1. **Kod Tekrarını Önler:** Element locator'ları tek yerde tanımlanır
2. **Bakım Kolaylığı:** UI değişikliklerinde sadece ilgili page class güncellenir
3. **Okunabilirlik:** Test kodları daha anlaşılır ve temiz olur
4. **Yeniden Kullanılabilirlik:** Page metodları farklı testlerde kullanılabilir
5. **Ölçeklenebilirlik:** Yeni sayfalar kolayca eklenebilir

## Dosya Adlandırma Kuralları

- **Sınıf dosyaları:** snake_case (popup_page.py)
- **Test dosyaları:** test_ prefix ile başlar (test_popup_functionality.py)
- **Sınıf isimleri:** PascalCase (PopupPage)
- **Metod isimleri:** snake_case (click_close_button)
- **Sabit değişkenler:** UPPER_CASE (BASE_URL)

## Proje Kurulum Sırası

1. Ana dizin oluşturma
2. Alt dizinleri oluşturma
3. __init__.py dosyalarını ekleme
4. requirements.txt oluşturma
5. Temel konfigürasyon dosyalarını oluşturma
6. Base page sınıfını oluşturma
7. Specific page sınıflarını oluşturma
8. Test dosyalarını oluşturma
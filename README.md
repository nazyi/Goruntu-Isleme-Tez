# NADA Drone Sistemleri

"Gökyüzündeki gözünüz"

Drone ile çekilen video ve fotoğrafları işleyip nesne tespiti yapan bir web uygulaması. Bitirme projem kapsamında Django ile geliştirdim.

<img width="1885" height="926" alt="Ekran görüntüsü 2025-01-13 203514" src="https://github.com/user-attachments/assets/3fe732ac-a956-45d5-bdc9-031eeedf2048" />


## Ne İşe Yarıyor

- Drone videolarını yükleyip YOLO ile üzerinde nesne tespiti yapıyor (insan, araç vb.)
- Güzergahları harita üzerinde gösteriyor
- Dronelara ait bilgileri (kamera tipi, uçuş menzili vb.) kaydedebiliyorsun
- Canlı nesne takibi yapabiliyorsun

## Kullanılan Teknolojiler

- Python / Django
- OpenCV + YOLOv3
- Leaflet (harita için)
- HTML / CSS

## Kurulum

```
git clone https://github.com/nazyi/Goruntu-Isleme-Tez.git
cd Goruntu-Isleme-Tez
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

YOLOv3'ün ağırlık dosyası (`yolov3.weights`) boyutu yüzünden repoya eklenmedi. Resmi kaynaktan indirip şu klasöre atman lazım:
```
goruntu_isleme/static/yolov3.weights
```

Sonra:
```
python manage.py runserver
```

## Not

Bitirme projesi olarak geliştirildi, hâlâ üzerinde çalışıyorum.


<div align="center">
# NADA Drone Sistemleri
 
**"Gökyüzündeki gözünüz"**
 
Drone ile çekilen video ve fotoğrafları işleyip YOLO ile nesne tespiti yapan, güzergah planlayan ve drone filosunu yöneten bir Django web uygulaması.
 
[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white)](https://opencv.org/)
[![YOLOv3](https://img.shields.io/badge/YOLOv3-Object%20Detection-yellow?style=flat-square)]()
[![Leaflet](https://img.shields.io/badge/Leaflet-199900?style=flat-square&logo=leaflet&logoColor=white)](https://leafletjs.com/)

<img width="1885" height="926" alt="Ekran görüntüsü 2025-01-13 203514" src="https://github.com/user-attachments/assets/3fe732ac-a956-45d5-bdc9-031eeedf2048" />

</div>
---

## Proje Hakkında
 
**NADA Drone Sistemleri**, drone ile çekilen video ve fotoğrafları işleyip üzerinde **YOLOv3** ile nesne tespiti (insan, araç vb.) yapan; uçuş güzergahları ve canlı nesne takip özelliklerini tek bir panelde toplayan bir bitirme (tez) projesidir. Django ile geliştirilmiştir.

## Özellikler
 
- 🎥 **Video Analizi** — Yüklenen drone videoları YOLOv3 ile işlenir, nesneler tespit edilir tespit edilen nesnelerin etiketi ile işlenmiş video kaydedilir
- 📊 **Video Raporu** — Tespit edilen nesnelerin dağılımı Matplotlib ile pasta grafiği olarak sunulur
- 🗺️ **Güzergah Planlama** — Harita üzerinde seçilen noktalar arasında **A\* algoritması** ile en kısa rota hesaplanır ve kaydedilir
- 📡 **Canlı Takip** — Gerçek zamanlı nesne takibi sayfası (Bilgisayar kamerasından gerçek zamanlı olarak nesne tespiti)
- 🚁 **Drone Filosu Yönetimi** — Kamera tipi, uçuş menzili, güç türü, koruma derecesi gibi teknik bilgilerin kaydı

## Kullanılan Teknolojiler

| Katman | Teknoloji |
|---|---|
| Backend | Python, Django |
| Nesne Tespiti | OpenCV (`cv2.dnn`), YOLOv3 |
| Veri Görselleştirme | Matplotlib, Plotly |
| Harita | Leaflet |
| Rota Hesaplama | A* (A-Star) algoritması |
| Arayüz | HTML / CSS |

> **YOLOv3 ağırlık dosyası:** `yolov3.weights` dosyası boyutu nedeniyle repoya eklenmemiştir.



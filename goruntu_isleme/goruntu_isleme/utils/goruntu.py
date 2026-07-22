import cv2

# Haar Cascade dosyalarının yolları
human_cascade_path = cv2.data.haarcascades + "haarcascade_fullbody.xml"
vehicle_cascade_path = cv2.data.haarcascades + "haarcascade_car.xml"  # Araç modeli için gerekli dosyayı ekleyin

# Sınıflandırıcıları yükleme
human_cascade = cv2.CascadeClassifier(human_cascade_path)
vehicle_cascade = cv2.CascadeClassifier(vehicle_cascade_path)

# İşlenecek görüntünün yolu
image_path = "deneme.jpg"  # Fotoğrafınızın dosya yolu

# Görüntüyü yükleme
image = cv2.imread(image_path)
if image is None:
    print("Görüntü yüklenemedi. Lütfen dosya yolunu kontrol edin.")
    exit()

# Görüntüyü gri tonlamaya çevirme
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)

# İnsan ve araç tespiti
humans = human_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
vehicles = vehicle_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

# İnsan tespitlerini çerçeveleme
for (x, y, w, h) in humans:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(image, "Human", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Araç tespitlerini çerçeveleme
for (x, y, w, h) in vehicles:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.putText(image, "Vehicle", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

# Sonuçları gösterme
cv2.imshow("Detection", image)

# 'q' tuşuna basıldığında pencereyi kapatır
cv2.waitKey(0)
cv2.destroyAllWindows()

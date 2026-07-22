import cv2
import numpy as np
import time

# ------------------------- YOLOv3 Modeli -------------------------
# YOLOv3 için ağ yükleme
yolo_net = cv2.dnn.readNet("static/yolov3.weights", "static/yolov3.cfg")
layer_names = yolo_net.getLayerNames()
output_layers = [layer_names[i - 1] for i in yolo_net.getUnconnectedOutLayers()]

# ------------------------- Haar Sınıflandırıcı -------------------------
# Haar sınıflandırıcı için model yükleme
human_cascade_path = cv2.data.haarcascades + "haarcascade_fullbody.xml"

# ------------------------- Test Görüntüsü -------------------------
# Görüntü yükleme
image_path = "deneme3.jpg"
image = cv2.imread(image_path)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# ------------------------- Performans Hesaplama (FPS) -------------------------
start_time = time.time()

# ------------------------- YOLOv3 ile Nesne Tespiti -------------------------
# YOLOv3'ü çalıştırma
blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
yolo_net.setInput(blob)
yolo_outputs = yolo_net.forward(output_layers)

# YOLOv3 tespitlerini görselleştirme
yolo_boxes = []
yolo_confidences = []
yolo_class_ids = []

for output in yolo_outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:
            center_x = int(detection[0] * image.shape[1])
            center_y = int(detection[1] * image.shape[0])
            width = int(detection[2] * image.shape[1])
            height = int(detection[3] * image.shape[0])
            x = int(center_x - width / 2)
            y = int(center_y - height / 2)
            yolo_boxes.append([x, y, width, height])
            yolo_confidences.append(float(confidence))
            yolo_class_ids.append(class_id)

# ------------------------- Haar Sınıflandırıcı ile Nesne Tespiti -------------------------
# Yüzleri tespit etme (Haar Sınıflandırıcı)
haar_faces = human_cascade_path.detectMultiScale(gray_image, 1.1, 4)

# Haar sınıflandırıcı sonuçlarını görselleştirme
haar_boxes = []
for (x, y, w, h) in haar_faces:
    haar_boxes.append([x, y, w, h])

# ------------------------- Performans Hesaplama (FPS) -------------------------
end_time = time.time()
fps = 1 / (end_time - start_time)
print(f"FPS: {fps}")

# ------------------------- Görselleştirme -------------------------
# YOLOv3 tespitlerini çizme
for i, box in enumerate(yolo_boxes):
    x, y, w, h = box
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# Haar tespitlerini çizme
for (x, y, w, h) in haar_boxes:
    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

# Sonuçları görselleştir
cv2.imshow("Comparison: YOLOv3 vs Haar", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# ------------------------- Performans Metrikleri -------------------------
# Bu kısımda, Precision, Recall, F1-Score gibi metrikleri hesaplayabilirsin.
# Örneğin, IoU (Intersection over Union) hesaplamasını yapmak için aşağıdaki fonksiyonu kullanabilirsin.

def calculate_iou(pred_box, true_box):
    x1, y1, w1, h1 = pred_box
    x2, y2, w2, h2 = true_box
    # Kesişim alanı hesaplama
    inter_area = max(0, min(x1 + w1, x2 + w2) - max(x1, x2)) * max(0, min(y1 + h1, y2 + h2) - max(y1, y2))
    # Birleşim alanı hesaplama
    union_area = w1 * h1 + w2 * h2 - inter_area
    return inter_area / union_area if union_area != 0 else 0

# Örnek IoU hesaplama
for yolo_box in yolo_boxes:
    for haar_box in haar_boxes:
        iou = calculate_iou(yolo_box, haar_box)
        print(f"IoU: {iou}")

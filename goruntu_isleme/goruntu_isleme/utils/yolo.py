import cv2
import numpy as np

# YOLO modelini ve yapılandırma dosyasını yükleyin
yolo_net = cv2.dnn.readNet("static/yolov3.weights", "static/yolov3.cfg")

# Nesne isimlerini yükleyin
with open("static/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Video veya Görüntü dosyasını yükleyin
image = cv2.imread('deneme.jpg')  # Kendi görüntünüzü buraya ekleyin

# Görüntüyü blob formatına dönüştürün
blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

# Modeli çalıştırın
yolo_net.setInput(blob)
layer_names = yolo_net.getLayerNames()
output_layers = [layer_names[i-1] for i in yolo_net.getUnconnectedOutLayers()]
outs = yolo_net.forward(output_layers)

# Sonuçları işleyin
height, width, _ = image.shape
boxes = []
confidences = []
class_ids = []

for out in outs:
    for detection in out:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5:  # Güven eşiği
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = int(center_x - w / 2)
            y = int(center_y - h / 2)
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Non-maxima suppression ile çakışan kutuları filtreleyin
indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# Tespit edilen nesneleri çizme
if len(indices) > 0:
    for i in indices.flatten():
        x, y, w, h = boxes[i]
        label = str(classes[class_ids[i]])
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

cv2.imshow("Detected Objects", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

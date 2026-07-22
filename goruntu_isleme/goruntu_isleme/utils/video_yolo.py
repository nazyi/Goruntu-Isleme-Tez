import cv2
import numpy as np

# YOLO modelini ve yapılandırma dosyasını yükleyin
yolo_net = cv2.dnn.readNet("static/yolov3.weights", "static/yolov3.cfg")

# Nesne isimlerini yükleyin
with open("static/coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Video dosyasını yükleyin
video_path = "utils/video.mp4"  # Video dosyasını buraya ekleyin
cap = cv2.VideoCapture(video_path)

# Çıkış videosu için ayarlar
output_path = "output_video.avi"
fourcc = cv2.VideoWriter_fourcc(*"XVID")
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

if not out.isOpened():
    print("VideoWriter oluşturulamadı!")
    exit()

# Video işleme döngüsü
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Frame boyutlarını kontrol et ve gerekirse yeniden boyutlandır
    if frame.shape[1] != frame_width or frame.shape[0] != frame_height:
        frame = cv2.resize(frame, (frame_width, frame_height))

    # Görüntüyü blob formatına dönüştürün
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    # Modeli çalıştırın
    yolo_net.setInput(blob)
    layer_names = yolo_net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in yolo_net.getUnconnectedOutLayers()]
    outs = yolo_net.forward(output_layers)

    # Sonuçları işleyin
    height, width, _ = frame.shape
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
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # İşlenmiş frame'i çıkış videosuna yazın
    #out.write(frame)

    # Frame'i ekranda gösterin (isteğe bağlı)
    cv2.imshow("YOLO Video Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Kaynakları serbest bırakın
cap.release()
out.release()
cv2.destroyAllWindows()

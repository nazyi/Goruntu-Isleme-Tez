import cv2
import numpy as np
import imageio

def analyze_video(video_path, output_path):
    net = cv2.dnn.readNet("static/yolov3.weights", "static/yolov3.cfg")
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]
    with open("static/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    writer = imageio.get_writer(output_path, fps=30)

    trackers = []  
    detection_history = [] 

    def calculate_iou(boxA, boxB):
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[0] + boxA[2], boxB[0] + boxB[2])
        yB = min(boxA[1] + boxA[3], boxB[1] + boxB[3])

        interArea = max(0, xB - xA) * max(0, yB - yA)

        boxAArea = boxA[2] * boxA[3]
        boxBArea = boxB[2] * boxB[3]

        iou = interArea / float(boxAArea + boxBArea - interArea)
        return iou

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)

        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores) 
                confidence = scores[class_id]  

                if confidence > 0.5:  
                    center_x = int(detection[0] * frame_width)
                    center_y = int(detection[1] * frame_height)
                    w = int(detection[2] * frame_width)
                    h = int(detection[3] * frame_height)
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        if len(indexes) > 0:
            for i in indexes.flatten():
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])

                matched = False
                for tracked_object in trackers:
                    iou = calculate_iou([x, y, w, h], tracked_object['coordinates'])
                    if iou > 0.3:  
                        matched = True
                        break

                if not matched:
                    tracker = cv2.TrackerCSRT_create() 
                    tracker.init(frame, (x, y, w, h))
                    trackers.append({'tracker': tracker, 'label': label, 'coordinates': (x, y, w, h)})

                    timestamp = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000  
                    detection_history.append({
                        'label': label,
                        'timestamp': timestamp,
                        'coordinates': (x, y, w, h)
                    })

        for tracked_object in trackers:
            success, bbox = tracked_object['tracker'].update(frame)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(frame, tracked_object['label'], (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        writer.append_data(frame)

    cap.release()
    writer.close()

    
    return detection_history  

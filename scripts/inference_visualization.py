import os
import cv2
import json
import time
from datetime import datetime
from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
MODEL_PATH = os.path.join(BASE_DIR, "scripts", "runs", "detect", "fine_tuning_v3_adamw", "weights", "best.pt")
VIDEO_PATH = os.path.join(BASE_DIR, "data", "video_containers_3.mp4")
RESULTS_PATH = os.path.join(BASE_DIR, "results", "events.json")

model = YOLO(MODEL_PATH)
tracker = DeepSort(max_age=30)

cap = cv2.VideoCapture(VIDEO_PATH)
events = []

refill_time_threshold = 3  
prev_bowl_states = {}
disappeared_bowls = {}

def get_current_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

frame_index = 0
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    frame_enhanced = cv2.cvtColor(clahe.apply(gray), cv2.COLOR_GRAY2BGR)
    
    results = model(frame_enhanced, conf=0.01, iou=0.05)
    boxes = results[0].boxes.xyxy.cpu().numpy()
    confidences = results[0].boxes.conf.cpu().numpy()
    class_ids = results[0].boxes.cls.cpu().numpy()
    
    detections = [(box, confidence, class_id) for box, confidence, class_id in zip(boxes, confidences, class_ids)]
    tracks = tracker.update_tracks(detections, frame=frame)
    
    current_time = time.time()
    active_bowls = set()

    for track in tracks:
        if not track.is_confirmed():
            continue
        
        track_id, bbox = track.track_id, track.to_tlbr()
        active_bowls.add(track_id)

        if track_id not in prev_bowl_states or track_id in disappeared_bowls:
            events.append({
                "timestamp": get_current_timestamp(),
                "container_id": track_id,
                "event_type": "refill",
                "bbox": bbox.tolist()
            })
            disappeared_bowls.pop(track_id, None)  

        elif track_id in prev_bowl_states:
            prev_bbox, _ = prev_bowl_states[track_id]
            if any(abs(prev_bbox[i] - bbox[i]) > 5 for i in range(4)):  
                events.append({
                    "timestamp": get_current_timestamp(),
                    "container_id": track_id,
                    "event_type": "movement",
                    "bbox": bbox.tolist()
                })

        prev_bowl_states[track_id] = (bbox, current_time)

        cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), (0, 255, 0), 2)
        cv2.putText(frame, f"ID: {track_id}", (int(bbox[0]), int(bbox[1]) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    for track_id in list(prev_bowl_states.keys()):
        if track_id not in active_bowls and track_id not in disappeared_bowls:
            disappeared_bowls[track_id] = current_time
            events.append({
                "timestamp": get_current_timestamp(),
                "container_id": track_id,
                "event_type": "disappearance"
            })

    cv2.imshow("YOLO + DeepSORT", frame)
    frame_index += 1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

with open(RESULTS_PATH, "w") as f:
    json.dump(events, f, indent=4)

print("Events saved in events.json")


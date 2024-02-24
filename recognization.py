import cv2 as cv
import mediapipe as mp
import numpy as np
from pyzbar import pyzbar

last_key_points = None
key_points_dy_dx_mean = []

# Recognized barcodes. Don't recognize them again.
last_recognized_barcodes = set()

mp_face_detection = mp.solutions.face_detection

# Start the window thread and prepare the camera
cv.startWindowThread()
cap = None

# Is the tape running?
face_running = last_face_running = False
barcode_running = last_barcode_running = False


def read_barcodes(frame):
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        barcode_text = barcode.data.decode('utf-8')
        if barcode_text not in last_recognized_barcodes:
            print(barcode_text)
            with open("codes.stat", "a") as f:
                f.write(barcode_text + "\n");
        last_recognized_barcodes.add(barcode_text)
        x, y , w, h = barcode.rect
        cv.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
    return frame
 

# noinspection PyUnresolvedReferences
def main():
    global last_key_points, cap, face_running, last_face_running, barcode_running, last_barcode_running
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 240)

    with open("codes.stat", "w") as f:
        f.write("")

    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5
    ) as face_detector:
        while True:
            summary()
            with open("running.stat", "r") as f:
                content = f.read()
                face_running = content == "Face"
                barcode_running = content == "Barcode"
                if last_face_running != face_running:
                    if not face_running:
                        print("Face Paused")
                    else:
                        print("Face Resumed")
                last_face_running = face_running
                
                if last_barcode_running != barcode_running:
                    if not barcode_running:
                        print("Barcode Paused")
                    else:
                        print("Barcode Resumed")
                last_barcode_running = barcode_running
            
            if face_running:
                ret, frame = cap.read()
                if ret is False:
                    break
                if not face_running and not barcode_running:
                    cv.namedWindow("frame")
                    cv.imshow("frame", frame)
                    key = cv.waitKey(1)
                    if key == ord("b"):
                        return
                    continue  # Skip the rest of the loop
                rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

                results = face_detector.process(rgb_frame)
                frame_height, frame_width, c = frame.shape
                if not results.detections:
                    cv.namedWindow("frame")
                    cv.imshow("frame", frame)
                    key = cv.waitKey(1)
                    if key == ord("b"):
                        return
                    continue
                # ---- Detection ----
                # Only one face per time
                face = results.detections[0]
                # Detect the face rectangle
                face_rect = np.multiply(
                    [
                        face.location_data.relative_bounding_box.xmin,
                        face.location_data.relative_bounding_box.ymin,
                        face.location_data.relative_bounding_box.width,
                        face.location_data.relative_bounding_box.height,
                    ],
                    [frame_width, frame_height, frame_width, frame_height],
                ).astype(int)
                key_points = np.array(
                    [(p.x, p.y) for p in face.location_data.relative_keypoints]
                )
                key_points_coords = np.multiply(
                    key_points, [frame_width, frame_height]
                ).astype(int)

                try:
                    key_points_dy_dx = key_points - last_key_points
                    # print(key_points_dy_dx.mean())
                    key_points_dy_dx_mean.append(key_points_dy_dx.mean())
                # During the first iteration, the value of the last key points are missing. This is negligible.
                except TypeError:
                    print("No last key points")
                finally:
                    last_key_points = key_points

                # ---- Annotate ----
                cv.putText(frame, "Face Mode", (0, 0), cv.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
                cv.rectangle(frame, face_rect, color=(0, 255, 0), thickness=2)

                for p in key_points_coords:
                    cv.circle(frame, p, 4, (0, 255, 0), 2)

                cv.namedWindow("frame", cv.WND_PROP_FULLSCREEN)
                cv.setWindowProperty(
                    "frame", cv.WND_PROP_FULLSCREEN, cv.WINDOW_NORMAL
                )
                cv.imshow("frame", frame)
                
            elif barcode_running:
                ret, frame = cap.read()
                frame = read_barcodes(frame)
                cv.imshow('Barcode reader', frame)
                
            
            key = cv.waitKey(1)
            if key == ord("b"):
                return


def stop():
    if cap is not None:
        cap.release()
    cv.destroyAllWindows()
    summary()


def summary():
    score = 0.5 / (np.std(key_points_dy_dx_mean) * 10) + 25
    if score < 50:
        score -= 2.5
    elif score > 100:
        score = 100
    elif np.isnan(score):
        score = 0
    # print(f"Your score is: {score:.1f}")

    # Write score to file
    with open("score.stat", "w") as f:
        f.write(f"{score:.1f}")


if __name__ == "__main__":
    main()
    stop()

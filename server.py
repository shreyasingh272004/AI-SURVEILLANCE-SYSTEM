from flask import Flask, Response, send_from_directory
from flask_cors import CORS
import cv2
import csv
from collections import Counter, defaultdict
from collections import defaultdict
import os


from ai_engine import AIEngine

app = Flask(__name__)
CORS(app)

cap = cv2.VideoCapture(0)
engine = AIEngine()


def generate_frames():

    while True:

        success, frame = cap.read()

        if not success:
            break

        # Process frame using your AI
        processed_frame = engine.process_frame(frame)

        # Convert frame to JPEG
        _, buffer = cv2.imencode(".jpg", processed_frame)

        frame_bytes = buffer.tobytes()

        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' +
            frame_bytes +
            b'\r\n'
        )


@app.route("/video")
def video():
    return Response(
        generate_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

@app.route("/stats")
def stats():

    events = []

    with open("logs/events.csv", "r") as file:

        reader = csv.DictReader(file)

        for row in reader:
            events.append(row)

    total_threats = len(events)

    intrusion_count = sum(
        1 for e in events
        if e["Event"] == "Intrusion"
    )

    crowd_count = sum(
        1 for e in events
        if e["Event"] == "Crowd"
    )

    threat_counter = Counter(
        e["Threat"] for e in events
    )

    if threat_counter:
        overall = threat_counter.most_common(1)[0][0]
    else:
        overall = "LOW"

    return {
        "totalThreats": total_threats,
        "intrusions": intrusion_count,
        "crowdEvents": crowd_count,
        "threatLevel": overall
    }

@app.route("/events")
def events():

    rows = []

    with open("logs/events.csv", "r") as file:

        reader = csv.DictReader(file)

        for row in reader:
            rows.append(row)

    # Return latest 10 events
    rows = rows[::-1][:6]

    return rows

@app.route("/analytics")
def analytics():

    hourly_counts = defaultdict(int)

    with open("logs/events.csv", "r") as file:

        reader = csv.DictReader(file)

        for row in reader:

            time = row["Timestamp"].split(" ")[1][:2] + ":00"

            hourly_counts[time] += 1

    data = []

    for hour in sorted(hourly_counts.keys()):

        data.append({
            "time": hour,
            "threat": hourly_counts[hour]
        })

    return data

@app.route("/screenshots/<filename>")
def screenshots(filename):

    return send_from_directory(
        "screenshots",
        filename
    )

@app.route("/gallery")
def gallery():

    files = sorted(
        os.listdir("screenshots"),
        reverse=True
    )[:8]

    return files


if __name__ == "__main__":
    app.run(debug=True)
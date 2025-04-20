from flask import Flask, request, jsonify, render_template, Response
import os
import cv2
import mediapipe as mp
import requests
import time
import tempfile
from process_video import process_video_and_translate

app = Flask(__name__)

current_processing_frame = None
UPLOAD_FOLDER = 'uploads'
TRIMMED_FOLDER = 'trimmed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRIMMED_FOLDER, exist_ok=True)

# Store the latest trimmed video path so it can be used for video feed
current_trimmed_video = None

# Setup MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


@app.route('/')
def index():
    return render_template('landing.html')
@app.route('/test')
def test():
    return render_template('index.html')


@app.route('/process_video', methods=['POST'])
def process_video():
    global current_trimmed_video

    if 'video' not in request.files:
        return jsonify({'error': 'No video uploaded'})

    video_file = request.files['video']
    if video_file.filename == '':
        return jsonify({'error': 'No file selected'})

    start_time = float(request.form.get('start_time', 0))
    end_time = float(request.form.get('end_time', 0))

    # Save the full uploaded video
    video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
    video_file.save(video_path)

    # Trim the video based on the provided start and end times
    trimmed_video_path = os.path.join(TRIMMED_FOLDER, f"trimmed_{video_file.filename}")
    success = trim_video(video_path, trimmed_video_path, start_time, end_time)

    if not success:
        return jsonify({'error': 'Failed to trim video'})

    # Store path for the live preview
    current_trimmed_video = trimmed_video_path

    # Process the trimmed video
    result = process_video_and_translate(trimmed_video_path)

    if isinstance(result, dict):
        return jsonify({
            'translation': result.get('translation', ''),
            'lexicon_translation': result.get('tagalog', ''),
            'detected_signs': result.get('detected_signs', '')
        })
    else:
        return jsonify({
            'error': 'Unexpected result format from translation function'
        })


@app.route('/process_video_url', methods=['POST'])
def process_video_url():
    global current_trimmed_video
    
    data = request.json
    if not data or 'url' not in data:
        return jsonify({'error': 'No video URL provided'})
        
    video_url = data['url']
    start_time = float(data.get('start_time', 0))
    end_time = float(data.get('end_time', 0))
    
    try:
        # Create a temporary file to store the downloaded video
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            # Download the video
            response = requests.get(video_url, stream=True)
            if response.status_code != 200:
                return jsonify({'error': 'Failed to download video from URL'})
                
            # Write the video to the temp file
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    temp_file.write(chunk)
            
            video_path = temp_file.name
        
        # Trim the video based on the provided start and end times
        filename = os.path.basename(video_path)
        trimmed_video_path = os.path.join(TRIMMED_FOLDER, f"trimmed_{filename}")
        success = trim_video(video_path, trimmed_video_path, start_time, end_time)
        
        # Remove the temporary file
        os.unlink(video_path)
        
        if not success:
            return jsonify({'error': 'Failed to trim video'})
            
        # Store path for the live preview
        current_trimmed_video = trimmed_video_path
        
        # Process the trimmed video
        translation, lexicon_translation = process_video_and_translate(trimmed_video_path)
        
        print(f"app.py{translation} .. {lexicon_translation}")
        return jsonify({
            'translation': translation,
            'lexicon_translation': lexicon_translation
        })
        
    except Exception as e:
        return jsonify({'error': f'Error processing video URL: {str(e)}'})


@app.route('/video_feed')
def video_feed():
    """This will provide the video stream with MediaPipe detection."""
    return Response(generate_mediapipe_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_mediapipe_frames():
    global current_processing_frame
    while True:
        if current_processing_frame is not None:
            _, buffer = cv2.imencode('.jpg', current_processing_frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        else:
            time.sleep(0.1)


def trim_video(input_path, output_path, start_time, end_time):
    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    frame_number = start_frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret or frame_number > end_frame:
            break
        out.write(frame)
        frame_number += 1

    cap.release()
    out.release()

    return os.path.exists(output_path)


if __name__ == '__main__':
    app.run(debug=True)
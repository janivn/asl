import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
import pandas as pd
import os

# Path resolution for the assets relative to this file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load model and lexicon once at the start to save time
model_path = os.path.join(current_dir, 'assets/model/200425 uneven.h5')
classes_path = os.path.join(current_dir, 'assets/model/200425 uneven.npy')
lexicon_path = os.path.join(current_dir, 'assets/lexicon/lexicon.csv')

try:
    model = tf.keras.models.load_model(model_path)
    label_encoder_classes = np.load(classes_path)
    print(label_encoder_classes)
    print(f"Model loaded with {label_encoder_classes.shape} classes")
    lexicon_df = pd.read_csv(lexicon_path)
    lexicon_dict = dict(zip(lexicon_df['ASL Structure'], lexicon_df['Tagalog']))
except Exception as e:
    print(f"Error loading model or lexicon: {e}")
    # Create fallbacks for development/demo
    if not os.path.exists(model_path):
        print(f"Model file not found at {model_path}")
    if not os.path.exists(classes_path):
        print(f"Classes file not found at {classes_path}")
    if not os.path.exists(lexicon_path):
        print(f"Lexicon file not found at {lexicon_path}")

mp_hands = mp.solutions.hands
mp_pose = mp.solutions.pose
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

num_hand_keypoints = 21 * 2
num_pose_keypoints = 33 * 3
max_frames = 24
confidence_threshold = 0.95

pronouns = {"me", "I", "you", "we", "he", "she", "they"}

def extract_keypoints(frame):
    frame_data = np.zeros(num_hand_keypoints + num_pose_keypoints)
    
    # Convert frame to RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process hands
    hand_results = hands.process(rgb_frame)
    if hand_results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
            if i < 2:  # Only process up to 2 hands
                hand_keypoints = []
                for landmark in hand_landmarks.landmark:
                    hand_keypoints.extend([landmark.x, landmark.y])
                # Fill in the appropriate section of frame_data
                offset = i * 42  # 21 landmarks * 2 coordinates
                frame_data[offset:offset + len(hand_keypoints)] = hand_keypoints

    # Process pose
    pose_results = pose.process(rgb_frame)
    if pose_results.pose_landmarks:
        pose_keypoints = []
        for landmark in pose_results.pose_landmarks.landmark:
            pose_keypoints.extend([landmark.x, landmark.y, landmark.z])
        frame_data[num_hand_keypoints:] = pose_keypoints

    return frame_data

def reorder_translation(predictions):
    if not predictions:
        return []
        
    filtered = []
    pronoun = None
    action_word = None
    
    for word in predictions:
        if word in pronouns and pronoun is None:
            pronoun = word
        elif word not in pronouns and action_word is None:
            action_word = word
    
    if pronoun and action_word:
        filtered.append(f"{pronoun} {action_word}")
    elif action_word:
        filtered.append(action_word)
    elif pronoun:
        filtered.append(pronoun)
    
    return filtered

def match_translation(asl_structure):
    try:
        row = lexicon_df.loc[lexicon_df['ASL Structure'] == asl_structure].iloc[0]
        return {
            "english": row['English'],
            "tagalog": row['Tagalog']
        }
    except Exception:
        return {
            "english": "No match found",
            "tagalog": "No match found"
        }


def process_video_and_translate(video_path):
    print(video_path)
    # For development mode - if we don't have a model, return dummy results
    if not os.path.exists(video_path):
        print(f"Error: Video file not found at {video_path}")
        return "Video file not found", "No match found"
        
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return "Could not open video file", "No match found"
            
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        print(f"Processing video with {total_frames} frames")

        frames = []
        predictions = []
        sign_detected = False
        frame_count = 0

        while cap.isOpened() and frame_count < 150:  # Limit to max 150 frames for safety
            ret, frame = cap.read()
            if not ret:
                break
                
            frame_count += 1
            
            # Extract keypoints from the current frame
            keypoints = extract_keypoints(frame)
            frames.append(keypoints)

            # When we have enough frames for a prediction
            if len(frames) == max_frames:
                input_data = np.expand_dims(np.array(frames), axis=0)
                
                try:
                    # Make prediction
                    prediction = model.predict(input_data)
                    predicted_class = np.argmax(prediction, axis=1)[0]
                    confidence = np.max(prediction)

                    if confidence >= confidence_threshold:
                        sign_name = label_encoder_classes[predicted_class]
                        predictions.append(sign_name)
                        sign_detected = True
                        print(f"Detected sign: {sign_name} with confidence {confidence:.2f}")
                except Exception as e:
                    print(f"Error during prediction: {e}")
                
                # Reset frames buffer for next prediction
                frames = []

        cap.release()

        if not sign_detected:
            return "No sign detected", "No match found"

        # Remove consecutive duplicates
        final_predictions = []
        for i, pred in enumerate(predictions):
            if i == 0 or pred != predictions[i - 1]:
                final_predictions.append(pred)

        cleaned_translation = " ".join(reorder_translation(final_predictions))
        if not cleaned_translation:
            cleaned_translation = "No clear signs detected"
            
        lexicon_translation = match_translation(cleaned_translation)
        
        print(f"Final ASL translation: {cleaned_translation}")
        print(f"Tagalog translation: {lexicon_translation}")

        return {
    "detected_signs": cleaned_translation,
    "translation": lexicon_translation  # This is a dictionary now
}
        
    except Exception as e:
        print(f"Error processing video: {e}")
        return f"Error: {str(e)}", "No translation available"
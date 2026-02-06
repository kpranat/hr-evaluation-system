import cv2
import numpy as np
import base64
import mediapipe as mp

# Initialize MediaPipe solutions
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_hands = mp.solutions.hands

def analyze_frame(image_data):
    """
    Analyzes a base64 encoded image frame using OpenCV and MediaPipe.
    Detects: No Face, Multiple Faces, Looking Away (Head Pose), Hand Detected.

    Args:
        image_data (str): Base64 encoded image string (e.g. "data:image/jpeg;base64,...")

    Returns:
        dict: Analysis results containing violations and details.
    """
    try:
        # 1. Decode Base64 Image
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        image_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            return {'error': 'Failed to decode image'}

        height, width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Prepare results dictionary
        results = {
            'face_detected': False,
            'multiple_faces': False,
            'looking_away': False,
            'phone_detected': False, # Using hand detection as proxy
            'hand_detected': False,
            'details': []
        }

        # 2. Face Detection (Fast check for count)
        with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
            detection_result = face_detection.process(rgb_frame)

            if not detection_result.detections:
                results['face_detected'] = False
                results['details'].append("No face detected")
                # Return early if no face? No, checking hands might still be useful.
            else:
                results['face_detected'] = True
                face_count = len(detection_result.detections)

                if face_count > 1:
                    results['multiple_faces'] = True
                    results['details'].append(f"Multiple faces detected: {face_count}")

        # 3. Head Pose / Gaze Tracking (using Face Mesh)
        # We only run this if at least one face is detected to avoid heavy processing on empty frames
        if results['face_detected']:
            with mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as face_mesh:

                mesh_result = face_mesh.process(rgb_frame)

                if mesh_result.multi_face_landmarks:
                    landmarks = mesh_result.multi_face_landmarks[0].landmark

                    # 3D Head Pose Estimation
                    # Nose tip: 1, Chin: 152, Left Eye Left Corner: 33, Right Eye Right Corner: 262, Left Mouth Corner: 61, Right Mouth Corner: 291
                    face_3d = []
                    face_2d = []

                    # Points to track
                    points_idx = [33, 262, 1, 61, 291, 199]

                    for idx in points_idx:
                        lm = landmarks[idx]
                        x, y = int(lm.x * width), int(lm.y * height)
                        face_2d.append([x, y])
                        face_3d.append([x, y, lm.z])

                    face_2d = np.array(face_2d, dtype=np.float64)
                    face_3d = np.array(face_3d, dtype=np.float64)

                    # Camera matrix
                    focal_length = 1 * width
                    cam_matrix = np.array([[focal_length, 0, height / 2],
                                           [0, focal_length, width / 2],
                                           [0, 0, 1]])

                    # Distortion matrix
                    dist_matrix = np.zeros((4, 1), dtype=np.float64)

                    # Solve PnP
                    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                    if success:
                        rmat, jac = cv2.Rodrigues(rot_vec)
                        angles, mtxR, mtxQ, Q, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                        x = angles[0] * 360 # Pitch (Up/Down)
                        y = angles[1] * 360 # Yaw (Left/Right)

                        # Thresholds for looking away
                        # Adjust based on testing. Typically > 10-15 degrees is noticeable turn.
                        if y < -15:
                            results['looking_away'] = True
                            results['details'].append("Looking Right")
                        elif y > 15:
                            results['looking_away'] = True
                            results['details'].append("Looking Left")
                        elif x < -10:
                            results['looking_away'] = True
                            results['details'].append("Looking Down")
                        elif x > 20: # Looking up is less suspicious usually
                            results['looking_away'] = True
                            results['details'].append("Looking Up")

        # 4. Hand Detection (Suspicious Objects)
        # Using Hands to detect if hands are near face or holding something
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:

            hands_result = hands.process(rgb_frame)

            if hands_result.multi_hand_landmarks:
                results['hand_detected'] = True
                # If hands are detected, we can flag it.
                # In strict proctoring, hands shouldn't be near the face/camera usually, unless typing (which is lower).
                # We could check Y coordinate. If hand is high (near face), it's suspicious.

                suspicious_hand = False
                for hand_landmarks in hands_result.multi_hand_landmarks:
                    for lm in hand_landmarks.landmark:
                        # If hand landmark y is less than e.g. 0.8 (where 1.0 is bottom), it might be raised.
                        # Usually face is at 0.3-0.6 range.
                        if lm.y < 0.9: # Hand is raised
                            suspicious_hand = True
                            break

                if suspicious_hand:
                    results['phone_detected'] = True # Proxy for "Suspicious object/hand"
                    results['details'].append("Hand detected in frame")

        return results

    except Exception as e:
        print(f"Error in analyze_frame: {str(e)}")
        return {
            'error': str(e),
            'face_detected': False
        }

# Alias for backward compatibility during refactor
def analyze_frame_with_llama(image_data):
    return analyze_frame(image_data)

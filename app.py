from flask import Flask, render_template, Response, request, jsonify
import cv2
import mediapipe as mp
import time

app = Flask(__name__)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)  # Use the default camera

current_expression = ""
operation_result = None
last_detected_value = None
last_detection_time = 0

def generate_frames():
    global current_expression, operation_result, last_detected_value, last_detection_time
    
    with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7) as hands:
        while True:
            success, image = cap.read()
            if not success:
                break

            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                    detected_value = detect_gesture(hand_landmarks)

                    current_time = time.time()
                    if detected_value is not None and detected_value != last_detected_value:
                        if current_time - last_detection_time > 1:  # 1 second delay
                            if detected_value == 'clear':
                                current_expression = ''
                            elif detected_value == 'equal':
                                try:
                                    operation_result = eval(current_expression)
                                    current_expression = str(operation_result)
                                except Exception as e:
                                    current_expression = "Error"
                            else:
                                current_expression += detected_value

                            last_detected_value = detected_value
                            last_detection_time = current_time

                    # Display the current expression and result on the video feed
                    cv2.putText(image, f'Expression: {current_expression}', (10, 30), 
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', image)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def calculator():
    return render_template('calculator.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/calculate', methods=['POST'])
def calculate():
    global current_expression
    data = request.get_json()
    expression = data.get('expression')
    try:
        result = eval(expression)
    except Exception as e:
        result = "Error"
    return jsonify({"result": result})

def detect_gesture(hand_landmarks):
    fingers = count_fingers(hand_landmarks)
    
    if fingers == [0, 1, 0, 0, 0]:
        return "1"
    elif fingers == [0, 1, 1, 0, 0]:
        return "2"
    elif fingers == [0, 1, 1, 1, 0]:
        return "3"
    elif fingers == [0, 1, 1, 1, 1]:
        return "4"
    elif fingers == [1, 1, 1, 1, 1]:
        return "5"
    elif fingers == [1, 0, 0, 0, 0]:
        return "6"
    elif fingers == [1, 1, 0, 0, 0]:
        return "7"
    elif fingers == [1, 1, 1, 0, 0]:
        return "8"
    elif fingers == [1, 1, 1, 1, 0]:
        return "9"
    elif fingers == [0, 0, 0, 0, 0]:
        return "0"
    elif fingers == [0, 1, 0, 0, 1]:  
        return "+"
    elif fingers == [1, 0, 0, 0, 1]: 
        return "-"
    elif fingers == [1, 0, 0, 1, 0]:  
        return "*"
    elif fingers == [1, 0, 0, 1, 1]:  
        return "/"
    elif fingers == [0, 0, 1, 1, 0]:  
        return "equal"
    elif fingers == [0, 0, 1, 0, 0]:  
        return "clear"
    
    return None

def count_fingers(hand_landmarks):
    finger_tip_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[finger_tip_ids[0]].x < hand_landmarks.landmark[finger_tip_ids[0] - 2].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other four fingers
    for i in range(1, 5):
        if hand_landmarks.landmark[finger_tip_ids[i]].y < hand_landmarks.landmark[finger_tip_ids[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

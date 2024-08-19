# Gesture-Based Virtual Calculator

This project is a gesture-controlled virtual calculator built using Flask, OpenCV, and Mediapipe. It detects hand gestures using a webcam feed and performs basic arithmetic operations based on the recognized gestures. The application also allows manual input via the HTML interface.

## Features

- Real-time hand gesture recognition using OpenCV and Mediapipe.
- Arithmetic operations (addition, subtraction, multiplication, division) using recognized hand gestures.
- Web interface built using Flask and HTML for manual input and camera feed display.

## Project Structure
├── app.py 
### Main Flask application
├── templates/ │ └── calculator.html
### HTML file for the calculator interface
└── README.md
### Project documentation

## Requirements

- Python 3.7+
- Flask
- OpenCV
- Mediapipe

## How to Run

1. Clone the repository:
    ```bash
    git clone https://github.com/<your-username>/Virtual-Calculator.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Virtual-Calculator
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    python app.py
    ```

5. Open a web browser and go to:
    ```
    http://127.0.0.1:5000
    ```

## How It Works

- **Hand Gesture Recognition:** The app uses OpenCV and Mediapipe to detect hand landmarks and recognize finger gestures. Each gesture corresponds to a specific digit or operation.
  
- **Manual Input:** You can manually enter expressions via the calculator buttons in the HTML interface.

- **Real-time Calculation:** The recognized gestures are continuously added to the expression, and showing the "equals" gesture performs the calculation.

## Gesture Mapping

| Gesture                         | Recognized As |
|---------------------------------|---------------|
| One Finger Up                   | 1             |
| Two Fingers Up                  | 2             |
| Three Fingers Up                | 3             |
| Four Fingers Up                 | 4             |
| Five Fingers Up                 | 5             |
| Thumb Up                        | 6             |
| Thumb and Index Finger Up       | 7             |
| Thumb, Index, and Middle Finger | 8             |
| Thumb, Index, Middle, and Ring  | 9             |
| Fist (All Fingers Down)         | 0             |
| Index and Pinky Finger Up       | + (Addition)  |
| Thumb and Pinky Finger Up       | - (Subtraction)|
| Thumb and Ring Finger Up        | * (Multiplication) |
| Thumb and Ring Finger Down      | / (Division)  |
| Two Fingers Together (Index, Middle) | Equal (Calculate) |
| Index Finger Up                 | Clear (Reset) |

## HTML Interface

The interface includes a standard calculator layout with buttons for digits, operations, and the camera feed for gesture detection.

## License

This project is open-source and free to use

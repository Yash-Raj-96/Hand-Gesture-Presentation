# Hand Gesture Controlled Presentation

A touch-free presentation control system enabling slide navigation, annotation, and zoom using hand gestures detected via webcam. Ideal for education, corporate settings, and accessibility.

---

## 🔹 Description
A gesture-based presentation controller that allows users to control slide navigation, annotate, erase, and zoom using only hand gestures. Built using Python, OpenCV, NumPy, and MediaPipe, this tool improves user interaction and accessibility during presentations.

---

## 🔧 Features
- ⬇️ Slide navigation via thumb or pinky gestures
- ✏️ Annotation with index finger
- ❌ Erase drawings with 3-finger gesture
- 🔄 Zoom in and out with 4 and 5-finger gestures
- 🔹 Pointer control for highlighting content
- Real-time webcam-based gesture detection

---

## 📄 Technologies Used
- **Python**
- **OpenCV**: Real-time video processing
- **NumPy**: Coordinate transformations
- **MediaPipe**: Hand tracking and gesture recognition

---

## 🌐 Applications
- Smart classrooms & digital education
- Business meetings and conferences
- Public speaking and virtual events
- Assistive technology for accessibility
- Interactive kiosks and smart homes

---

## 📁 Project Structure
```
Hand-Gesture-Presentation/
├── HandTracker.py         # Hand detection and gesture logic
├── main.py                # Main application logic
├── Images/                # Slide images
├── README.md              # Project documentation
└── requirements.txt       # Dependencies
```

---

## 🔍 How It Works
- Uses MediaPipe to detect hand landmarks
- Maps specific gestures to actions:
  - **[1,0,0,0,0]** → Previous slide (thumb)
  - **[0,0,0,0,1]** → Next slide (pinky)
  - **[0,1,0,0,0]** → Draw annotation (index)
  - **[0,1,1,1,0]** → Erase last annotation
  - **[0,1,1,1,1]** → Zoom in
  - **[1,1,1,1,1]** → Zoom out/reset

---

## 📝 Installation
```bash
git clone https://github.com/Yash-Raj-96/Hand-Gesture-Presentation.git
cd Hand-Gesture-Presentation
pip install -r requirements.txt
```

---

## 🚀 Run the Project
```bash
python main.py
```

Make sure your webcam is connected and active.

---

## 📸 Preview

📢 Gesture Overview         
📄 Slide Navigation        
✏️ Drawing/Annotation
🔄 Zoom Gesture       


---

## 🚀 Author
Made with ❤️ by **Yash Raj**

---

## ✅ License
This project is open-source under the MIT License.

# 🎧 SoundGaze  

**SoundGaze** is an open-source system that enhances spatial audio by adjusting sound balance based on head movements using a webcam. It provides a more immersive and natural listening experience by dynamically shifting audio between left and right channels.  

## 📌 Table of Contents  

1. [System Requirements](https://github.com/jrodriiguezg/SoundGaze/tree/main?tab=readme-ov-file#-system-requirements)
2. [Installation](https://github.com/jrodriiguezg/SoundGaze/tree/main?tab=readme-ov-file#-installation)
   - [Dependencies](https://github.com/jrodriiguezg/SoundGaze/tree/main?tab=readme-ov-file#-dependencies) 
   - [Setup](https://github.com/jrodriiguezg/SoundGaze/tree/main?tab=readme-ov-file#%EF%B8%8F-setup) 
3. [Usage](https://github.com/jrodriiguezg/SoundGaze/tree/main?tab=readme-ov-file#-usage) 
   - [Get the Audio Sink ID](https://github.com/jrodriiguezg/SoundGaze/tree/main?tab=readme-ov-file#%EF%B8%8F-get-the-audio-sink-id)
   - [Set the Sink ID](https://github.com/jrodriiguezg/SoundGaze/tree/main?tab=readme-ov-file#-set-the-sink-id-in-soundgaze)
4. [Run the System](https://github.com/jrodriiguezg/SoundGaze/tree/main?tab=readme-ov-file#%EF%B8%8F-run-the-system)
 
 
 

---

## 🔧 System-Requirements  

To run **SoundGaze**, you need:  

- A **Linux-based system** with **PipeWire** and **PulseAudio**.  
- A **working webcam**.  
- Python **3.7** or later.  
- A modern CPU (real-time processing requires good performance).  
**!!!Tested only on Fedora 41!!!!**
---

## 📥 Installation  

### 📌 Dependencies  

Make sure you have the following packages installed:  

```bash
sudo dnf install python3 python3-pip cmake gcc-c++ make pipewire pulseaudio-utils
```
Clone the proyect 
```bash
git clone https://github.com/jrodriiguezg/SoundGaze.git && cd SoundGaze
```
Then, install the required Python libraries:
```bash 
pip install -r requirements.txt
```
⚠️ Note: dlib may require CMake and a C++ compiler:
```bash
sudo dnf install cmake g++ make
```
You also need the dlib facial landmark model (shape_predictor_68_face_landmarks.dat).
Download it here:

[🔗 Download Model](https://github.com/italojs/facial-landmarks-recognition/blob/master/shape_predictor_68_face_landmarks.dat)

## ⚙️ Setup

Ensure PipeWire and PulseAudio are running. Check their status with:
```bash
systemctl --user status pipewire
systemctl --user status pulseaudio
```
If they are not running, start them manually:
```bash
systemctl --user start pipewire
systemctl --user start pulseaudio
```
## 🎯 Usage
### 🎚️ Get the Audio Sink ID
SoundGaze controls audio balance by modifying the audio sink volume. To get your sink ID, run:
```bash
pactl list sinks | grep "Sink #"
```
The ID is a number like 52 or 53.

📌 Example output:
```bash
Sink #53
        State: RUNNING
```
Here, the sink ID is 53.

If multiple audio devices are connected, list them with:
```bash
pactl list short sinks
```
📌 Example output:
```bash
53  alsa_output.pci-0000_00_1b.0.analog-stereo
```
### 🛠 Set the Sink ID in SoundGaze

In the audio handling script (audio.py), locate the function:
```python
def get_current_audio_sink_id():
    return "52"  # Change this to your sink ID
```
Replace "52" with the correct sink ID for your system.
## ▶️ Run-the-System

To start head tracking and audio adjustment, run:
```bash
python3 soundgaze.py
```
The system will dynamically adjust sound balance based on your head movements.
The program will:
✔️ Open your webcam
✔️ Track head movements
✔️ Adjust audio balance dynamically

To stop the program, press Ctrl + C.

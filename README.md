# Emotion Recognition in Videos

Simple demo that analyzes a video feed and displays the detected emotion alongside a representative image.

- Main script: [main.py](main.py)
- Key symbols:
  - [`video_path`](main.py)
  - [`emotion_images`](main.py)
  - [`emotion_imgs`](main.py)
  - [`map_emotion`](main.py)

## Requirements

- Python 3.8+
- pip packages:
  - deepface
  - opencv-python
  - numpy

Install quickly:
```sh
pip install deepface opencv-python numpy
```

## Usage

1. Place your video file (default name: `Static.mp4`) and optional emotion images (`happy.jpg`, `sad.jpg`, `angry.jpg`, `surprise.jpg`, `neutral.jpg`) in the project root.
2. Run:
```sh
python main.py
```
3. Press `q` in the video window to quit.

## Configuration

- Edit [`video_path`](main.py) to point to another video file.
- Adjust mapping and thresholds in [`map_emotion`](main.py) to change how detected emotions are normalized and when the displayed emotion updates.

## Notes

- The script displays two windows: the video feed and an emotion display image.
- If an emotion image is missing the script shows a white placeholder.
- See [main.py](main.py) for implementation details.

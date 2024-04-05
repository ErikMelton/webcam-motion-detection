# Motion Detection and Recording

This project is a Python application that uses OpenCV to detect motion in a video feed and record the video when motion is detected.

## Requirements

- Python
- OpenCV

## Setup

1. Clone the repository.
2. Install the required packages using poetry:

```bash
poetry install
```

## How it works

The application starts a video feed from the default camera. It then continuously monitors the feed for any significant 
changes in the frames, which it interprets as motion.

When motion is detected, the application starts recording the video feed. The recording continues for a minimum duration
to ensure that all motion is captured. If motion continues beyond this minimum duration, the recording continues until 
the motion stops and records a buffer of the minimum duration at the end to ensure all motion is captured.

The recorded videos are saved in the `./recordings` directory with a timestamp in the filename.

## Configuration

The application has several configurable parameters:

- `FRAME_RATE`: The frame rate of the video feed. This should be set to the frame rate of the camera.
- `MINIMUM_RECORDING_DURATION_SECONDS`: The minimum duration for which the video is recorded after motion is detected.
- `GRACE_PERIOD_SECONDS`: A number of seconds after the camera starts before motion detection is enabled. This is useful 
to avoid recording the user setting up the camera, and to avoid the initial frame being interpreted as motion.

These parameters can be adjusted in `main.py`.

## License

This project is licensed under the terms of the MIT license.
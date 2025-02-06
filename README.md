# Hand Tracking with YOLOv8

This project implements real-time hand tracking using YOLOv8 and OpenCV in a Docker container.

## Prerequisites

- Docker installed on your system
- A webcam connected to your computer

## Building the Docker Image

To build the Docker image, run the following command in the project directory:

```bash
docker build -t hand-tracker .
```

## Running the Application

To run the hand tracking application with access to your webcam, use:

```bash
docker run --rm -it \
    --device=/dev/video0:/dev/video0 \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    hand-tracker
```

Note: On macOS, you'll need to install XQuartz and configure it to allow connections from network clients.

## Usage

- The application will open a window showing the webcam feed with hand detection
- Green boxes will be drawn around detected hands
- Press 'q' to quit the application

## Troubleshooting

If you encounter permission issues with the webcam or display, make sure to:

1. Grant necessary permissions to the webcam device
2. Allow Docker to access the X server (on Linux):
   ```bash
   xhost +local:docker
   ```

## Notes

- The application uses the YOLOv8 nano model by default
- Detection is optimized for real-time performance
- The model will download automatically on first run 
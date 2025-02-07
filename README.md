# Hand Tracking Virtual Boundary Detection

This project implements real-time hand tracking and virtual boundary detection using MediaPipe and OpenCV, optimized for macOS systems.

## Overview

The application uses your Mac's webcam to track hand movements and detect when they cross into a designated "danger zone". A visual warning system with striped patterns indicates when hands enter restricted areas.

## Features

- Real-time hand tracking with 21 points per hand
- Visual danger zone with dynamic striped pattern
- Automatic boundary violation detection
- Support for both built-in FaceTime camera and external webcams
- Visual feedback when hands cross the boundary

## Prerequisites

- macOS system
- Python 3.9 or higher
- Built-in FaceTime camera or external webcam
- Internet connection (for initial package downloads)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd [repository-name]
```

2. Make the setup script executable:
```bash
chmod +x setup_and_run.sh
```

3. Run the setup script:
```bash
./setup_and_run.sh
```

The script automatically:
- Creates a Python virtual environment
- Installs required dependencies
- Launches the application

## Usage

When you run the application:
1. A window opens showing your webcam feed
2. The right portion of the screen shows a striped "danger zone"
3. Hand movements are tracked with:
   - Green dots for joint positions
   - Red lines connecting the joints
4. The striped pattern becomes more visible when any hand joint enters the danger zone
5. Press 'q' to quit the application

## Technical Details

The application uses:
- MediaPipe for precise hand landmark detection
- OpenCV for video capture and visualization
- Custom boundary detection algorithm
- Dynamic visual feedback system

## Project Structure

.
├── hand_tracker.py      # Main application code
├── requirements.txt     # Python dependencies
├── setup_and_run.sh    # Setup and launch script
└── .gitignore          # Git ignore rules
```

## Troubleshooting

If you encounter issues:

1. Camera not opening:
   - Check if other applications can access your webcam
   - Close other applications that might be using the camera
   - The app will try alternative camera indices automatically

2. Performance issues:
   - Ensure good lighting conditions
   - Keep hands within camera view
   - Close resource-intensive applications

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

[Your chosen license]

## Acknowledgments

- MediaPipe team for the hand tracking solution
- OpenCV community for computer vision tools

## Notes

- The application uses the YOLOv8 nano model by default
- Detection is optimized for real-time performance
- The model will download automatically on first run 
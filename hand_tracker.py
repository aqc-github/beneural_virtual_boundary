import cv2
import mediapipe as mp
import sys
import numpy as np

def create_striped_overlay(width, height, boundary_x, stripe_width=10):
    """Create a striped overlay with parallel 45-degree lines in the danger zone"""
    overlay = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Only create stripes in the danger zone (right side of boundary)
    start_x = boundary_x
    
    # Calculate offset to ensure stripes vertically aligned
    for i in range(0, width, stripe_width):
        start_point = (start_x+i, 0)
        end_point = (start_x+i, height)
        
        # Only draw if the line intersects with the danger zone
        if start_point[0] < width or end_point[0] >= boundary_x:
            cv2.line(overlay,
                    (min(max(start_point[0], boundary_x), width), start_point[1]),
                    (min(max(end_point[0], boundary_x), width), end_point[1]),
                    (0, 0, 255),
                    2)
    
    return overlay

def draw_boundary_line(frame, boundary_x, is_violated=False):
    """Draw a translucent striped pattern and boundary line"""
    height, width = frame.shape[:2]
    
    # Create striped overlay
    overlay = create_striped_overlay(width, height, boundary_x)
    
    # Apply transparency - more opaque if violated
    alpha = 0.6 if is_violated else 0.3
    frame = cv2.addWeighted(overlay, alpha, frame, 1.0, 0)
    
    # Draw the boundary line
    cv2.line(frame, (boundary_x, 0), (boundary_x, height), (0, 0, 255), 2)
    
    return frame

def check_boundary_violation(hand_landmarks, frame_width, boundary_x):
    """Check if any hand landmark crosses the boundary"""
    if hand_landmarks:
        for landmark in hand_landmarks.landmark:
            # Convert normalized coordinates to pixel coordinates
            x = int(landmark.x * frame_width)
            if x > boundary_x:
                return True
    return False

def main():
    # Initialize MediaPipe Hands
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    )
    
    # For MacOS, we'll try both camera indices
    camera_index = 0  # FaceTime HD Camera
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("Could not open default camera, trying alternative...")
        camera_index = 1  # Try alternative camera
        cap = cv2.VideoCapture(camera_index)
        
    if not cap.isOpened():
        print("Error: Could not open any camera")
        sys.exit(1)

    print(f"Successfully opened camera at index {camera_index}")
    print("Starting hand tracking. Press 'q' to quit.")
    
    # Set camera properties for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # Get actual frame size
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    
    # Set boundary at 60% of the frame width
    boundary_x = int(frame_width * 0.6)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame")
            break
            
        # Flip the frame horizontally for a later selfie-view display
        frame = cv2.flip(frame, 1)
        
        # Convert BGR image to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame and detect hands
        results = hands.process(rgb_frame)
        
        # Reset violation flag for this frame
        current_violation = False
        
        # Draw hand landmarks if detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Check for boundary violation
                if check_boundary_violation(hand_landmarks, frame_width, boundary_x):
                    current_violation = True
                
                # Draw landmarks
                mp_draw.draw_landmarks(
                    frame, 
                    hand_landmarks, 
                    mp_hands.HAND_CONNECTIONS,
                    mp_draw.DrawingSpec(color=(0,255,0), thickness=2, circle_radius=2),
                    mp_draw.DrawingSpec(color=(0,0,255), thickness=2)
                )
        
        # Draw boundary line and danger zone with appropriate highlighting
        frame = draw_boundary_line(frame, boundary_x, current_violation)
        
        # Display the frame
        cv2.imshow('Hand Tracking', frame)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    hands.close()

if __name__ == '__main__':
    main() 
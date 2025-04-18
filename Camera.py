# TEST PLAN: USB Camera Verification on Jetson
# 1. Plug in your standard USB camera (disconnect iPhone).
# 2. Run: ls /dev/video*
#    - Confirm your camera appears (usually as /dev/video0).
# 3. Run: v4l2-ctl --list-devices
#    - Confirm your camera is listed and note its /dev/videoX node.
# 4. Check your user is in the video group: groups $USER
#    - If not, run: sudo usermod -aG video $USER (then log out/in).
# 5. Run the updated Camera.py: python Camera.py
#    - You should see a message that the USB camera opened successfully and a test image saved in static/images.
# 6. If you encounter issues, try a different index, check permissions, or ensure no other app is using the camera.

# TEST CODE: See the __main__ section below for a simple test that captures and saves an image from the USB camera.

import GlobalConstants as GC
import cv2
import time
import os

class Camera:
    def __init__(self, camera_index=0):
        self.numOfPhotos = 0
        self.camera_index = camera_index
        # Serial number logic removed for generic USB camera support

    def take_picture(self):
        # SBX-004: Added error handling for missing camera device
        print(f"Trying to open USB camera at index {self.camera_index} (V4L2 backend)...")
        camera = cv2.VideoCapture(self.camera_index, cv2.CAP_V4L2)
        if not camera.isOpened():
            print(f"Error: Failed to open camera at index {self.camera_index} using V4L2 backend. No camera device detected.")
            return None
        # Capture a single frame
        ret, frame = camera.read()
        if not ret:
            print("Error: Failed to capture image from camera.")
            camera.release()
            return None
        # Save the captured frame as an image in a cross-platform way
        images_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
        os.makedirs(images_dir, exist_ok=True)
        imageFileName = os.path.join(images_dir, f"USBImage{self.numOfPhotos}_{int(time.time())}.jpg")
        cv2.imwrite(imageFileName, frame)
        print(f"{imageFileName} captured and saved successfully from camera index {self.camera_index}")
        self.numOfPhotos += 1
        camera.release()
        return imageFileName

if __name__ == "__main__":
    # Only test the first camera (index 0) for USB camera verification
    camera = Camera(camera_index=0)
    result = camera.take_picture()
    if result:
        print(f"Test image saved: {result}")
    else:
        print("Camera test failed. See error messages above.")


import GlobalConstants as GC

# pip install opencv-python
import cv2

# pip install libusb1
# usb1 is Python wrapper for libusb, a C library that provides generic access to USB devices.
import usb1

import time

class Camera:

    def __init__(self):
        self.numOfPhotos = 0
        self.serialNumber = Camera.get_serial_number()


    def get_serial_number():
        # Initialize libusb context
        try:
            with usb1.USBContext() as context:
                # Open the iPhone 14 Pro Max Camera as USB device by Vendor ID and Product ID (Bus 002 Device 004: ID 05ac:12a8) found using 'lsusb' command
                handle = context.openByVendorIDAndProductID(0x05AC, 0x12A8)
                
                if handle is None:
                    print("Failed to open device")
                    return 1
                
                # Read the serial number string descriptor (usually index 3, but this may vary)
                serial_number_index = 3
                try:
                    serialNumber = handle.getASCIIStringDescriptor(serial_number_index)
                    return serialNumber
                except usb1.USBError as e:
                    print(f"Failed to read serial number: {e}")
                    return 1
                
        except usb1.USBError as e:
            print(f"Failed to initialize libusb: {e}")
            return 1


    def take_picture(self):
        # Open the camera (0 usually refers to the default camera)
        camera = cv2.VideoCapture(0)
        
        if not camera.isOpened():
            print("Failed to open camera")
            return

        # Capture a single frame
        ret, frame = camera.read()

        if not ret:
            print("Failed to capture image")
        
        # Save the captured frame as an image
        imageFileName = f"/Users/pluto/GitRepos/StrongBox/static/images/iPhoneImage{self.numOfPhotos}_{int(time.time())}.jpg"
        #imageFileName = f"/Users/pluto/GitRepos/StrongBox/static/images/iPhoneImage{self.numOfPhotos}_{int(time.time())}_{self.serialNumber}.jpg"
        cv2.imwrite(imageFileName, frame)
        print(f"{imageFileName} captured and saved successfully from camera serial #{self.serialNumber}")
        self.numOfPhotos = self.numOfPhotos + 1
        
        # Release the camera
        camera.release()
        return imageFileName


if __name__ == "__main__":
    cameras = []
    for i in range(GC.NUMBER_OF_CAMERAS):
        camera = Camera() 
        cameras.append(camera)
                  
    cameras[0].take_picture()
    cameras[0].take_picture()
    cameras[0].take_picture()
    cameras[1].take_picture()
    cameras[2].take_picture()
    cameras[3].take_picture()
    cameras[4].take_picture()
    cameras[5].take_picture()
    cameras[6].take_picture()
    cameras[7].take_picture()
    cameras[8].take_picture()
    cameras[9].take_picture()


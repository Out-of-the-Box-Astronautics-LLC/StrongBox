# pip install opencv-python
import cv2

# pip install libusb1
import usb1


class Camera:

    def __init__(self, serialNumber: str):
        self.numOfPhotos = 1

    def get_serial_number():
        # Initialize libusb context
        try:
            with usb1.USBContext() as context:
                # Open the iPhone 14 Pro Max Camera as USB device by Vendor ID and Product ID (Bus 002 Device 004: ID 05ac:12a8)
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

        if ret:
            # Save the captured frame as an image
            cv2.imwrite(f"iPhoneImage{self.numOfPhotos}.jpg", frame)
            print(f"Image #{self.numOfPhotos} captured and saved successfully")
            self.numOfPhotos = self.numOfPhotos + 1
        else:
            print("Failed to capture image")

        # Release the camera
        camera.release()

if __name__ == "__main__":
    cameraObj = Camera(Camera.get_serial_number())
    cameraObj.take_picture()
    cameraObj.take_picture()
    cameraObj.take_picture()


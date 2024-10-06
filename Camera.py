import cv2
import usb1

def camera_info():
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
                serial_number = handle.getASCIIStringDescriptor(serial_number_index)
                print(f"Serial Number: {serial_number}")
            except usb1.USBError as e:
                print(f"Failed to read serial number: {e}")
                return 1
            
    except usb1.USBError as e:
        print(f"Failed to initialize libusb: {e}")
        return 1

def take_picture():
    # Open the camera (0 usually refers to the default camera)
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        print("Failed to open camera")
        return

    # Capture a single frame
    ret, frame = camera.read()

    if ret:
        # Save the captured frame as an image
        cv2.imwrite("captured_image.jpg", frame)
        print("Image captured and saved successfully")
    else:
        print("Failed to capture image")

    # Release the camera
    camera.release()

if __name__ == "__main__":
    take_picture()
    camera_info()

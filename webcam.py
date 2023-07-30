import cv2

# Open the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened successfully
if not cap.isOpened():
    print("Failed to open the webcam")
else:
    # Read the first frame from the webcam
    ret, frame = cap.read()

    # Check the dimensions of the frame
    if ret:
        height, width, _ = frame.shape
        print("Webcam dimensions: {} x {}".format(width, height))
    else:
        print("Failed to read frame from the webcam")

# Release the webcam
cap.release()
cv2.destroyAllWindows()
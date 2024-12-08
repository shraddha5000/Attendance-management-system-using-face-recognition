import cv2
import os
import numpy as np
from PIL import Image

# Ensure Haar Cascade file is downloaded
cascade_path = 'haarcascade_frontalface_default.xml'
if not os.path.isfile(cascade_path):
    import urllib.request
    url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    urllib.request.urlretrieve(url, cascade_path)

# Initialize face recognizer and detector
recognizer = cv2.face.LBPHFaceRecognizer_create()  # Requires opencv-contrib-python
detector = cv2.CascadeClassifier(cascade_path)

# Function to get images and labels
def getImagesAndLabels(path):
    # Get paths of all files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    faceSamples = []
    Ids = []

    for imagePath in imagePaths:
        # Convert image to grayscale
        pilImage = Image.open(imagePath).convert('L')
        imageNp = np.array(pilImage, 'uint8')  # Convert PIL image to NumPy array

        # Extract the ID from the file name (assumes format: Name.ID.SampleNum.jpg)
        try:
            Id = int(os.path.split(imagePath)[-1].split(".")[1])
        except ValueError:
            print(f"Skipping invalid file: {imagePath}")
            continue

        # Detect faces in the image
        faces = detector.detectMultiScale(imageNp)
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)

    return faceSamples, Ids

# Prepare training data
if not os.path.exists("TrainingImageLabel"):
    os.makedirs("TrainingImageLabel")

faces, Ids = getImagesAndLabels('TrainingImage')

if faces and Ids:
    recognizer.train(faces, np.array(Ids))
    recognizer.save('TrainingImageLabel/trainer.yml')  # Save the trained model
    print("Training completed and model saved as 'TrainingImageLabel/trainer.yml'")
else:
    print("No training data found. Please ensure 'TrainingImage' contains valid images.")

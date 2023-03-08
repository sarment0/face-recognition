# First, you need to install the required libraries: requests, opencv-python-headless, and face_recognition.
# You can install face_recognition by running !pip install face_recognition

import os
import requests
import shutil
import cv2
import face_recognition

# Function to download images from a URL and save them locally
def download_images(url_list):
    
    for idx, url in enumerate(url_list):
        response = requests.get(url, stream=True)
        with open(f'image_{idx}.jpg', 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
        
    print('Images downloaded')
    
# Function to find faces in images and save them as thumbnail in a local folder
def identify_and_save_faces():
    
    # Global variables to keep track of the identified faces and their path location
    known_face_encodings = []
    known_face_paths = []

    for filename in os.listdir():
        if filename.endswith('.jpg'):
            
            img_path = os.path.abspath(filename)
            img = cv2.imread(img_path)

            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_img)
            face_encodings = face_recognition.face_encodings(rgb_img, face_locations)
            
            if face_encodings:
                # Save the face thumbnail in a local folder
                top, right, bottom, left = face_locations[0]
                name = f"{filename.split('.')[0]}_{top}_{right}_{bottom}_{left}"
                cv2.imwrite(f'faces/{name}.jpg', img[top:bottom, left:right])
                
                # Identify if it's the first time the face is found or make a new group if already identified
                face_found = False
                for i, encoding in enumerate(known_face_encodings):
                    match = face_recognition.compare_faces([encoding], face_encodings[0])
                    if match[0]:
                        face_found = True
                        shutil.move(img_path, known_face_paths[i])
                        break
                        
                if not face_found:
                    known_face_encodings.append(face_encodings[0])
                    known_face_paths.append(os.path.abspath(f"faces/{name}.jpg"))
                    os.makedirs(f"faces/Group{len(known_face_paths)}")
                    shutil.move(img_path, known_face_paths[-1])
                    
            else:
                # If no face is found just delete the image
                os.remove(img_path)

    print('Faces identified and saved')        
            

# Public repository urls where the script can get imagery, this is an example 
image_urls = [
    'https://www.publicdomainpictures.net/pictures/40000/nahled/plain-blue-background.jpg',
    'https://www.publicdomainpictures.net/pictures/200000/nahled/sunrise-over-istanbul.jpg',
    'https://www.publicdomainpictures.net/pictures/100000/nahled/tulips-in-bloom.jpg',
    'https://www.publicdomainpictures.net/pictures/320000/nahled/seagull.jpg', 
    'https://www.publicdomainpictures.net/pictures/310000/nahled/shark-swimming-underwater.jpg',
    'https://www.publicdomainpictures.net/pictures/190000/nahled/mountain-landscape.jpg',
    'https://www.publicdomainpictures.net/pictures/150000/nahled/red-car.jpg', 
    'https://www.publicdomainpictures.net/pictures/170000/nahled/macaw.jpg',
    'https://www.publicdomainpictures.net/pictures/10000/nahled/abstract-autumn-colors.jpg',
    'https://www.publicdomainpictures.net/pictures/220000/nahled/cutlery-classic-kitchen-knife.jpg'
]

# Download the images
download_images(image_urls)

# Identify the faces in the images and save them as a thumbnail 
identify_and_save_faces()

# Delete the original images
for filename in os.listdir():
    if filename.endswith('.jpg'):
        os.remove(filename)

print("Process Complete")        

import pyaudio
import wave
import cv2
import os
import pickle
import time
from scipy.io.wavfile import read
from IPython.display import Audio, display, clear_output

from random_word import RandomWords

# os.mkdir('testing/test1')

# exit()

from main_functions import *


import requests
import json


def sendPassword(pw):
##send password with twilio
    url = "https://us-central1-aiot-fit-xlab.cloudfunctions.net/sendsms "

    payload = json.dumps({
    "token": "GETYOUROWNTOKEN",
    "receiver": "13218775974", ##put own number here
    "message": "Thank You for registering! your password is " + pw
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)



def getKeyFromPassword(password_provided):
    # password_provided = "password" # This is input in the form of a string
    password = password_provided.encode() # Convert to type bytes
    salt = b'salt_' # CHANGE THIS - recommend using a key from os.urandom(16), must be of type bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password)) # Can only use kdf once
    return key




def genWords(n):
    words = []
    r = RandomWords()
    ##generate a random list of words
    for i in range(n):
        r.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb", minCorpusCount=1, maxCorpusCount=10, minDictionaryCount=1, maxDictionaryCount=10, minLength=5, maxLength=10)





def add_user():
    
    name = input("Enter Name:")

    #  # check for existing database
    # if os.path.exists('./face_database/embeddings.pickle'):
    #     with open('./face_database/embeddings.pickle', 'rb') as database:
    #         db = pickle.load(database)   
            
    #         if name in db or name == 'unknown':
    #             print("Name Already Exists! Try Another Name...")
    #             return
    # else:
    #     #if database not exists than creating new database
    #     db = {}
    
    # cap = cv2.VideoCapture(0)
    # cap.set(3, 640)
    # cap.set(4, 480)
    
    # #detecting only frontal face using haarcascade
    # face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_default.xml')
    
    # i = 3
    # face_found = False
    
    # while True:            
    #     _, frame = cap.read()
    #     frame = cv2.flip(frame, 1, 0)
            
    #     #time.sleep(1.0)
    #     cv2.putText(frame, 'Keep Your Face infront of Camera', (100, 200), cv2.FONT_HERSHEY_SIMPLEX, 
    #                 0.8, (255, 255, 255), 2)
        
    #     cv2.putText(frame, 'Starting', (260, 270), cv2.FONT_HERSHEY_SIMPLEX, 
    #                 0.8, (255, 255, 255), 2)
        
    #     cv2.putText(frame, str(i), (290, 330), cv2.FONT_HERSHEY_SIMPLEX, 
    #                 1.3, (255, 255, 255), 3)

    #     i-=1
                   
    #     cv2.imshow('frame', frame)
    #     cv2.waitKey(1000)
        
    #     if i < 0:
    #         break
            
    # start_time = time.time()        
    # img_path = './saved_image/1.jpg'

    # ## Face recognition 
    # while True:
    #     curr_time = time.time()
        
    #     _, frame = cap.read()
    #     frame = cv2.flip(frame, 1, 0)
    #     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
    #     face = face_cascade.detectMultiScale(gray, 1.3, 5)
        
    #     if len(face) == 1:
    #         for(x, y, w, h) in face:
    #             roi = frame[y-10:y+h+10, x-10:x+w+10]

    #             fh, fw = roi.shape[:2]

    #             #make sure the face roi is of required height and width
    #             if fh < 20 and fw < 20:
    #                 continue

    #             face_found = True
    #             #cv2.imwrite(img_path, roi)

    #             cv2.rectangle(frame, (x-10,y-10), (x+w+10, y+h+10), (255, 200, 200), 2)

         
    #     if curr_time - start_time >= 3:
    #         break
            
    #     cv2.imshow('frame', frame)
    #     cv2.waitKey(1)
            
    # cap.release()        
    # cv2.destroyAllWindows()

    
    # if face_found:
    #     img = cv2.resize(roi, (96, 96))

    #     db[name] = img_to_encoding(img)

    #     with open('./face_database/embeddings.pickle', "wb") as database:
    #         pickle.dump(db, database, protocol=pickle.HIGHEST_PROTOCOL)
    
    # elif len(face) > 1:
    #     print("More than one faces found. Try again...")
    #     return
    
    # else:
    #     print('There was no face found in the frame. Try again...')
    #     return
      
    # os.system('cls' if os.name == 'nt' else 'clear') 
    
    #Voice authentication
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 3
    
    source = "voice_database/" + name
    
   
    os.mkdir(source)

    for i in range(3):
        audio = pyaudio.PyAudio()

        if i == 0:
            j = 3
            while j>=0:
                time.sleep(1.0)
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Speak your name in {} seconds".format(j))
                j-=1

        elif i ==1:
            time.sleep(2.0)
            print("Speak your name one more time")
            time.sleep(0.8)
        
        else:
            time.sleep(2.0)
            print("Speak your name one last time")
            time.sleep(0.8)

        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

        print("recording...")
        frames = []

        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        # saving wav file of speaker
        waveFile = wave.open(source + '\\' + str((i+1)) + '.wav', 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()
        print("Done")
    
    
    rn = RandomWords()
    
    pw = rn.get_random_word(hasDictionaryDef="true", includePartOfSpeech="noun,verb", minCorpusCount=1, maxCorpusCount=10, minDictionaryCount=1, maxDictionaryCount=10, minLength=5, maxLength=10)
    
    text_file = open(name + ".pw", "w")
    n = text_file.write(pw)
    text_file.close()
    
    sendPassword(pw) ##send the password with twilio helper function hosted on GCP
    

    dest =  "gmm_models/"
    count = 1

    for path in os.listdir(source):
        path = os.path.join(source, path)

        features = np.array([])
        
        # reading audio files of speaker
        (sr, audio) = read(path)
        
        # extract 40 dimensional MFCC & delta MFCC features
        vector   = extract_features(audio,sr)

        if features.size == 0:
            features = vector
        else:
            features = np.vstack((features, vector))
            
        # when features of 3 files of speaker are concatenated, then do model training
        if count == 3:    
            gmm = GMM(n_components = 16, max_iter = 200, covariance_type='diag',n_init = 3)
            gmm.fit(features)

            # saving the trained gaussian model
            pickle.dump(gmm, open(dest + name + '.gmm', 'wb'))
            print(name + ' added successfully') 
            
            features = np.asarray(())
            count = 0
        count = count + 1

if __name__ == '__main__':
    add_user()

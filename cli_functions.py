import os
import glob
import json
import time
import requests
from os import path
import time
from datetime import datetime
from colorama import Fore,Style
import colorama
from numpy import double
from Backend.MainController import encryption
from Backend.MainController import decryption
from rich.table import Table
from rich.console import Console
import firebase_admin
from firebase_admin import credentials, storage
from PIL import Image
from io import BytesIO
import uuid
from firebase_admin import firestore
from fastapi import FastAPI
import blockchain
from pymongo import MongoClient
from fastapi.responses import HTMLResponse 
from fastapi.staticfiles import StaticFiles

blockChain = blockchain.Blockchain()


class MyDatabase:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://sanathamin28:sanath123@cluster0.uom0tz1.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['blockchain_db']
        self.mycol = self.db["website_db"]
  
    def update_one(self, webName, password):
        self.mycol.update_one({"webName": webName}, {"$set": {"password": password}})

    def insert_data(self, data):
        x = self.mycol.insert_one(data)
        return x.inserted_id
    def find(self, data):
        return list(self.mycol.find({"webName": data}))
class MyDatabase2:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://sanathamin28:sanath123@cluster0.uom0tz1.mongodb.net/?retryWrites=true&w=majority")
        self.db = self.client['blockchain_db']
        self.mycol = self.db["user_blocks"]
  

    def find(self, data):
        return list(self.mycol.find({"_id": data}))
    def insert_data(self, data):
        x = self.mycol.insert_one(data)
        return x.inserted_id    
status = ""
input_length = 0
cipher_length = 0
which_algo = -1
process_type = ""
elapsed_time = double(0.0)


def print_message(msg, msg_type,delay):
    '''General function to print info, Warning and error messages'''
    colorama.init(autoreset = True)
    msg_type.upper()
    current_datetime = str(datetime.now())

    if msg_type == "INFO":
            print(f'[{Fore.BLUE}{msg_type}{Fore.RESET}] {current_datetime} {Style.BRIGHT}{msg}')
            time.sleep(delay)
    elif msg_type == "WARNING":
        print(f'[{Fore.YELLOW}{msg_type}{Fore.RESET}] {Fore.YELLOW}{current_datetime} {Fore.YELLOW}{Style.BRIGHT}{msg}')
        time.sleep(delay)
    elif msg_type == "ERROR":
        print(f'[{Fore.RED}{msg_type}{Fore.RESET}] {Fore.RED}{current_datetime} {Fore.RED}{Style.BRIGHT}{msg}')
        time.sleep(delay)
    elif msg_type == "SUCCESS":
        msgtype = "INFO"
        print(f'[{Fore.BLUE}{msgtype}{Fore.RESET}]{Fore.RESET}--------------------------------------------------------------------------------------------------')
        print(f'[{Fore.BLUE}{msgtype}{Fore.RESET}] {Fore.GREEN}{current_datetime} {Fore.GREEN}{Style.BRIGHT}{msg}')
        print(f'[{Fore.BLUE}{msgtype}{Fore.RESET}]{Fore.RESET}--------------------------------------------------------------------------------------------------')

        time.sleep(delay)

app = FastAPI()
mydb = MyDatabase()
fetchDb = MyDatabase2()
pas = "x"
from starlette.responses import FileResponse

# # Mount the static files directory from Angular
# app.mount("/static", StaticFiles(directory="final-year-frontend-main"), name="static")

# # @app.get("/", response_class=HTMLResponse)
# # Serve the Angular index.html file
# @app.get("/")
# async def serve_index():
#     return FileResponse("final-year-frontend-main/index.html") 


# Serve static files (including index.html)
app.mount("/static", StaticFiles(directory="./"), name="static")

# Define the route for serving index.html
@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("./index.html") as f:
        return f.read()

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)
    
    
@app.post('/save')
async def SavePassword(data: dict):
    webName = data.get('webName')
    password = data.get('password')
    
    url = f_encrypt(password)
    id = blockChain.mine_block(url)
    mydata = {"webName":webName,
                  "password": id
                }
    result = mydb.find(webName)
    if len(result) == 0:
        mydb.insert_data(mydata)
    else:    
        mydb.update_one(webName, id)
    
    return {"ID": url}


@app.get('/getPassword')
def GetPassword(webName):
   
    result = mydb.find(webName)
    if len(result) == 0:
        return {"Error": "We don't have password for the requested Website"}
    response = result[0]
    id = response['password']
    URL = fetchDb.find(id)
    dataURL = URL[0]['data']
    response = requests.get(dataURL)
    downloadedImage = Image.open(BytesIO(response.content))
    downloadedImage.show()
    folder_path = r'C:\Users\Dell\Documents\Images_FYProject\FetchImg'
    filename = os.path.basename(dataURL)
    response = requests.get(dataURL) 

# Construct the file path where you want to save the image
    filename = os.path.basename(dataURL)
    file_path = os.path.join(folder_path, filename)

# Save the image to the file path
    with open(file_path, "wb") as f:
        f.write(response.content)
        files = os.listdir(folder_path)

# Filter the list to only include image files (e.g. PNG, JPG)
    image_files = glob.glob(os.path.join(folder_path, '*.png'))

# Sort the list of image files by modification time in descending order
    image_files = sorted(image_files, key=os.path.getmtime, reverse=True)
    path = image_files[0]
# Get the path of the most recently modified image file
    password = f_decrypt(path)
    print("From api ", password)

    return {"Password":password}

@app.get('/')
def IsMyPasswordSafe():
    result = blockChain.is_chain_valid()
    if result:
        return {"Result": "Yes it is safe"}
    else:
        return {"Result": "Password is not safe"} 

def f_encrypt(plain_text):
  
    # global plain_text
    # print("Your Plain text:")
    # plain_text = str(input(f'{Fore.LIGHTCYAN_EX}'))
   
    global input_length
    input_length = len(plain_text)
    global cipher_length
    global which_algo
    global process_type
    global elapsed_time
    global status
    process_type = "Encryption"
    
    status,cipher_length,which_algo,image,elapsed_time = encryption(plain_text)
    
    cred = credentials.Certificate("techiebuddy-6b2c0-firebase-adminsdk-xw1xy-e0ce9fcbf4.json")
    firebase_admin.initialize_app(cred, {'storageBucket':'techiebuddy-6b2c0.appspot.com'})
    db = firestore.client()
    # bucket = storage.Bucket()
    print(save_image(image))
    folder_path = r'C:\Users\Dell\Documents\Images_FYProject\savedImg'
    files = os.listdir(folder_path)

# Filter the list to only include image files (e.g. PNG, JPG)
    image_files = [f for f in files if f.endswith('.png') or f.endswith('.jpg')]

# Sort the list by modification time (most recent first)
    image_files.sort(key=lambda f: os.path.getmtime(os.path.join(folder_path, f)), reverse=True)
    
    name = image_files[0]
    bucket = storage.bucket()
    blob = bucket.blob(name)
    url = 'C:/Users/Dell/Documents/Images_FYProject/savedImg'
    file_path = os.path.join(url, name)
    blob.upload_from_filename(file_path)
    blob.make_public()
    
    public_url = blob.public_url
    
    print("")  
    #print("timeout")
    # response = requests.get(public_url)
    # downloadedImage = Image.open(BytesIO(response.content))
    # downloadedImage.show()
    return public_url
    
def save_image(image):
    
    
    filename = str(uuid.uuid4()) + '.png'
    filepath = os.path.join(r'C:\Users\Dell\Documents\Images_FYProject\savedImg', filename)
    with open(filepath, 'wb') as f:
        image.save(f) # save image to file
    return filepath


def f_decrypt(paths):
    '''Decrypt the given imaage, and extract the plain text from the cipher text'''
    global status
    global cipher_length
    global which_algo
    global elapsed_time
    global process_type
    process_type = "Decryption"

    
    inp_path = str(paths)
    
    if path.exists(inp_path):
        if path.isfile(inp_path):
            status,cipher_length,which_algo,message,elapsed_time= decryption(inp_path)
            print(message, type(message))
            return message

def init():
    f_encrypt()

# def upload_image_to_firebase(image):
#     print("Upload image to firebase got called\n")
#     # Get a reference to the Firebase storage bucket
#     bucket = storage.bucket()

#     # Upload the image to Firebase storage bucket
#     blob = bucket.blob('encrypted_image.png')
#     blob.upload_from_file(image)

#     # Get the public URL of the uploaded image
#     url = blob.public_url

#     return url    

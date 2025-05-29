from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import io
from tensorflow.keras.models import load_model

# Load model and constants
model = load_model('captcha_solver_alphanum.h5')

PADDING_CHAR = '_'
ALPHANUM_CHARS = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' + PADDING_CHAR
CHAR_TO_INDEX = {char: i for i, char in enumerate(ALPHANUM_CHARS)}
INDEX_TO_CHAR = {i: char for char, i in CHAR_TO_INDEX.items()}
MAX_LEN = 9

app = FastAPI()

def preprocess_image_file(file) -> np.ndarray:
    img = Image.open(file).convert('RGB')
    img = img.resize((64, 64))
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

def decode_prediction(prediction):
    predicted_label = ""
    for i in range(len(prediction)):
        char_index = np.argmax(prediction[i])
        predicted_label += INDEX_TO_CHAR[char_index]
    return predicted_label.strip(PADDING_CHAR)

@app.post("/solve-captcha/")
async def solve_captcha(file: UploadFile = File(...)):
    image_bytes = await file.read()
    img = io.BytesIO(image_bytes)
    X_test = preprocess_image_file(img)
    predictions = model.predict(X_test)
    captcha_text = decode_prediction(predictions)
    return JSONResponse(content={"captcha": captcha_text})
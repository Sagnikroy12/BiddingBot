from fastapi import FastAPI
from pydantic import BaseModel
import base64
import numpy as np
import cv2
import tensorflow as tf

model = tf.keras.models.load_model("captcha_model.h5")

app = FastAPI()

class CaptchaRequest(BaseModel):
    image_base64: str

@app.post("/solve")
def solve_captcha(req: CaptchaRequest):
    img_data = base64.b64decode(req.image_base64)
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (64, 64)).reshape(1, 64, 64, 1) / 255.0

    preds = model.predict(img)
    digits = [str(np.argmax(p)) for p in preds]
    return {"prediction": ''.join(digits)}

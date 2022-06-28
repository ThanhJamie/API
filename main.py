from fastapi import FastAPI, File, UploadFile, Request
from starlette.responses import StreamingResponse
import io
import cv2
import numpy as np
import use_model_class as model
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates/")
app = FastAPI()

@app.get("/")
async def welcome(request: Request):
    return templates.TemplateResponse('appear.html', context={'request': request})

@app.post("/image")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    im_jpg = model.response(frame)
    return StreamingResponse(io.BytesIO(im_jpg.tobytes()), media_type="image/jpg")

async def generate(camera):
    while (True):
        success, frame = camera.read()
        if not success:
            break
        else:
            buffer = model.response(frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.get("/camera") #post
async def request_cam():
    camera = cv2.VideoCapture(0)
    return StreamingResponse(generate(camera), media_type="multipart/x-mixed-replace;boundary=frame")
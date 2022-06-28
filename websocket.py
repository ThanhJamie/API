from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import cv2
import numpy as np
import websockets
from fastapi.responses import StreamingResponse
import uvicorn
import use_model_class as reponse

app = FastAPI()

async def generate(camera):
    while (True):
        success, frame = camera.read()
        if not success:
            break
        else:
            frame = reponse.image(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.get("/camera") #post
async def request_cam():
    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    return StreamingResponse(generate(camera), media_type="multipart/x-mixed-replace;boundary=frame")

#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000, access_log=False)

'''
@app.websocket("/recieve_stream")
async def websocket_endpoint(websocket: WebSocket):
    # listen for connections
    await websocket.accept()
    #count = 1
    try:
        while True:
            contents = await websocket.receive_bytes()
            arr = np.frombuffer(contents, np.uint8)
            frame = cv2.imdecode(arr, cv2.IMREAD_UNCHANGED)
            cv2.imshow('frame', frame)
            cv2.waitKey(1)
            #cv2.imwrite("frame%d.png" % count, frame)
            #count += 1
    except WebSocketDisconnect:
        cv2.destroyWindow("frame")
        print("Client disconnected")
'''


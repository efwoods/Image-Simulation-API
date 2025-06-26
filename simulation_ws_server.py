import asyncio
import base64
import json
import websockets
import torch
from PIL import Image
from io import BytesIO
from models.image_encoder import ImageEncoder
from models.waveform_decoder import WaveformDecoder
import websocket

device = "cuda" if torch.cuda.is_available() else "cpu"

# Load pretrained models
image_encoder = ImageEncoder().to(device).eval()
waveform_decoder = WaveformDecoder().to(device).eval()


async def process_image(image_data):
    async for message in websocket:
        data = json.loads(message)
        session_id = data.get("session_id")
        image_b64 = data.get("image_base64")

        # Decode the base64 image data
        image = Image.open(BytesIO(base64.b64decode(image_b64.split(",")[1]))).convert(
            "RGB"
        )
        image_tensor = (
            torch.tensor(np.array(image)).permute(2, 0, 1).unsqueeze(0).float() / 255.0
        )
        image_tensor = image_tensor.to(device)

        with torch.no_grad():
            image_embedding = image_encoder(image_tensor)
            waveform_latent = waveform_decoder(image_embedding).squeeze().cpu().tolist()

        # Send latent to relay
        await websocket.send(
            json.dumps(
                {
                    "type": "waveform_latent",
                    "session_id": session_id,
                    "payload": waveform_latent,
                }
            )
        )


start_server = websockets.serve(process_image, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

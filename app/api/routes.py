# api/routes.py

from fastapi import APIRouter
from fastapi import WebSocket, WebSocketDisconnect
from core.monitoring import metrics
from core.config import settings
from core.logging import logger
import json

import websockets

from core.config import settings

from service.transform import (
    preprocess_image_from_websocket,
    transform_image_to_waveform_latents,
)

router = APIRouter()


@router.websocket("/ws/simulate-image-to-waveform-latent")
async def simulate(websocket: WebSocket):
    await websocket.accept()

    try:
        async for message in websocket:
            image_tensor, request = preprocess_image_from_websocket(message)
            waveform_latent = transform_image_to_waveform_latents(image_tensor)

            payload = {
                "type": "waveform_latent",
                "session_id": request.get("session_id", "anonymous"),
                "payload": waveform_latent.squeeze().cpu().tolist(),
            }

            # Forward to latents to relay
            async with websockets.connect(settings.RELAY_URI) as relay_ws:
                await relay_ws.send(json.dumps(payload))

            # Optional: Send response back to client
            await websocket.send_json(
                {"status": "success", "latents": payload["payload"]}
            )
            metrics.visual_thoughts_simulated.inc()

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected.")
    except Exception as e:
        print(f"Error: {e}")
        metrics.websocket_errors.inc()


@router.get("/ws-info", tags=["Simulate"])
async def websocket_info():
    return {
        "endpoint": "/simulate/ws/simulate-image-to-waveform-latent",
        "full_url": "ws://localhost:8000/image-simulation-to-synthetic-waveform-api/simulate/ws/simulate-image-to-waveform-latent",
        "protocol": "WebSocket",
        "description": "Real-time simulation of image → synthetic waveform → waveform latent.",
        "input_format": {
            "type": "simulate",
            "session_id": "string (optional)",
            "image_base64": "data:image/png;base64,...",
        },
        "output_format": {
            "type": "waveform_latent",
            "session_id": "copied from input",
            "payload": "[float list representing latent]",
        },
    }

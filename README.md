# Image-Simulation-API

This is a websocket server that will process any image into a neural-waveform latent space.

## Data Flow Diagram

```
     (Train Phase)
   ┌──────────────┐
   │  Image Input │
   └──────┬───────┘
          ▼
  ┌─────────────────┐
  │  Image Encoder  │  (ResNet / ViT)
  └─────────────────┘
          ▼
    image_latent_space ───┐
                          ▼
              ┌────────────────────┐
              │  Waveform Decoder  │ (MLP or 1D CNN)
              └────────────────────┘
                          ▼
                 Synthetic Waveform
                          ▼
              ┌────────────────────┐
              │  Waveform Encoder  │
              └────────────────────┘
                          ▼
    waveform_latent ◄────── latent alignment loss ──────► image_latent_space
                          ▼
              ┌──────────────────┐
              │  Image Decoder   │
              └──────────────────┘
                          ▼
               Reconstructed Image
```

The simulation path may accept a real waveform or a synthetic waveform.
The Image encoder, waveform decoder, waveform encoder, and image decoder are all individual modular models. 

```
Simulation Path (How to See) (websocket api)
Image ─▶ Image Encoder ─▶ image_latent_space ─▶ Waveform Decoder ─▶ Synthetic (or real) Waveform ─▶ Waveform Encoder ─▶ (waveform_latent)

OR

Synthetic (or real) Waveform ─▶ Waveform Encoder ─▶ (waveform_latent)

```

```
Reconstruction Path (How to Visualize Sight, Imagination, and Dreams) (relay api)
 waveform_latent ─▶ Image Decoder ─▶ Reconstructed Image
```

## Full-Stack Project Architecture
```
[Simulation API: WebSocket Server]
┌─────────────────────────────┐
│ Accept a random image       │
│ └── image_encoder → latents │
│     └── waveform_decoder    │
│         └── Send to Relay   │
└─────────────────────────────┘

[Relay API: WebSocket Server]
┌────────────────────────────────┐
│ Receive waveform_latent        │
│ └── waveform_encoder → latents │
│     └── image_decoder          │
│         └── Buffer image       │
│             └── Respond        │
└────────────────────────────────┘

[Frontend: React]
┌───────────────────────────┐
│ Thought-to-Image button   │
│ └── Poll Relay API WS     │
│     └── Receive image     │
│         └── Display       │
└───────────────────────────┘

```

## Full-Stack Development Time:
```
| Task                                    | Time Estimate   |
| --------------------------------------- | --------------- |
| ✅ Webcam capture & preprocessing        | 0.5 hour        |
| ✅ Integrate image encoder model         | 0.5 hour        |
| ✅ Generate waveform latent              | 0.5 hour        |
| ✅ Send waveform to relay via WebSocket  | 0.5 hour        |
| ✅ Relay receives, decodes image         | 1.5 hours       |
| ✅ Frontend polling WebSocket + image UI | 1.5 hours       |
| ✅ Testing + debugging                   | 1.5 hours       |
| **Total**                               | **\~7.5 hours** |
```

## Simulation -> Relay Message Format
```
{
  "type": "waveform_latent",
  "session_id": "xyz123",
  "payload": [0.023, 0.55, ..., -0.011]  // z_waveform_latent vector
}
```

## Relay -> Simulation Message Format
```
{
  "type": "reconstructed_image",
  "session_id": "xyz123",
  "image_base64": "data:image/jpeg;base64,/9j/4AAQSk..."
}
```

from pydantic_settings import BaseSettings

import torch


class Settings(BaseSettings):
    # Ngrok / WebSocket
    RELAY_URI: str

    # Torch
    DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"

    # Models
    NORMALIZATION_CONFIG: str
    IMAGE_ENCODER_PATH: str
    WAVEFORM_ENCODER_PATH: str
    WAVEFORM_DECODER_PATH: str
    RESIZED_IMAGE_SIZE: int
    LATENT_DIM: int

    class Config:
        env_file = ".env"


settings = Settings()

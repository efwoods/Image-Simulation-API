from pydantic_settings import BaseSettings
import torch
from typing import Optional


class Settings(BaseSettings):
    # Torch
    DEVICE: str = "cuda" if torch.cuda.is_available() else "cpu"

    # Models
    NORMALIZATION_CONFIG: str
    IMAGE_ENCODER_PATH: str
    WAVEFORM_ENCODER_PATH: str
    WAVEFORM_DECODER_PATH: str
    RESIZED_IMAGE_SIZE: int
    LATENT_DIM: int

    # GITHUB NGROK CONFIG
    GITHUB_TOKEN: str
    GITHUB_GIST_ID: str

    NGROK_URL: Optional[str] = None

    @property
    def GIST_API_URL(self) -> str:
        return f"https://api.github.com/gists/{self.GITHUB_GIST_ID}"

    @property
    def RELAY_URI(self) -> str:
        return self.NGROK_URL + "/relay-waveform-latent-to-image-reconstruction-api"

    class Config:
        env_file = ".env"


settings = Settings()

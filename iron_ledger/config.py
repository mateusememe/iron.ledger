import os
from dataclasses import dataclass
from dotenv import load_dotenv
from iron_ledger.exceptions import ConfigError

@dataclass
class Config:
    hevy_api_key: str

def load_config() -> Config:
    load_dotenv()
    
    api_key = os.getenv("HEVY_API_KEY")
    if not api_key:
        raise ConfigError("HEVY_API_KEY environment variable is required")
        
    return Config(hevy_api_key=api_key)

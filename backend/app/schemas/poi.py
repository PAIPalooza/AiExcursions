from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator, ConfigDict, Field

class POIBase(BaseModel):
    """Base POI schema."""
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    audio_url: Optional[str] = Field(None, max_length=512)

    @field_validator('audio_url')
    @classmethod
    def validate_audio_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate audio URL format."""
        if v is None:
            return v
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Audio URL must be a valid HTTP(S) URL')
        return v

    model_config = ConfigDict(from_attributes=True)

class POICreate(POIBase):
    """POI creation schema."""
    pass

class POIUpdate(BaseModel):
    """POI update schema."""
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    audio_url: Optional[str] = Field(None, max_length=512)

    @field_validator('audio_url')
    @classmethod
    def validate_audio_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate audio URL format."""
        if v is None:
            return v
        if not v.startswith(('http://', 'https://')):
            raise ValueError('Audio URL must be a valid HTTP(S) URL')
        return v

    model_config = ConfigDict(from_attributes=True)

class POIInDB(POIBase):
    """POI database schema."""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

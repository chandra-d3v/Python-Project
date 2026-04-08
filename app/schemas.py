from pydantic import BaseModel, ConfigDict, Field, field_validator


class AddressBase(BaseModel):
    label: str = Field(..., min_length=1, max_length=120, examples=["Home"])
    street: str | None = Field(default=None, max_length=255, examples=["221B Baker Street"])
    city: str | None = Field(default=None, max_length=120, examples=["London"])
    state: str | None = Field(default=None, max_length=120, examples=["Greater London"])
    postal_code: str | None = Field(default=None, max_length=20, examples=["NW1"])
    country: str | None = Field(default=None, max_length=120, examples=["United Kingdom"])
    latitude: float = Field(..., ge=-90, le=90, examples=[51.523767])
    longitude: float = Field(..., ge=-180, le=180, examples=[-0.1585557])

    @field_validator("label")
    @classmethod
    def validate_label(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("label must not be blank")
        return cleaned


class AddressCreate(AddressBase):
    pass


class AddressUpdate(BaseModel):
    label: str | None = Field(default=None, min_length=1, max_length=120)
    street: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, max_length=120)
    state: str | None = Field(default=None, max_length=120)
    postal_code: str | None = Field(default=None, max_length=20)
    country: str | None = Field(default=None, max_length=120)
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)

    @field_validator("label")
    @classmethod
    def validate_optional_label(cls, value: str | None) -> str | None:
        if value is None:
            return value
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("label must not be blank")
        return cleaned


class AddressRead(AddressBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class NearbyAddress(AddressRead):
    distance_km: float = Field(..., examples=[2.37])


class NearbySearchParams(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    distance_km: float = Field(..., gt=0, le=20000, examples=[5])

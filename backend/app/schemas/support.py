from pydantic import BaseModel, EmailStr, field_validator


class SupportMessageCreate(BaseModel):
    name: str
    email: EmailStr
    message: str

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("name cannot be blank")
        return v

    @field_validator("message")
    @classmethod
    def message_length(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 10:
            raise ValueError("message must be at least 10 characters")
        if len(v) > 4000:
            raise ValueError("message must be at most 4000 characters")
        return v


class SupportMessageResponse(BaseModel):
    message: str

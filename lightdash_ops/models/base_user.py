from pydantic import BaseModel, EmailStr, Field


class LightdashUser(BaseModel):
    """Information about a Lightdash user"""
    email: EmailStr = Field(description='Member email')
    uuid: str = Field(description='Member UUID', default=None)

    def __hash__(self):
        return hash(self.email)

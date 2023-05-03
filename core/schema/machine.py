from pydantic import BaseModel


class TextSchema(BaseModel):
    review: str

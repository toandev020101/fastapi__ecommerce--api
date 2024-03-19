from typing import List

from pydantic import BaseModel


class RemoveSchema(BaseModel):
    ids: List[int]
from pydantic import BaseModel, ConfigDict

# схема для создания продукта
class EpisodesCreate(BaseModel):
    tags: str
    name: str 
    preview: str
    content: str

class EpisodesPydantic(BaseModel):
    id: int
    tags: str
    name: str 
    preview: str
    content: str

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
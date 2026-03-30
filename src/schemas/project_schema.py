from pydantic import BaseModel,Field  


class ProjectCreate(BaseModel):
    key: str = Field(..., max_length=10, description="Unique key for the project")
    name: str = Field(..., max_length=255, description="Name of the project")
    description: str = Field(None, description="Description of the project")
    owner_id: int = Field(None, description="ID of the user who owns the project")

 
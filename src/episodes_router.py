from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from .episodes_models import Episodes
from .episodes_shema import EpisodesCreate, EpisodesPydantic
from .db import get_session

app = APIRouter(prefix="/episodes", tags=["Episodes"])

templates = Jinja2Templates(directory="src/templates")
app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.post("/", status_code=201)
async def add_episode(episode_create: EpisodesCreate, session: AsyncSession = Depends(get_session)):
    episode = Episodes(
        name=episode_create.name,
        tags=episode_create.tags,
        preview=episode_create.preview,
        content=episode_create.content
    )
    session.add(episode)
    try:
        await session.commit()
        await session.refresh(episode)
    except Exception as e:
        await session.rollback()
        raise e
    return {"message": "Episode added successfully"}


@app.get("/episodes/{id}", response_model=EpisodesPydantic, response_class=HTMLResponse)
async def get_episodes(request: Request, id: int, session: AsyncSession = Depends(get_session)):
    episodes = await session.scalar(select(Episodes).filter(Episodes.id == id))
    tags = episodes.tags
    name = episodes.name
    preview = episodes.preview
    content = episodes.content
    context = {
        "request": request,
        "title": name,
        "id": id,
        "tags": tags,
        "preview": preview,
        "content": content
    }
    return templates.TemplateResponse("templates/index.html", context=context)
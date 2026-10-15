import secrets
import string
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy import func, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .db import get_db
from .models import Click, Link
from .schemas import DailyClicks, LinkCreate, LinkOut, LinkStats

ALPHABET = string.ascii_letters + string.digits
MAX_CODE_ATTEMPTS = 5

DbSession = Annotated[Session, Depends(get_db)]

health_router = APIRouter(tags=["health"])
links_router = APIRouter(prefix="/links", tags=["links"])
redirect_router = APIRouter(tags=["redirect"])


def generate_code(length: int) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))


@health_router.get("/healthz")
def healthz() -> dict[str, str]:
    """Liveness: the process is up. Deliberately does not touch the database."""
    return {"status": "ok"}


@health_router.get("/readyz")
def readyz(db: DbSession) -> dict[str, str]:
    """Readiness: the app can reach its database."""
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "database unavailable") from exc
    return {"status": "ready"}


@links_router.post("", response_model=LinkOut, status_code=status.HTTP_201_CREATED)
def create_link(payload: LinkCreate, request: Request, db: DbSession) -> LinkOut:
    settings = request.app.state.settings
    target = str(payload.target_url)
    for _ in range(MAX_CODE_ATTEMPTS):
        link = Link(code=generate_code(settings.code_length), target_url=target)
        db.add(link)
        try:
            db.commit()
        except IntegrityError:  # code collision: try another one
            db.rollback()
            continue
        return LinkOut(
            code=link.code,
            short_url=f"{settings.base_url.rstrip('/')}/{link.code}",
            target_url=link.target_url,
        )
    raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "could not allocate a short code")


@links_router.get("/{code}/stats", response_model=LinkStats)
def link_stats(code: str, db: DbSession) -> LinkStats:
    link = db.scalar(select(Link).where(Link.code == code))
    if link is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "link not found")
    day = func.date(Click.clicked_at)
    rows = db.execute(
        select(day, func.count(Click.id))
        .where(Click.link_id == link.id)
        .group_by(day)
        .order_by(day)
    ).all()
    daily = [DailyClicks(date=d, clicks=n) for d, n in rows]
    return LinkStats(
        code=link.code,
        target_url=link.target_url,
        total_clicks=sum(d.clicks for d in daily),
        daily=daily,
    )


@redirect_router.get("/{code}")
def follow_link(code: str, db: DbSession) -> RedirectResponse:
    link = db.scalar(select(Link).where(Link.code == code))
    if link is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "link not found")
    db.add(Click(link_id=link.id))
    db.commit()
    return RedirectResponse(link.target_url, status_code=status.HTTP_302_FOUND)

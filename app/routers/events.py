from datetime import datetime
from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from app.models.event import Event
from app.models.user import User
from app.models.registration import Registration
from app.data.db import SessionDep
from app.schemas import EventInput  # importiamo lo schema di validazione
from app.schemas import UserInput

router = APIRouter()

@router.get("/events")
def get_events(session: SessionDep):
    """Restituisce la lista di tutti gli eventi."""
    # prendiamo tutti gli eventi dal database
    events = session.exec(select(Event)).all()
    return events


@router.post("/events")
def create_event(event: EventInput, session: SessionDep):
    """Crea un nuovo evento nel database."""
    new_event = Event(
        title=event.title,
        description=event.description,
        date=event.date,
        location=event.location
    )
    session.add(new_event)
    session.commit()
    session.refresh(new_event)
    return new_event

  


@router.get("/events/{id}")
def get_event(id: int, session: SessionDep):
    """Restituisce un singolo evento tramite il suo id."""
    # cerchiamo l'evento con quell'id
    event = session.get(Event, id)
    if not event:
        # se non esiste, restituiamo errore 404
        raise HTTPException(status_code=404, detail="Evento non trovato")
    return event


@router.put("/events/{id}")
def update_event(id: int, updated_event: EventInput, session: SessionDep):
    """Aggiorna un evento esistente."""
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    event.title = updated_event.title
    event.description = updated_event.description
    event.date = updated_event.date
    event.location = updated_event.location
    session.commit()
    session.refresh(event)
    return event

@router.post("/events/{id}/register")
def register_to_event(id: int, user: UserInput, session: SessionDep):
    """Registra un utente a un evento. Se l'utente non esiste, lo crea."""
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    existing_user = session.get(User, user.username)
    if not existing_user:
        new_user = User(username=user.username, name=user.name, email=user.email)
        session.add(new_user)
        session.commit()
    # gestiamo la registrazione duplicata senza errore 500
    existing_reg = session.get(Registration, (user.username, id))
    if existing_reg:
        return {"message": "Utente già registrato"}
    registration = Registration(username=user.username, event_id=id)
    session.add(registration)
    session.commit()
    return {"message": "Registrazione avvenuta con successo"}


@router.delete("/events")
def delete_all_events(session: SessionDep):
    """(Opzionale) Elimina tutti gli eventi dal database."""
    events = session.exec(select(Event)).all()
    for event in events:
        session.delete(event)
    session.commit()
    return {"message": "Tutti gli eventi eliminati"}


@router.delete("/events/{id}")
def delete_event(id: int, session: SessionDep):
    """(Opzionale) Elimina un evento e tutte le sue registrazioni."""
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    # eliminiamo prima le registrazioni associate all'evento
    registrations = session.exec(select(Registration).where(Registration.event_id == id)).all()
    for reg in registrations:
        session.delete(reg)
    # poi eliminiamo l'evento
    session.delete(event)
    session.commit()
    return {"message": "Evento eliminato"}
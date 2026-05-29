from fastapi import APIRouter, HTTPException, Depends  # strumenti FastAPI per creare le API
from sqlmodel import Session, select  # strumenti per interrogare il database
from app.models.event import Event  # il modello Event che abbiamo creato
from app.models.user import User  # il modello User che abbiamo creato
from app.models.registration import Registration  # il modello Registration già esistente
from app.data.db import SessionDep  # la connessione al database
from datetime import datetime
# creiamo il router: è come un "blocco" che raggruppa tutte le API degli eventi
router = APIRouter()


@router.get("/events")
def get_events(session: SessionDep):
    """Restituisce la lista di tutti gli eventi."""
    # prendiamo tutti gli eventi dal database
    events = session.exec(select(Event)).all()
    return events


@router.post("/events")
def create_event(event: Event, session: SessionDep):
    """Crea un nuovo evento nel database."""
    # creiamo un nuovo oggetto Event con i dati ricevuti
    # convertiamo la data da stringa a datetime se necessario
    if isinstance(event.date, str):
        event.date = datetime.fromisoformat(event.date)
    # creiamo un oggetto nuovo per evitare problemi con la sessione
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
def update_event(id: int, updated_event: Event, session: SessionDep):
    """Aggiorna un evento esistente."""
    # cerchiamo l'evento da aggiornare
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    # aggiorniamo i campi con i nuovi valori
    event.title = updated_event.title
    event.description = updated_event.description
    event.date = updated_event.date
    event.location = updated_event.location
    session.commit()
    session.refresh(event)
    return event


@router.post("/events/{id}/register")
def register_to_event(id: int, user: User, session: SessionDep):
    """Registra un utente a un evento. Se l'utente non esiste, lo crea."""
    # verifichiamo che l'evento esista
    event = session.get(Event, id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    # se l'utente non esiste nel database, lo creiamo
    existing_user = session.get(User, user.username)
    if not existing_user:
        session.add(user)
        session.commit()
    # creiamo la registrazione che collega utente ed evento
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
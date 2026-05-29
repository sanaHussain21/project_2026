from fastapi import APIRouter, HTTPException  # strumenti FastAPI per creare le API
from sqlmodel import select  # strumento per interrogare il database
from app.models.registration import Registration  # il modello Registration
from app.models.user import User  # serve per verificare che l'utente esista
from app.models.event import Event  # serve per verificare che l'evento esista
from app.data.db import SessionDep  # la connessione al database

# creiamo il router che raggruppa tutte le API delle registrazioni
router = APIRouter()


@router.get("/registrations")
def get_registrations(session: SessionDep):
    """Restituisce la lista di tutte le registrazioni."""
    # prendiamo tutte le registrazioni dal database
    registrations = session.exec(select(Registration)).all()
    return registrations


@router.delete("/registrations")
def delete_registration(username: str, event_id: int, session: SessionDep):
    """(Opzionale) Elimina una singola registrazione tramite username e event_id."""
    # verifichiamo che l'utente esista
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    # verifichiamo che l'evento esista
    event = session.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Evento non trovato")
    # cerchiamo la registrazione specifica
    registration = session.get(Registration, (username, event_id))
    if not registration:
        raise HTTPException(status_code=404, detail="Registrazione non trovata")
    session.delete(registration)
    session.commit()
    return {"message": "Registrazione eliminata"}
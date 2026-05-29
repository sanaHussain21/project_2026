from fastapi import APIRouter, HTTPException  # strumenti FastAPI per creare le API
from sqlmodel import select  # strumento per interrogare il database
from app.models.user import User  # il modello User che abbiamo creato
from app.models.registration import Registration  # serve per eliminare le registrazioni a cascata
from app.data.db import SessionDep  # la connessione al database

# creiamo il router che raggruppa tutte le API degli utenti
router = APIRouter()


@router.get("/users")
def get_users(session: SessionDep):
    """Restituisce la lista di tutti gli utenti."""
    # prendiamo tutti gli utenti dal database
    users = session.exec(select(User)).all()
    return users


@router.post("/users")
def create_user(user: User, session: SessionDep):
    """Crea un nuovo utente. Restituisce errore se lo username esiste già."""
    # controlliamo se esiste già un utente con questo username
    existing = session.get(User, user.username)
    if existing:
        raise HTTPException(status_code=409, detail="Username già esistente")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/users/{username}")
def get_user(username: str, session: SessionDep):
    """Restituisce un singolo utente tramite il suo username."""
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    return user


@router.delete("/users")
def delete_all_users(session: SessionDep):
    """(Opzionale) Elimina tutti gli utenti e le loro registrazioni."""
    users = session.exec(select(User)).all()
    for user in users:
        # eliminiamo prima le registrazioni dell'utente
        registrations = session.exec(select(Registration).where(Registration.username == user.username)).all()
        for reg in registrations:
            session.delete(reg)
        session.delete(user)
    session.commit()
    return {"message": "Tutti gli utenti eliminati"}


@router.delete("/users/{username}")
def delete_user(username: str, session: SessionDep):
    """(Opzionale) Elimina un utente e tutte le sue registrazioni."""
    user = session.get(User, username)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    # eliminiamo prima le registrazioni associate all'utente
    registrations = session.exec(select(Registration).where(Registration.username == username)).all()
    for reg in registrations:
        session.delete(reg)
    # poi eliminiamo l'utente
    session.delete(user)
    session.commit()
    return {"message": "Utente eliminato"}
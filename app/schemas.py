from pydantic import BaseModel  # BaseModel di Pydantic gestisce la validazione automaticamente
from datetime import datetime


class EventInput(BaseModel):
    """Schema per la creazione e aggiornamento di un evento.
    Pydantic valida automaticamente i tipi dei campi.
    """
    title: str       # deve essere una stringa, altrimenti 422
    description: str # deve essere una stringa, altrimenti 422
    date: datetime   # deve essere una data valida, altrimenti 422
    location: str    # deve essere una stringa, altrimenti 422


class UserInput(BaseModel):
    """Schema per la creazione di un utente.
    Pydantic valida automaticamente i tipi dei campi.
    """
    username: str  # deve essere una stringa, altrimenti 422
    name: str      # deve essere una stringa, altrimenti 422
    email: str     # deve essere una stringa, altrimenti 422
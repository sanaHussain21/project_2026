from sqlmodel import SQLModel, Field  # importiamo gli strumenti per creare il modello del database
from typing import Optional  # Optional serve per i campi che possono essere None
from datetime import datetime  # datetime serve per gestire date e orari


class Event(SQLModel, table=True):
    """Modello ORM per la tabella 'event'.
    Rappresenta un evento nel database.
    """

    # id è la chiave primaria: viene assegnata automaticamente dal database
    # Optional significa che all'inizio può essere None, poi il database gli assegna un numero
    id: Optional[int] = Field(default=None, primary_key=True)

    # titolo dell'evento
    title: str

    # descrizione dettagliata dell'evento
    description: str

    # data e ora dell'evento
    date: datetime

    # luogo dove si svolge l'evento
    location: str
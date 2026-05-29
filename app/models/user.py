from sqlmodel import SQLModel, Field  # importiamo gli strumenti per creare il modello del database


class User(SQLModel, table=True):
    """Modello ORM per la tabella 'user'.
    Rappresenta un utente nel database.
    """

    # username è la chiave primaria: identifica univocamente ogni utente
    username: str = Field(primary_key=True)

    # nome completo dell'utente
    name: str

    # indirizzo email dell'utente
    email: str
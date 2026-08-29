import sqlmodel
import uvicorn
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,validator,field_validator
from sqlmodel import Field, SQLModel, create_engine, Session,select
from sqlmodel.orm import session
app = FastAPI()

#sqlmodel ja coloca Base automaticamente
class Issue(SQLModel,table =True):
    id_issue : int | None = Field(default=None, primary_key=True)
    name :str
    feito : bool = False

   # validator é redutante para pydantic  V2
   # @validator('id_issue')
    #def id_issue_validator(cls,value):
       # if(value<=0):
       #     raise ValueError("id_issue must be greater than 0")
       # return value
    @field_validator("id_issue")
    @classmethod
    def check_id_issue(cls, n:int | None):
        if n <= 0:
            raise ValueError("id_issue must be greater than 0")
        return n

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True) # echo para imprimerir tutod que sql faz


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
@app.get("/")
async def root():
    return {"message": "Hello World"}

lista_issue = []
#async def get_item():
@app.post("/postarissue")
async def adicionar_issue(issue:Issue):
    create_db_and_tables()
    with(Session(engine) as session):
        session.add(issue)
        session.commit()
        session.refresh(issue)
        return {"Lista adicionar com sucesso":issue}

@app.get("/issue")
async def imprimir_issue():
    #arrumar essa funcao depois,ela nao "printa" nada
    with(Session(engine) as session):
        info = select(Issue)
        result = session.exec(info).all() #aparantemente o all converter o tipo para o python ler
    return {"Issues" : result}

@app.get("/issue/{id_issue}")
async def retornar_issue(id_issue:int):
    with Session(engine) as session:
        info = session.get(Issue,id_issue) # troque para get,aparentemente é mais rapido que o outro
        if not info:
            raise HTTPException(status_code=404,detail ="id not found")
        return {"Issue: ",info.id_issue} # problema de usar de tipo Issue não é valido em retorno

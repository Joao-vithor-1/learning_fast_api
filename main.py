import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel,validator,field_validator
app = FastAPI()

class Issue(BaseModel):
    name :str
    feito : bool = False
    id_issue : int
   # validator é redutante para pydantic  V2
   # @validator('id_issue')
    #def id_issue_validator(cls,value):
       # if(value<=0):
       #     raise ValueError("id_issue must be greater than 0")
       # return value
    @field_validator("id_issue")
    @classmethod
    def check_id_issue(cls, n:int):
        if n <= 0:
            raise ValueError("id_issue must be greater than 0")
        return n

@app.get("/")
async def root():
    return {"message": "Hello World"}

lista_issue = []
#async def get_item():
@app.post("/postarissue")
async def adicionar_issue(issue:Issue):
    lista_issue.append(issue)
    return {"Lista adicionar com sucesso":issue, "tamanho lista":len(lista_issue)}

@app.get("/issue")
async def imprimir_issue():
    return {"Issues" : lista_issue}
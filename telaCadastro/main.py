from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import bcrypt
import sqlite3
from database import create_tables

app = FastAPI()

# Configurando o diretório static para servir arquivos estáticos
app.mount("/static", StaticFiles(directory="."), name="static")
templates = Jinja2Templates(directory="templates")

# chamando a função para garantir que ela existe
create_tables()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit/")
async def submit_form(
    email: str = Form(...),
    cpf: str = Form(...),
    role: str = Form(...),
    password: str = Form(None),
):
    hashed_password = None

    # Lógica de hash da senha apenas para o papel "psicologo"
    if role == 'psicologo':
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Lógica para processar dados
    print(f"Email: {email}, CPF: {cpf}, Role: {role}, Hashed Password: {hashed_password}")

    # Redirecione para a página de sucesso apropriada com base no papel escolhido
    if role == 'aluno':
        return RedirectResponse(url="/success-aluno")
    elif role == 'psicologo':
        return RedirectResponse(url="/success-psicologo")

@app.get("/success-psicologo", response_class=HTMLResponse)
async def success_psicologo(request: Request):
    return templates.TemplateResponse("success_psicologo.html", {"request": request})

@app.get("/success-aluno", response_class=HTMLResponse)
async def success_aluno(request: Request):
    return templates.TemplateResponse("success_aluno.html", {"request": request})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level='info', reload=False)


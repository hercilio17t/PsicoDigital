from fastapi import FastAPI, Form, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import bcrypt
import sqlite3
from database import create_tables, get_user_by_email

app = FastAPI()

# Configurando o diretório static para servir arquivos estáticos
app.mount("/static", StaticFiles(directory="."), name="static")
templates = Jinja2Templates(directory="templates")

# Chamando a função para garantir que ela existe
create_tables()

# Função de verificação de autenticação
async def authenticate_user(email: str, password: str, role: str):
    user = get_user_by_email(email)

    if user and user["role"] == role and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
        return True

    return False

# Middleware para verificar autenticação
async def authenticate(request: Request, role: str = Form(...), email: str = Form(...), password: str = Form(...)):
    if not await authenticate_user(email, password, role):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

app = FastAPI(dependencies=[Depends(authenticate)])

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
    # Lógica de hash da senha apenas para o papel "psicologo"
    hashed_password = None
    if role == 'psicologo':
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Lógica para processar dados
    print(f"Email: {email}, CPF: {cpf}, Role: {role}, Hashed Password: {hashed_password}")

    # Redirecione para a página de sucesso apropriada com base no papel escolhido
    if role == 'aluno':
        return RedirectResponse(url="/success-aluno")
    elif role == 'psicologo':
        return RedirectResponse(url="/success-psicologo")

@app.post("/login/")
async def login(
    request: Request,
    role: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    return templates.TemplateResponse("login.html", {"request": request, "role": role})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level='info', reload=False)

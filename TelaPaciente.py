# main.py
from fastapi import FastAPI, Form, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import bcrypt
import sqlite3
from database import create_tables, get_user_by_email, create_appointment

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
        return True, user

    return False, None

# Middleware para verificar autenticação
async def authenticate(request: Request, role: str = Form(...), email: str = Form(...), password: str = Form(...)):
    authenticated, user = await authenticate_user(email, password, role)
    if not authenticated:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return user

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

    # Lógica para processar dados e armazenar no banco de dados
    # (você precisa adaptar isso com base no seu modelo de dados)
    # Exemplo: salvar usuário no banco de dados
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (email, cpf, role, password) VALUES (?, ?, ?, ?)",
                   (email, cpf, role, hashed_password))
    conn.commit()
    conn.close()

    # Redirecione para a página de sucesso apropriada com base no papel escolhido
    if role == 'aluno':
        return RedirectResponse(url="/success-aluno")
    elif role == 'psicologo':
        return RedirectResponse(url="/success-psicologo")

@app.get("/success-psicologo", response_class=HTMLResponse)
async def success_psicologo(request: Request, user: dict = Depends(authenticate)):
    return templates.TemplateResponse("success_psicologo.html", {"request": request, "user": user})

@app.get("/success-aluno", response_class=HTMLResponse)
async def success_aluno(request: Request, user: dict = Depends(authenticate)):
    return templates.TemplateResponse("success_aluno.html", {"request": request, "user": user})

# Novas rotas para funcionalidades do paciente
@app.get("/patient-dashboard", response_class=HTMLResponse)
async def patient_dashboard(request: Request, user: dict = Depends(authenticate)):
    # Recupera informações sobre agendamentos, histórico, etc. do banco de dados
    # (você precisa adaptar isso com base no seu modelo de dados)
    appointments = []  # Exemplo: Consulta agendada
    history = []  # Exemplo: Histórico de consultas
    available_slots = []  # Exemplo: Horários disponíveis de outros psicólogos

    return templates.TemplateResponse(
        "patient_dashboard.html",
        {"request": request, "user": user, "appointments": appointments, "history": history, "available_slots": available_slots}
    )

@app.post("/schedule-appointment")
async def schedule_appointment(
    request: Request,
    user: dict = Depends(authenticate),
    psychologist_email: str = Form(...),
    datetime: str = Form(...),
):
    # Lógica para agendar nova consulta e armazenar no banco de dados
    create_appointment(user["email"], psychologist_email, datetime)
    return RedirectResponse(url="/patient-dashboard")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level='info', reload=False)

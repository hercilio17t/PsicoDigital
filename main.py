from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Configurando o diretório static para servir arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Resto do seu código...

@app.post("/submit/")
async def submit_form(email: str = Form(...), cpf: str = Form(...), role: str = Form(...), password: str = Form(None)):
    if role == 'psicologo':
        # Lógica para processar dados para psicólogos (se necessário)
        print(f"Email: {email}, CPF: {cpf}, Role: {role}, Password: {password}")
        return RedirectResponse(url="/success-psicologo")
    else:
        # Lógica para processar dados para alunos
        print(f"Email: {email}, CPF: {cpf}, Role: {role}")
        return RedirectResponse(url="/success-aluno")

@app.get("/success-psicologo", response_class=HTMLResponse)
async def success_psicologo(request: Request):
    return templates.TemplateResponse("success_psicologo.html", {"request": request})

@app.get("/success-aluno", response_class=HTMLResponse)
async def success_aluno(request: Request):
    return templates.TemplateResponse("success_aluno.html", {"request": request})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)

# **Brain Agriculture – Backend API**

API construída com **FastAPI**, **SQLAlchemy**, **Pydantic**, **PostgreSQL**, **Alembic** e **Docker**, destinada ao gerenciamento de **produtores rurais**, **propriedades**, **safras**, **culturas** e **culturas plantadas**.

O projeto implementa regras de negócio importantes do agronegócio, como:

* Validação de **CPF/CNPJ**
* Garantia de consistência das áreas da fazenda
* Relacionamentos entre produtor → propriedade → safra → culturas plantadas
* Sistema de autenticação JWT
* Auditoria automática (`criado_em`, `atualizado_em`, …)

---

## **Tecnologias Principais**

| Tecnologia                  | Uso                           |
| --------------------------- | ----------------------------- |
| **FastAPI**                 | API REST                      |
| **SQLAlchemy + Alembic**    | ORM + Migrações               |
| **PostgreSQL**              | Banco de dados                |
| **Pydantic v2**             | Schemas e validações          |
| **Docker + docker-compose** | Contêinerização               |
| **Uvicorn**                 | Servidor ASGI                 |
| **Poetry**                  | Gerenciamento de dependências |

---

# **Estrutura principal do Projeto**

```
app/
│── api/
│   └── v1/
│       ├── auth/
│       ├── user/
│       ├── producer/
│       ├── property/
│       ├── property_season/
│       ├── season/
│       ├── culture/
│       └── planted_culture/
│
│── database/
│   ├── base.py
│   ├── session.py
│   └── models/
│       ├── produtor.py
│       ├── propriedade.py
│       ├── safra.py
│       ├── cultura.py
│       ├── cultura_plantada.py
│       ├── propriedade_safra.py
│       └── auditoria_mixin.py
│
│── middleware/
│── core/
│── utils/
│── main.py
│
alembic/
│── versions/
│    └── 0001_initial.py
│── env.py
│── script.py.mako
```

---

# **Configuração da Aplicação**

## **Variáveis de Ambiente (.env)**

Crie um arquivo `.env` na raiz:

```
DATABASE_URL=postgresql://admin:postgre@db:5432/brain_db
SECRET_KEY=uma_chave_super_secreta
SMTP_SERVER=
SMTP_PORT=
SMTP_USERNAME=
SMTP_PASSWORD=
```

---

# **Rodando com Docker + Makefile**

## Subir os serviços

```bash
make up
```

## Parar tudo

```bash
make down
```

## Build sem cache

```bash
make build
```

## Logs do back-end

```bash
make logs
```

## Limpar tudo

```bash
make clean
```

---

# **Rodando Localmente (sem Docker)**

### 1. Instale dependências

```bash
poetry install
```

### 2. Rode o servidor

```bash
make run-fastapi
```

ou

```bash
uvicorn app.main:app --reload --port 8007
```

---

# **Migrações com Alembic**

### Aplicar migrações

```bash
poetry run alembic upgrade head
```

### Ver versão atual

```bash
poetry run alembic current
```

---

# **Autenticação**

O projeto usa **JWT** com middleware:

* Login `/auth/login`
* Rotas protegidas usam:

```python
authuser: Annotated[AuthUser, Security(jwt_middleware)]
```

---

# **Regras de Negócio Implementadas**

### ✔ Validação completa de CPF/CNPJ (Pydantic v2)

Com check-digit real.

### ✔ Restrições de área

Em `propriedade`:

```
area_agricultavel + area_vegetacao <= area_total
```

### ✔ Relacionamentos

* Producer → Propriedades (**1:N**)
* Property → Safras (**1:N**, via tabela propriedade_safra)
* PropertySeason → CulturasPlantadas (**1:N**)
* PlantedCulture → Culture (**N:1**)

### ✔ Exclusões em CASCADE

Deleta automaticamente propriedades → culturas plantadas.

---

# **Principais Endpoints**

### **Produtores**

```
GET    /producers
GET    /producers/{id}
POST   /producers
PUT    /producers/{id}
DELETE /producers/{id}
```

### **Propriedades**

```
GET    /properties
POST   /properties
...
```

### **Safras**

```
GET    /seasons
...
```

### **Culturas**

```
POST   /cultures
...
```

### **Culturas Plantadas**

```
POST   /planted-cultures
GET    /planted-cultures
...
```

---

# **Testando a API**

Após subir o container:

```
http://localhost:8007/docs
```

Swagger completo e funcional.

---

# **Como contribuir**

1. Crie uma branch
2. Implemente sua feature
3. Rode testes e linters
4. Abra um Pull Request

---

# **Licença**

Licença **MIT** — livre para uso comercial e modificações.

---
# Etapa 1: Builder
FROM python:3.12-slim AS builder

WORKDIR /app

# Instala pacotes do sistema necessários
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libpq5 \
    curl \
    tzdata \
    && apt-get clean

ENV TZ=America/Sao_Paulo

# Instala a versão atual do Poetry (compatível com Python 3.12)
RUN pip install --no-cache-dir poetry==1.8.2

# Copia os arquivos do Poetry
COPY pyproject.toml poetry.lock README.md ./

# Configura o Poetry
RUN poetry config virtualenvs.create false

# Instala dependências
RUN poetry install --no-interaction --no-ansi --no-root

# Copia o restante do código
COPY . .

# Instala dependências do código
RUN poetry install --no-interaction --no-ansi

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8007"]

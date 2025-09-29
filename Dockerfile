# On définit la version de python et slim pour pas que la machine soit trop lourde
FROM python:3.9-slim

# Working Directory
WORKDIR /app

# Copy source code to working directory
# on va copier tout le contenu du dossier courant (.) vers le dossier /app/ dans le container
COPY .  /app/

# Install packages from requirements.txt

RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

#la commande cm va généerer l'image et lancer le container
CMD ["python", "app.py"]
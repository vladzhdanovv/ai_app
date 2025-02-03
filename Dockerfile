FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
COPY ./.env /code/.env

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 8000

# CMD ["fastapi", "run",  "app/main.py"]
CMD ["fastapi", "dev",  "/code/app/main.py", "--host", "0.0.0.0"]

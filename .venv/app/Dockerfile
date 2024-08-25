FROM python:3.10

LABEL authors="vboxuser"

WORKDIR /home/vboxuser/PycharmProjects/pythonProjectBot/.venv/app

COPY ./requirements.txt /home/vboxuser/PycharmProjects/pythonProjectBot/.venv/app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /home/vboxuser/PycharmProjects/pythonProjectBot/.venv/app/requirements.txt

COPY ./config.py /home/vboxuser/PycharmProjects/pythonProjectBot/.venv/app/config.py
COPY ./keyboard.py /home/vboxuser/PycharmProjects/pythonProjectBot/.venv/app/keyboard.py
COPY ./handlers.py /home/vboxuser/PycharmProjects/pythonProjectBot/.venv/app/handlers.py
COPY ./handlers_time.py /home/vboxuser/PycharmProjects/pythonProjectBot/.venv/app/handlers_time.py
COPY ./handlers_timer.py /home/vboxuser/PycharmProjects/pythonProjectBot/.venv/app/handlers_timer.py
COPY ./main.py /home/vboxuser/PycharmProjects/pythonProjectBot/.venv/app/main.py

CMD ["python", "main.py"]
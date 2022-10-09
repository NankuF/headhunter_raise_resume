FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt update && apt upgrade -y &&\
    wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb &&\
    apt install ./google-chrome-stable_current_amd64.deb -y &&\
    apt install nano -y

COPY . .

CMD ["python", "main.py"]
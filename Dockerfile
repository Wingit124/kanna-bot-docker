FROM python:3.10.6
WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt --use-deprecated=html5lib --use-deprecated=legacy-resolver
COPY . /bot
CMD python bot.py
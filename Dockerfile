FROM python:3.10.6
WORKDIR /
RUN pip install -r requirements.txt
CMD python bot.py
FROM python:3.11

RUN pip install --upgrade pip
RUN pip install discord.py
RUN pip install pynacl
RUN pip install requests
RUN pip install dotenv

CMD python main.py

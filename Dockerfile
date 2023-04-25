FROM python:3.11
COPY . /code
COPY ./requirements.txt /code/requirements.txt
WORKDIR /code
EXPOSE 8000:8000
RUN pip install -r requirements.txt
CMD [ "uvicorn", "core.main:app", "--host", "0.0.0.0", "--reload" ]


# docker run -p 8000:8000 -t -i ml19
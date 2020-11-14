FROM python:3.6

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip

WORKDIR /code

VOLUME /media/kobatcon/33946daa-b25d-46a9-80d0-06b326db3c0d/home/alex/Steller/steller2:/code/.

COPY requirements.txt /code

RUN python3 -m pip install -r requirements.txt

COPY . /code

EXPOSE 8000

#RUN python3 manage.py migrate
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

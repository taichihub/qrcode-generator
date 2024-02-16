FROM python:3.10
WORKDIR /app
ENV PYTHONPATH /app
COPY Pipfile Pipfile.lock /app/
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile --system
COPY src/ /app/src/

VOLUME /app/data
VOLUME /app/img
VOLUME /app/qr_code
CMD ["python", "/app/src/read_csv.py"]

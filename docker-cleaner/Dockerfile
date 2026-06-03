FROM python:3.12-slim
WORKDIR /app/
COPY datacleaner.py /app/
COPY "InputFiles/" /app/InputFiles/
COPY requirements.txt /app/
RUN pip install -r requirements.txt
RUN mkdir "OutputFiles"
ENTRYPOINT [ "python3", "datacleaner.py" ]
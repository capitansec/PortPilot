FROM python:3.11.6
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
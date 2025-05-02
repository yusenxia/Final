FROM python:3.10-slim
WORKDIR /app
COPY minesweeper.py requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "minesweeper.py"]

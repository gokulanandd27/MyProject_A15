FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the Flask port
EXPOSE 5000

# Run the application with Socket.IO support (using python directly for simplicity or gunicorn+eventlet)
# For dev/demo, python app.py is fine as it uses socketio.run
CMD ["python", "app.py"]

FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    libfontconfig1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY hand_tracker.py .

# Set environment variables for display
ENV QT_X11_NO_MITSHM=1
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "hand_tracker.py"] 
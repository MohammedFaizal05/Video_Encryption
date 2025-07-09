# Use Debian as the base image (better compatibility than Alpine)
FROM python:3.12.9-slim-bullseye

# Install system dependencies for GUI and video processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1-mesa-glx \
    python3-tk \
    x11-utils \
    x11-xserver-utils \
    xorg \
    xvfb \
    dbus-x11 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Ensure the script is executable
RUN chmod +x /app/enc_dec.py

# Set environment variables for GUI applications
ENV DISPLAY=:99
ENV QT_X11_NO_MITSHM=1

# Start Xvfb and ensure it's running before launching the app
CMD Xvfb :99 -screen 0 1024x768x16 & sleep 2 && export DISPLAY=host.docker.internal:0.0 && python /app/enc_dec.py

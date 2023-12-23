# Specify the base image. Python 3.8 is a good choice for most applications
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy dependency files to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other files to the working directory
COPY . .

# Env var for Flask
ENV FLASK_APP=pi.py

# Run
CMD ["flask", "run", "--host=0.0.0.0"]

# Use a specific Python version as the base image for the build stage.
FROM python:3.9-slim-buster

# Set environment variables to prevent Python from buffering stdout/stderr.
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container.
WORKDIR /app

# Copy the requirements file and install dependencies.
# This step is cached if requirements.txt doesn't change, speeding up builds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire Django project into the container.
COPY . /app/

# Collect static files. This is important for production environments where
# WhiteNoise will serve them. '--noinput' prevents prompts.
RUN python manage.py collectstatic --noinput

# Create a non-root user and group for running the application.
# This is a security best practice.
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
USER appuser

# Expose the port on which Gunicorn will run.
EXPOSE 8000

# Command to run the Gunicorn server.
# `--bind 0.0.0.0:8000` makes the server accessible from outside the container.
# `cape_control_backend.wsgi:application` points to your Django project's WSGI application.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cape_control_backend.wsgi:application"]


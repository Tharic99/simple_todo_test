# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 8000

# Run collectstatic
RUN python manage.py collectstatic --noinput


# Run Gunicorn to serve the Django application
CMD ["gunicorn", "simple_todo.wsgi:application", "--bind", "0.0.0.0:8000"]

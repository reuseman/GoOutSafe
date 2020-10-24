# DEVELOPMENT Dockerfile

FROM python:3.6.12-slim

# Set working directory in the container
WORKDIR /code

# Copy the requirements folder in the cwd
COPY requirements/ requirements/

# Install the dependencies
RUN pip install -r requirements/dev.txt 

# Copy the monolith folder in the cwd
COPY monolith/ monolith/

# Export the location of app.py
ENV FLASK_APP monolith/app.py

# Run and bind on the 0.0.0.0 address
CMD ["flask", "run", "-h", "0.0.0.0"]
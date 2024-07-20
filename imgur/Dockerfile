# Use the official Python image
FROM python:3.12.4

# Set the working directory in thdocker-compose up --builde container
WORKDIR /code

# Copy the requirements file into the container
COPY requirements.txt /code/

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code/

# Expose port 8000 to be accessible from the host
EXPOSE 8000
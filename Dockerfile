# Use the official Python image
FROM python:3.11.4

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file first to leverage Docker cache
COPY requirements.txt ./requirements.txt


# Install required Python packages
RUN python -m  pip install -r requirements.txt 

#copy the rest of the application files to the container's working directory
COPY . . 


# Expose the port that Django will run on
EXPOSE 8000

# Command to run your Django application
CMD streamlit run app.py

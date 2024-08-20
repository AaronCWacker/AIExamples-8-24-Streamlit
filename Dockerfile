# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

#python -m nltk.downloader stopwords punkt wordnet

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit app into the container
COPY app.py .

# Expose the port Streamlit runs on
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py"]

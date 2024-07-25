# Use the specified base image
FROM huggingface/transformers-pytorch-gpu:4.41.2

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file (if you have one)
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 9000

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9000"]

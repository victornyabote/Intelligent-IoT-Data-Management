# Step 1: Use an official Python image from Docker Hub
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy requirements.txt for dependencies
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the application code into the container
COPY . .

# Step 6: Expose the port that the app will run on (default for Flask is 5000)
EXPOSE 5000

# Step 7: Run the Flask/Django application
CMD ["python", "app.py"]  # For Flask
# or
# CMD ["python", "manage.py", "runserver"]  # For Django

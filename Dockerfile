FROM python:3.9-bullseye

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY . /app/

#Install packages
RUN pip install -r requirements.txt

#Export port
EXPOSE 80

# Run app.py at container launch
ENTRYPOINT ["gunicorn", "-b", ":8080", "main:APP"]
# Use an official Python runtime as a parent image
FROM python:3.9-slim
# Add a default user
RUN useradd --create-home --shell /bin/bash admin

COPY . /home/admin/app
WORKDIR /home/admin/app

# Install any needed dependencies specified in requirements.txt
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Default user home
RUN chown -R admin:admin /home/admin/app
RUN chmod 755 /home/admin/app
USER admin

CMD ["python", "-u", "app.py"]
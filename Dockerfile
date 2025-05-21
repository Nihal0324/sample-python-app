FROM python:3.8.0-alpine3.10

USER root

# Install necessary packages
RUN apk add --no-cache shadow bash

# Create user 'nihal' with password 'nihal123'
RUN useradd -m -s /bin/bash nihal \
    && echo "nihal:nihal123" | chpasswd

# Copy password-protected shell script and configure .bashrc
COPY secure_shell.sh /home/nihal/secure_shell.sh
RUN chmod +x /home/nihal/secure_shell.sh \
    && echo "/home/nihal/secure_shell.sh" >> /home/nihal/.bashrc \
    && chown nihal:nihal /home/nihal/.bashrc /home/nihal/secure_shell.sh

# Set working directory and copy app files
WORKDIR /app
COPY src/ /app/src/
COPY ./requirements.txt /app
RUN ls -la /app

# Install Python dependencies
RUN python3 --version
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r /app/requirements.txt
RUN pip3 list --format=columns

# Switch to 'nihal' user
USER nihal

EXPOSE 5001
ENTRYPOINT ["python3", "/app/src/app.py"]


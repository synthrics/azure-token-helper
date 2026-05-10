FROM mcr.microsoft.com/azure-cli:azurelinux3.0

WORKDIR /app

COPY requirements.txt .
RUN tdnf install -y python3-pip \
    && python3 -m pip install --no-cache-dir -r requirements.txt \
    && tdnf clean all

COPY server.py .
EXPOSE 9999

CMD ["python3", "server.py"]

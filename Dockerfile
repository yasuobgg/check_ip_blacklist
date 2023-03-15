# For more information, please refer to https://aka.ms/vscode-docker-python
# FROM python:3.10-slim
# WORKDIR /app
# COPY . /app
# RUN  pip install -r requirements.txt
# EXPOSE 5000
# CMD ["python", "app.py"]

FROM python:3.10-slim
ADD . /app
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt
EXPOSE 5008
CMD ["python", "get_ip.py"]



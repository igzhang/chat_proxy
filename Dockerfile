FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
COPY main.py .
CMD ["python", "main.py"]
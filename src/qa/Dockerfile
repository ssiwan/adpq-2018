FROM python:3.6
ADD . .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
CMD ["python", "runner.py"]
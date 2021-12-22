FROM python:3-stretch
RUN pip install --trusted-host pypi.python.org -r requirements.txt
EXPOSE 64001
CMD ["python","server.py"] 

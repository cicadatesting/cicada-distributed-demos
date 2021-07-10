FROM cicadatesting/cicada-distributed-base-image:latest

RUN pip install requests

COPY . .

ENTRYPOINT ["python", "-u", "test.py"]

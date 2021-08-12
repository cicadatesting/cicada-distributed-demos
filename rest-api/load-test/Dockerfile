FROM cicadatesting/cicada-distributed-base-image:1.3.0

RUN pip install requests

COPY . .

ENTRYPOINT ["python", "-u", "test.py"]

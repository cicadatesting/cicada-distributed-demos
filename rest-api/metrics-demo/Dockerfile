FROM cicadatesting/cicada-distributed-base-image:1.6.0

RUN pip install requests

COPY . .

ENTRYPOINT ["python", "-u", "test.py"]

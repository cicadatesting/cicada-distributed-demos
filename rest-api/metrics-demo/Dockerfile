FROM cicadatesting/cicada-distributed-base-image:1.5.0

RUN pip install requests

COPY . .

ENTRYPOINT ["python", "-u", "test.py"]

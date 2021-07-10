FROM cicadatesting/cicada-distributed-base-image:pre-release

RUN pip install requests

COPY . .

ENTRYPOINT ["python", "-u", "test.py"]

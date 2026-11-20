FROM eclipse-temurin:21.0.13_9-jre-noble@sha256:b4f9d2a0bc273417cf5219b7b832bbf0493ed500b7b57d5001d9f83374659060 AS jre
FROM python:3.14.10-slim-trixie@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f AS web
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements*.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt && pip check
COPY . .
RUN mkdir -p scratch/regular/target scratch/regular/calculadora/db scratch/phase02 && chown 10001:10001 scratch/phase02
USER 10001:10001
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "--noreload", "--insecure"]

FROM web AS regular
COPY --from=jre /opt/java/openjdk /opt/java/openjdk
CMD ["python", "-m", "adapters.launch", "--java", "/opt/java/openjdk/bin/java", "--openssl", "/usr/bin/openssl"]

# Same digest in every app on the host (benefits-aggregator, open-congress): the server then keeps
# one copy of the base layers. Bump all three together.
FROM python:3.12-slim@sha256:05cda9777409a9c3ffddd94a4c476b79f0769a0b4857f0c7ed9226b6800b0d6f

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Every dependency ships as a binary wheel (psycopg[binary], Pillow), so no compiler or libpq
# headers are needed; pip is removed afterwards, nothing installs packages at runtime.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y pip

COPY . .

RUN chmod +x /app/entrypoint.sh \
    && mkdir -p /app/staticfiles /app/media

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]

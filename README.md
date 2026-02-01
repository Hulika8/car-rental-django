# Car Rental Django

## Run with Docker Compose
Requirements: Docker Desktop

```bash
docker compose up --build
```

API will be available at:
http://localhost:8000/

## Celery (local without Docker)

Redis:
```bash
brew services start redis
```

Worker:
```bash
celery -A car_rental worker -l info
```

Beat:
```bash
celery -A car_rental beat -l info
```

Manual task trigger:
```bash
python manage.py shell
```

```python
from reservations.tasks import activate_todays_reservations
activate_todays_reservations.delay()
```
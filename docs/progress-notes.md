# Project Progress Notes

## Plan Snapshot
- Week 1: Foundations (models, admin, validations) ✅
- Week 2: Core business logic (reservations) ✅
- Week 3: API + automation + cancellation/refund ✅/⏳
- Week 4: Testing + frontend + deployment ⏳

## 4-Week Roadmap (Full)
### ✅ Week 1: Foundations
- Django Models (Car, Reservation, UserProfile)
- PostgreSQL Database Design
- Admin Panels (custom configurations)
- Model Validations (clean methods)
- Business Logic Methods

### 🔄 Week 2: Core Business Logic (in progress)
#### Days 8–9: Auto Calculation ✅
- Django Admin Custom Form
- Daily rate auto-fill (AJAX)
- Total amount auto-calc (real-time)
- JS Integration (MutationObserver + setInterval)
- Real-time form updates
- blank=True, null=True migrations
- Backend fallback on save

#### Days 10–11: Reservation System 🔄
- signals.py → auto car status update
- apps.py → signal activation
- admin.py → status management
- admin.py → advanced validation (end_date, duplicate active, cancellation)
- models.py → user profile validation
- models.py → create vs update validation (if not self.pk)
- Testing ⏳
- Refactor: field naming improvement ⏳

#### Days 12–14: User System
- User registration/login
- JWT authentication
- User profile management
- ID/license validation
- Smart admin enhancements

### 🚀 Week 3: Advanced Features (updated)
#### Days 15–16: API Development ✅
- DRF setup
- Serializers (Car, Reservation, UserProfile)
- ViewSets
- API authentication (JWT)
- Endpoints:
  - GET /api/cars/
  - GET /api/cars/{id}/
  - POST /api/reservations/
  - GET /api/reservations/
  - POST /api/reservations/{id}/activate/
  - POST /api/reservations/{id}/complete/
  - POST /api/reservations/{id}/cancel/
  - GET /api/reservations/{id}/cancellation-policy/
- API docs (Swagger/DRF Spectacular)
- Permissions & throttling

#### Days 17–18: Automation & Scheduled Tasks ✅/⏳
- Celery setup
- Redis/RabbitMQ broker
- Celery worker config
- Scheduled tasks:
  - activate_todays_reservations (00:00)
  - cleanup_expired_reservations (01:00)
  - complete_ended_reservations (23:59)
  - send_reminder_emails (08:00) ⏳
  - check_overdue_rentals (hourly) ⏳
- Background jobs:
  - Async email
  - Image processing
  - PDF invoice
  - Backup jobs

#### Day 19: Cancellation Policy & Refund ✅
- can_be_cancelled()
- get_cancellation_fee()
- cancel() flow
- Cancellation fields migration
- Business rules + API endpoints

#### Day 20: Payment System 🔄
- Stripe integration ⏳
- Payment API endpoints ✅ (local)
- Webhook handling ⏳
- Refund system ✅ (local)
- Refund history tracking ⏳
- Stripe refund integration ⏳

#### Day 21: Email & Notifications ⏳
- Email backend + templates
- Async email (Celery)
- Notification types (reservation lifecycle)
- In-app notifications / WebSocket / SMS (optional)

### 🧪 Week 4: Testing & Deployment ⏳
#### Days 22–23: Testing
- Unit tests
- API tests (pytest)
- Integration tests
- Celery task tests ⏳
- Cancellation policy tests ✅
- Refund system tests ✅
- Postman collection ⏳
- Coverage report ⏳

#### Days 24–25: Demo Frontend ⏳
- Basic HTML/CSS/Bootstrap
- AJAX API calls
- Responsive UI
- Payment integration UI
- Cancellation & policy UI
- Real-time status updates

#### Days 26–28: Deployment & Docs ⏳
- Docker (Django, Postgres, Redis, Celery)
- docker-compose setup
- Heroku/AWS deploy
- Env vars
- Logging & monitoring
- README + API docs
- Demo video / presentation

## Completed (Earlier)
- Reservation actions + cancellation policy/fee
- Swagger docs
- Permissions & throttling (login/register scoped)
- Tests: reservations + cars + users
- Field rename: daily_price → daily_rate + migration
- Celery setup + reservation automation tasks
- Docker setup (Dockerfile, compose, README)

## Recent Work (This Session)
- Docker compose fix PR merged
- Settings env vars PR merged
- Payment/Refund:
  - Added payment/refund fields to `Reservation`
  - Added `get_refund_amount()` model method
  - Added pay/refund endpoints (views)
  - Added refund tests
  - Migrations applied
  - Tests passed

## Decisions/Notes
- Payment rule: full payment required (no partials for now)
- `remaining_amount` kept for future partial/deposit support
- Postman auth: access token stored in env; collection uses `{{access_token}}`

## Manual Test Status
- Pay: done (full payment)
- Cancel: done (reservation cancelled)
- Refund: done (refund processed, 0.00 due to 100% fee)

## Next Steps
1) Manual test: cancel → refund
2) Update docs (test plan, API notes)
3) Commit changes (views, models, serializers, tests, migration)

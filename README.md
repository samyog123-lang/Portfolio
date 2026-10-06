# Samyog Panthee Portfolio

A Django portfolio for Python and backend projects. Projects, skills, developer-journey milestones, journal entries, chatbot knowledge, profile details, and contact submissions are managed in Django Admin.

## Requirements

- Python 3.14 (or a compatible supported Python release)
- PowerShell on Windows

## Local setup

```powershell
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the portfolio and `http://127.0.0.1:8000/admin/` to manage content and review contact messages. The seeded visitor baseline is 10,003; the counter increments once per browser session.

The public read-only project API is available at `/api/projects/` and `/api/projects/<slug>/`. Contact and text-style messages are validated, CSRF-protected, rate-limited, and stored in the admin inbox. Text-style messages do not send carrier SMS without an SMS provider.

## Content management

Edit the profile and upload a resume in Portfolio Profile. Upload project screenshots and galleries in Projects. Add skills and developer-journey milestones in the matching sections. Blog drafts remain private until Published is enabled. Contact Messages and the visitor counter are available in the admin.

The profile portrait is at `media/profile/profile.jpg`. Project and blog uploads are stored under `media/` in development. Uploaded media must be served by a private or object-storage-backed media service in production.

## Environment

Settings load `.env` automatically. Keep `.env` out of version control. `DJANGO_DEBUG=0` requires a unique `DJANGO_SECRET_KEY` and production `DJANGO_ALLOWED_HOSTS`. PostgreSQL can be enabled with `DJANGO_DB_ENGINE=postgresql` and the `POSTGRES_*` values. AI replies are optional; without `OPENAI_API_KEY`, Samyog AI uses the verified local portfolio knowledge.

## Production checklist

1. Set a strong secret key, `DJANGO_DEBUG=0`, allowed hosts, and PostgreSQL credentials.
2. Configure SMTP, HTTPS, and a production cache backend for contact rate limiting.
3. Run `python manage.py migrate` and `python manage.py collectstatic`.
4. Use a production WSGI/ASGI server and configure persistent media storage and backups.
5. Create a superuser, review uploaded content, and run `python manage.py check --deploy`.

## Tests

```powershell
python manage.py check
python manage.py test portfolio.tests
```# Portfolio

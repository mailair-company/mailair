<p align="center">
  <img src="frontend/public/logo.svg" alt="Mailair" height="48" />
</p>

<h3 align="center">Email Marketing & Team Hub for Small Businesses</h3>

<p align="center">
  Campaigns, an AI-sorted inbox, docs, chat, and calls — in one place.<br />
  <a href="https://mailair.company"><strong>mailair.company</strong></a>
</p>

<p align="center">
  <img src="frontend/public/social/mailair-og.png" alt="Mailair — today in your hub" width="720" />
</p>

---

## What Mailair does

Small teams usually run on five disconnected tools: one for marketing, one for email, one for chat, one for files, one for calls. Mailair puts them in one hub.

**Email marketing**
- Campaigns with audiences, a composer, and tracking for opens, clicks, bounces, and unsubscribes
- Automated follow-up sequences
- Per-organization monthly send limits by plan

**Shared inbox, sorted by AI**
- Gmail and Outlook in one inbox, with multi-account support
- Every email classified (Urgent, Needs Response, Follow Up, FYI, Newsletter, Spam) and priority-scored
- Action items and deadlines extracted automatically
- Revenue signals (quotes, invoices, renewals) and relationship health scoring
- Reply drafts in the user's own voice, with a live "voice match" score comparing each draft to what was actually sent

**Team workspace**
- Shared docs, files, and team chat
- Built-in voice and video calls (WebRTC)
- Teams, roles, SLAs, and auto-assignment rules

**Integrations**
- HubSpot, Salesforce, Slack, Google Calendar, webhooks
- Web app (PWA), iOS and Android app, and a browser extension

---

## Tech stack

| Layer          | Technology                                                    |
|----------------|---------------------------------------------------------------|
| Web frontend   | Next.js 14 (Pages Router), TypeScript, Tailwind CSS           |
| Mobile         | Expo 54 / React Native 0.81                                   |
| Backend        | Python 3.11, FastAPI, APScheduler background workers          |
| Database/Auth  | Supabase (PostgreSQL, Auth, Row-Level Security)               |
| AI             | Claude API — Opus for classification and drafting, Haiku for high-volume extraction |
| Email          | Gmail API, Microsoft Graph (Outlook), Resend (campaign sending) |
| Payments       | Razorpay subscriptions                                        |
| Hosting        | Vercel (frontend), Render (backend), GitHub Actions (CI, scheduled jobs) |

---

## Repository layout

```
.
├── frontend/            Next.js web app and marketing site
│   ├── pages/           Routes (landing, inbox, campaigns, workspace, …)
│   ├── components/
│   ├── lib/             API client, Supabase client, helpers
│   └── public/          Static assets, social banners, sitemap
├── backend/             FastAPI service
│   ├── main.py          App entry point and router registration
│   ├── config.py        Settings (all environment variables)
│   ├── routes/          HTTP endpoints
│   ├── services/        Business logic (Gmail, Outlook, campaigns, CRM, billing, …)
│   ├── ai/              Classifier, reply generator, retrieval
│   ├── workers/         Scheduled jobs (mail polling, digests, reminders, social posts)
│   └── tests/
├── mobile/              Expo / React Native app
├── browser-extension/   Chrome extension
├── infra/migrations/    Base schema
├── migrations_v*.sql    Incremental migrations (run in order, v2 → v11)
├── scripts/             Asset generators (e.g. social banners)
├── docs/                API reference and deployment guide
└── .github/workflows/   CI and the daily social-post trigger
```

---

## Local development

```bash
git clone https://github.com/mailair-company/mailair.git
cd mailair
```

### Prerequisites

- Python 3.11+ and Node.js 20+
- A [Supabase](https://supabase.com) project
- An [Anthropic API key](https://console.anthropic.com)
- A Google Cloud project with the Gmail API enabled (and, optionally, an Azure app for Outlook)

### 1. Database

In the Supabase SQL editor, run `infra/migrations/001`–`004` in order, then `migrations_v2.sql` through `migrations_v11.sql` in order. (`003_sample_data.sql` is for development only.)

### 2. Backend

```bash
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # fill in the values below
uvicorn main:app --reload
# API: http://localhost:8000 · Swagger docs: http://localhost:8000/docs
```

### 3. Frontend

```bash
cd frontend
npm install
cp .env.local.example .env.local
npm run dev
# http://localhost:3000
```

### 4. Mobile (optional)

```bash
cd mobile
npm install
npx expo start
```

---

## Environment variables

### Backend (`backend/.env`)

All settings live in [`backend/config.py`](backend/config.py). The main ones:

| Variable | Required | Purpose |
|---|---|---|
| `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_KEY` | Yes | Database and auth |
| `ANTHROPIC_API_KEY` | Yes | Claude API |
| `SECRET_KEY` | Yes | Signing secret (32+ chars) |
| `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REDIRECT_URI` | For Gmail | Google OAuth |
| `MS_CLIENT_ID`, `MS_CLIENT_SECRET`, `MS_REDIRECT_URI` | For Outlook | Microsoft OAuth |
| `GCAL_CLIENT_ID`, `GCAL_CLIENT_SECRET`, `GCAL_REDIRECT_URI` | For Calendar | Google Calendar OAuth |
| `RESEND_API_KEY` | For campaigns | Campaign email delivery |
| `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`, `RAZORPAY_WEBHOOK_SECRET`, `RAZORPAY_PRO_PLAN_ID`, `RAZORPAY_AGENCY_PLAN_ID` | For billing | Subscriptions |
| `SLACK_WEBHOOK_URL` | No | Urgent-email alerts |
| `VAPID_PUBLIC_KEY`, `VAPID_PRIVATE_KEY` | No | Web push notifications |
| `FRONTEND_URL`, `BACKEND_URL`, `CORS_ORIGINS`, `ENVIRONMENT` | Yes in prod | Deployment URLs |
| `ZERNIO_*`, `SOCIAL_AUTOPOST_ENABLED`, `CRON_SECRET` | No | Daily social posting |

### Frontend (`frontend/.env.local`)

| Variable | Purpose |
|---|---|
| `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase client |
| `NEXT_PUBLIC_API_URL` | Backend URL |
| `NEXT_PUBLIC_RAZORPAY_KEY_ID` | Checkout |

---

## Deployment

- **Frontend:** Vercel, deployed on push to `main`.
- **Backend:** Render, defined in [`render.yaml`](render.yaml).
- **Scheduled jobs:** in-process APScheduler, plus a GitHub Actions cron ([`daily-social-post.yml`](.github/workflows/daily-social-post.yml)) that wakes the backend on Render's free tier.

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for the full guide.

---

## Contact

Built by the Mailair team — [mailair.company](https://mailair.company) · [support](https://mailair.company/support)

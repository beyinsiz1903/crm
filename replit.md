# Syroce CRM

A Customer Relationship Management system with website builder/template features for the hospitality industry.

## Templates

105 built-in templates, generated programmatically in `backend/templates_data.py`:
- **40 hotel** templates (segment=`hotel`, section `rooms`; some include optional `menu`)
- **35 restaurant** templates (segment=`restaurant`, section `menu`)
- **30 agency** templates (segment=`agency`, section `tours`)

Each template is standalone for its segment. Section types `menu` and `tours` are rendered in the frontend preview (`previewRenderer.js`) and in the backend HTML exporter (`export_service.py`). Multi-page export is segment-aware and emits `menu.html` / `tours.html` / `rooms.html` depending on what sections are present. Seed logic in `server.py` auto-reseeds built-ins when the stored count is below the generator target.

## Tech Stack

- **Frontend**: React 19 (CRA + CRACO), Tailwind CSS, Radix UI, React Router v7, Axios
- **Backend**: FastAPI (Python), Motor (async MongoDB driver), JWT auth (PyJWT + bcrypt)
- **Database**: MongoDB (Atlas)
- **Build**: Yarn (frontend), pip (backend)

## Project Structure

```
backend/        FastAPI server (server.py + routes modules)
frontend/       React app
  src/setupProxy.js   Dev proxy: /api -> localhost:8000
attached_assets/      Uploaded user assets
```

## Replit Setup

- **Frontend workflow**: runs CRACO dev server on port 5000 with host 0.0.0.0 and `DANGEROUSLY_DISABLE_HOST_CHECK=true` so the Replit iframe proxy works.
- **Backend workflow**: runs uvicorn on `0.0.0.0:8000`. Bound to 0.0.0.0 (not 127.0.0.1) so the workflow port checker can detect it.
- The frontend dev server proxies `/api/*` to the backend via `setupProxy.js`. `REACT_APP_BACKEND_URL` is intentionally empty so requests are relative.
- Backend startup is tolerant of MongoDB being unreachable: it pings with a 3s timeout and skips index/seed init on failure.

## Required Secrets

- `MONGO_URL` — MongoDB Atlas connection string (e.g. `mongodb://user:pass@host:27017/?ssl=true&...`). MongoDB Atlas IP whitelist must include `0.0.0.0/0` for Replit access.

## Optional Env Vars (in `backend/.env`)

- `DB_NAME` (default `syroce_crm`)
- `JWT_SECRET`
- `CORS_ORIGINS`

## Deployment

- Target: **VM** (single-process serving both frontend and API)
- Build: `cd frontend && yarn install && yarn build`
- Run: `cd backend && uvicorn server:app --host 0.0.0.0 --port 5000`
- In production the FastAPI app detects `frontend/build` and serves the SPA + static assets, with API routes under `/api`.

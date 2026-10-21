# Syroce hotel website CRM

Hotel website editor, CRM and immutable site publishing built with FastAPI,
MongoDB and React/Vite. This repository does not provision hosting, DNS, TLS or a
mail provider automatically.

## Local setup

Use Python 3.11+ and Node.js 24 with Yarn classic. Create a virtual environment
and install `backend/requirements-dev.txt`. Install frontend dependencies with
`cd frontend && yarn install --frozen-lockfile`.

Configure these backend environment variables (never commit real secrets):

| Variable | Purpose |
| --- | --- |
| `MONGO_URL` | Authenticated MongoDB connection string |
| `DB_NAME` | Database name |
| `JWT_SECRET` | Random secret of at least 32 characters, unique per environment |
| `PUBLIC_BASE_URL` | Public HTTPS origin, e.g. `https://sites.example.com`, no path |

Run `uvicorn server:app --host 127.0.0.1 --port 8000` from `backend`, and
`yarn start` from `frontend`. The development server proxies `/api` to port 8000.
For a remote development preview, set `DEV_ALLOWED_HOSTS` to the exact hostname;
do not disable host checking. Never expose the development server as production.
The first registration creates the administrator; subsequent public registrations
are blocked. Create other accounts through the team panel.

## Production deployment

1. Run `yarn build` in `frontend`; the backend serves `frontend/build`.
2. Run the backend behind an HTTPS reverse proxy and set `PUBLIC_BASE_URL`.
3. Persist and back up MongoDB and `backend/uploads`. Keep the JWT secret stable
   across workers/restarts. Restrict database access to application servers.
4. Replace sample hotel content/contact details, enter hotel-approved privacy
   information in editor settings, and configure a real HTTPS booking URL or
   an iframe supplied by the reservation provider.
5. Publish in the editor. A validated immutable release is created. Editing or
   autosaving the draft does not change the live site; republishing does.
   Published releases can be restored without overwriting the draft.
6. Verify the published HTTPS site, mobile navigation, forms and booking provider
   end-to-end on the actual production environment before accepting customers.

The managed site URL is `/api/hosted/{project_id}/index.html`. ZIP exports include
HTML, sitemap and robots metadata. Uploaded raster images are copied into exports;
optional external image bundling is bounded and blocks private network addresses.
ZIP forms require the configured, published backend to remain reachable. They are
not standalone email delivery or a reservation/payment engine.

## Operational limitations (explicit, not simulated)

- Contact and configured form submissions are stored in the Forms panel, with
  required-field validation and per-IP rate limiting. They do not send email.
- Reservation buttons redirect to a configured provider. Provider availability,
  payment and PMS synchronization require that provider's real integration tests.
- Custom domains/SSL and campaign delivery return configuration errors until a
  real infrastructure/provider implementation is installed; no random success,
  fabricated DNS records or fake sent counts are returned.
- Arbitrary scripts are not accepted. Google Analytics is opt-in and requires
  hotel-specific privacy text. Legal text must be reviewed by the hotel.
- Admin/editor/viewer access is enforced server-side. This CRM is one organization
  per deployment, not a tenant-isolated SaaS platform.

## Verification

From the repository root: `.venv/bin/pytest -q backend/tests` and
`.venv/bin/ruff check backend --select E9,F63,F7,F82`.
From `frontend`: `yarn test`, `yarn lint`, `yarn build`, `yarn audit`.
For Python dependencies: `pip-audit --strict -r backend/requirements.txt`.
CI treats tests, build, lint and dependency audit failures as failures.

The offline acceptance suite checks all 105 templates in both export modes,
unsafe inputs, authorization, immutable publication/rollback and form storage.
It uses disposable fake persistence by default. Set `TEST_MONGO_URL` to opt into
the real MongoDB integration test, which creates and removes only a uniquely
named test database. Passing tests is not evidence that production DNS, email,
booking/payments or a production deployment have been verified.

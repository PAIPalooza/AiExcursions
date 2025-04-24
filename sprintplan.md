---

# 🗓️ Agile Sprint Plan – *GeoVoyager*

## 👥 Team
- **Dev 1 (Lead)**: Backend/API, architecture, deployment
- **Dev 2**: Frontend UI/UX, voice integration, testing

---

## 🚦 Sprint 1: MVP Backend & POI Playback (2 Weeks)

### 🎯 Goals
- Set up backend and core data model in Supabase
- Build FastAPI endpoints for POIs and Tours
- Implement GPS-based POI detection logic
- Enable audio playback from AWS S3
- Mobile responsive voice-first UI (basic)

### ✅ Deliverables
- Supabase tables (users, POIs, tours)
- FastAPI endpoints for `GET/POST /pois`, `GET /tours`
- Location trigger prototype (browser geolocation)
- Basic frontend with GPS readout + S3 audio streaming
- Unit tests and Postman collection for endpoints

### 🧪 TDD Stories
- [x] Create POI API and validate GPS match within 20m radius
- [x] Validate user auth with Supabase JWT
- [x] Write test suite for `/pois` endpoint (CRUD + geofilter)

---

## 🚦 Sprint 2: Group Session Mode + Admin Dashboard (2 Weeks)

### 🎯 Goals
- Build group session sync (leader/follower roles)
- Use Supabase Realtime to sync current POI
- Implement admin upload panel (with auth)
- Support POI creation with image/audio upload (to S3)

### ✅ Deliverables
- Supabase `group_sessions`, `session_participants` tables
- FastAPI endpoints: `POST /sessions`, `PATCH /sessions/:id`
- Admin UI: Auth + POI upload (audio/image to S3)
- Realtime sync engine for group POI playback
- Test coverage for file upload, session start/join logic

### 🧪 TDD Stories
- [x] Session model: create, join, sync
- [x] Audio/image upload: MIME check, presigned S3
- [x] Group sync tests using Supabase Realtime mock

---

## 🚦 Sprint 3: Map UI + Playback UX Polish (2 Weeks)

### 🎯 Goals
- Render map with user location + POIs (Mapbox or Leaflet)
- Implement autoplay with distance threshold
- Voice fallback via Web Speech API for unsupported formats
- Improve mobile UI + offline UX

### ✅ Deliverables
- Interactive map w/ pins and location tracking
- Autoplay on geofence match (w/ cancel/pause/replay)
- Responsive mobile-first design with tailwind
- Fallback to Web TTS if audio file is missing
- Service worker for PWA-style offline use (optional)

### 🧪 TDD Stories
- [x] Geofence simulation tests (mock GPS drift)
- [x] Voice fallback UX tests
- [x] E2E test: Create POI → Assign to tour → Trigger voice playback

---

## 🚦 Sprint 4: Learning Layer, Analytics & Launch (2 Weeks)

### 🎯 Goals
- Add trivia/questions per POI
- Track user engagement (tours completed, POIs heard)
- Admin dashboard for analytics
- Deploy app to production (Vercel + S3)

### ✅ Deliverables
- New table: `quiz_questions`, `user_progress`
- Analytics dashboard (pageviews, POI play count)
- Admin dashboard: add/edit questions, view metrics
- Deploy backend (Fly.io or Railway) + frontend (Vercel)
- Beta release checklist, bug fix round

### 🧪 TDD Stories
- [x] Quiz engine: Randomize order, score answers
- [x] Track and persist progress with Supabase
- [x] Analytics queries (top POIs, top regions, drop-off rates)

---

## 🧩 Optional Future Sprints

- Gamified badges + rewards
- AI-generated voiceover using ElevenLabs or Polly
- Public API for 3rd-party excursion creators
- Bluetooth beacon integration for indoor museums

---

---

# 📋 Backlog – *GeoVoyager*

---

## 🧱 Epic 1: Core Infrastructure Setup

| Story ID | User Story | Points |
|----------|------------|--------|
| INF-1 | As a developer, I want to set up Supabase with tables for `users`, `pois`, and `tours` so that we can store location content. | 2 |
| INF-2 | As a developer, I want to configure a FastAPI backend project with auth middleware using Supabase JWT. | 2 |
| INF-3 | As a developer, I want to deploy the FastAPI backend to Railway with HTTPS enabled. | 1 |

---

## 📍 Epic 2: POI Management

| Story ID | User Story | Points |
|----------|------------|--------|
| POI-1 | As an admin, I want to create, update, and delete POIs via FastAPI endpoints so that I can manage locations. | 3 |
| POI-2 | As a user, I want to fetch a list of POIs near my GPS coordinates so I can hear content based on my location. | 3 |
| POI-3 | As a developer, I want to test geofence matching within a 20-meter radius to ensure accuracy. | 2 |

---

## 🔊 Epic 3: Audio Playback & Voice UI

| Story ID | User Story | Points |
|----------|------------|--------|
| VOICE-1 | As a user, I want audio narration to autoplay when I enter a POI's geofence. | 3 |
| VOICE-2 | As a developer, I want to support fallback to browser TTS if no audio file is found. | 2 |
| VOICE-3 | As an admin, I want to upload MP3 narration files to AWS S3 via the dashboard. | 2 |

---

## 🗺️ Epic 4: Mobile Interface + Map Integration

| Story ID | User Story | Points |
|----------|------------|--------|
| UI-1 | As a user, I want to see my real-time location and nearby POIs on a map. | 3 |
| UI-2 | As a developer, I want to use Mapbox or Leaflet to render an interactive map with POI markers. | 2 |
| UI-3 | As a user, I want to pause, skip, or replay narration from the UI. | 2 |

---

## 🧑‍🤝‍🧑 Epic 5: Group Session Sync

| Story ID | User Story | Points |
|----------|------------|--------|
| GROUP-1 | As a user, I want to create a group session and invite others with a session code. | 3 |
| GROUP-2 | As a participant, I want my device to stay in sync with the leader’s current POI. | 3 |
| GROUP-3 | As a developer, I want to implement Supabase Realtime to broadcast POI changes. | 2 |

---

## 🧠 Epic 6: Learning Layer & Quiz

| Story ID | User Story | Points |
|----------|------------|--------|
| QUIZ-1 | As an admin, I want to create trivia questions linked to POIs. | 2 |
| QUIZ-2 | As a user, I want to answer quiz questions and see correct answers immediately. | 3 |
| QUIZ-3 | As a developer, I want to persist quiz scores and progress per user. | 2 |

---

## 📊 Epic 7: Admin Dashboard & Analytics

| Story ID | User Story | Points |
|----------|------------|--------|
| ADMIN-1 | As an admin, I want a dashboard to view/edit POIs and upload content. | 3 |
| ADMIN-2 | As an admin, I want to see analytics like POI visits and tour completions. | 2 |
| ADMIN-3 | As a developer, I want to visualize POI engagement metrics via Supabase queries. | 2 |

---

## 🚀 Epic 8: Deployment, QA & Beta Launch

| Story ID | User Story | Points |
|----------|------------|--------|
| DEPLOY-1 | As a developer, I want to deploy the frontend to Vercel with proper env vars. | 1 |
| DEPLOY-2 | As a QA, I want to test the full tour experience with 3 users in a group. | 2 |
| DEPLOY-3 | As a team, I want to soft launch a beta with 10 real users and collect feedback. | 3 |

---

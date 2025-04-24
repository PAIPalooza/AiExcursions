---

# 📘 Product Requirements Document (PRD)

## 🧭 Overview

**Product Name**: *GeoVoyager*  
**Summary**: GeoVoyager is a mobile-responsive web app that enhances group excursions through **voice-guided, location-aware historical storytelling**. The platform detects user location via GPS, triggers context-aware content, and provides **hands-free playback** of regional history and facts. It’s powered by **FastAPI** for the backend, **Supabase** for authentication and database, and **AWS S3** for media hosting.

---

## 🎯 Goals

- Deliver immersive, GPS-triggered content during tours and excursions
- Enable mobile-first, voice-powered, low-friction user experience
- Synchronize tour content across groups for coordinated exploration
- Empower local historians to upload and manage content

---

## 🧑‍🤝‍🧑 Target Users

- Cultural tourists and local explorers
- Group travel organizers, schools, and educational institutions
- Local governments, museums, and heritage centers

---

## 🗺️ Key Features

### 📍 Geolocation-Based Triggers
- GPS location tracking on mobile browsers
- Geofenced points of interest (POIs) trigger voice content

### 🔊 Voice-Guided Storytelling
- Text-to-speech via browser APIs or uploaded audio files
- Autoplay triggered when entering proximity of POI

### 👫 Group Mode
- Group Leader assigns session ID; members sync tour state
- Real-time sync of current POI across group members via Supabase Realtime

### 🧭 Responsive Web App
- Built for mobile-first browsing (PWA optional)
- Interactive map with POI markers and route paths
- Option to pause, replay, or skip segments

### ✍️ Creator/Admin Panel
- FastAPI backend routes with Supabase-authenticated access
- Upload POI content: title, geo-coordinates, description, audio file
- Store media on AWS S3, track metadata in Supabase

### 📊 Analytics Dashboard
- POI engagement metrics per user/group
- Most visited locations and average tour durations

---

## 🏗️ Technical Architecture

### Frontend
- **Framework**: React with Tailwind CSS
- **Map SDK**: Mapbox GL JS or Leaflet.js
- **Voice**: Native Web Speech API or embedded MP3 playback

### Backend
- **Framework**: FastAPI
- **Auth**: Supabase Auth
- **Database**: Supabase PostgreSQL
- **Realtime**: Supabase Realtime channels (for group sync)
- **File Storage**: AWS S3 (for audio/image uploads)
- **Caching**: Redis (optional for location-to-POI matching)

---

## 🔐 Security & Compliance

- Supabase JWT-secured endpoints for all content APIs
- Authenticated upload only for admin users
- Location permissions only requested on tour start
- GDPR-compliant data handling and opt-in analytics

---

## 📅 Development Timeline

| Phase               | Deliverables                                       | Timeframe   |
|--------------------|----------------------------------------------------|-------------|
| Phase 1 - MVP      | POI model, GPS triggers, voice playback, 5 POIs   | Week 1–2    |
| Phase 2 - Admin UI | Content uploader with FastAPI+Supabase auth        | Week 3–4    |
| Phase 3 - Grouping | Group session sync using Supabase Realtime         | Week 5–6    |
| Phase 4 - Polish   | Map UI, offline fallback, mobile testing           | Week 7–8    |
| Phase 5 - Launch   | Bug fixes, deploy to Vercel + S3, soft launch      | Week 9–10   |

---

## 📈 Success Metrics

- ✅ 90% location-accuracy match rate for triggered content
- ✅ 80% user satisfaction via feedback form
- ✅ 50% repeat usage rate within 30 days
- ✅ <1% app crash or failure rate across devices

---

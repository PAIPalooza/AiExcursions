---

# 📊 Data Model – *GeoVoyager*

This data model includes all primary entities required for excursion tracking, POI management, group sync, and media integration.

---

## 📍 `points_of_interest`

| Field             | Type        | Description                                      |
|------------------|-------------|--------------------------------------------------|
| `id`             | UUID (PK)   | Unique identifier for the POI                    |
| `title`          | Text        | Name of the location or landmark                 |
| `description`    | Text        | Rich text or markdown content                   |
| `latitude`       | Float       | Latitude for GPS geofencing                     |
| `longitude`      | Float       | Longitude for GPS geofencing                    |
| `audio_url`      | Text        | Public S3 URL for the voice narration file      |
| `image_url`      | Text        | Optional image for the POI                      |
| `region`         | Text        | Region label (for filtering/sorting)            |
| `tags`           | Text[]      | Tags like `["historical", "museum", "park"]`    |
| `created_at`     | Timestamp   | Time of POI creation                            |
| `updated_at`     | Timestamp   | Last updated time                               |
| `created_by`     | UUID (FK)   | References `users.id` who created the POI       |

---

## 🔊 `tours`

| Field             | Type        | Description                                      |
|------------------|-------------|--------------------------------------------------|
| `id`             | UUID (PK)   | Unique identifier for the tour                   |
| `title`          | Text        | Title of the tour                                |
| `description`    | Text        | Overview or introduction                         |
| `poi_ids`        | UUID[]      | Ordered list of POIs included in the tour        |
| `estimated_time` | Integer     | Duration in minutes                              |
| `region`         | Text        | Geographic label                                 |
| `created_by`     | UUID (FK)   | Tour creator                                     |
| `created_at`     | Timestamp   | Created time                                     |

---

## 🧑 `users`

| Field          | Type        | Description                                      |
|---------------|-------------|--------------------------------------------------|
| `id`          | UUID (PK)   | User ID, from Supabase Auth                      |
| `email`       | Text        | Email address                                    |
| `role`        | Text        | `admin`, `tourist`, or `guide`                  |
| `display_name`| Text        | Optional name for group sync                     |
| `created_at`  | Timestamp   | Account creation date                            |

---

## 🧑‍🤝‍🧑 `group_sessions`

| Field          | Type        | Description                                      |
|---------------|-------------|--------------------------------------------------|
| `id`          | UUID (PK)   | Session ID used to sync users                    |
| `tour_id`     | UUID (FK)   | Associated tour being followed                   |
| `leader_id`   | UUID (FK)   | User who created the session                     |
| `status`      | Text        | `active`, `paused`, `ended`                      |
| `current_poi` | UUID (FK)   | Currently active POI being visited               |
| `started_at`  | Timestamp   | When the session began                           |
| `ended_at`    | Timestamp   | When the session was ended                       |

---

## 📍 `session_participants`

| Field          | Type        | Description                                      |
|---------------|-------------|--------------------------------------------------|
| `id`          | UUID (PK)   | Unique ID                                        |
| `session_id`  | UUID (FK)   | Belongs to `group_sessions.id`                   |
| `user_id`     | UUID (FK)   | Participant user                                 |
| `joined_at`   | Timestamp   | When user joined the session                     |

---

## 🧠 `quiz_questions` *(Optional – learning layer)*

| Field           | Type        | Description                                     |
|----------------|-------------|-------------------------------------------------|
| `id`           | UUID (PK)   | Unique ID                                       |
| `poi_id`       | UUID (FK)   | Linked POI                                      |
| `question`     | Text        | The question to display                         |
| `options`      | Text[]      | Multiple-choice options                         |
| `correct_index`| Integer     | Index of correct answer in `options[]`          |

---

## 📂 AWS S3 Object Structure

- **Bucket**: `geovoyager-media`
  - `/audio/{poi_id}.mp3`
  - `/images/{poi_id}.jpg`

You can optionally include an `s3_keys` table to map metadata if needed.

---

# Supabase Setup for GeoVoyager

## Database Schema

The GeoVoyager app uses Supabase for:
- User authentication and profiles
- Points of Interest (POIs) management
- Tour creation and management
- Live group sessions
- Real-time updates for group features

## Tables

1. `profiles` - User profiles extending Supabase auth
2. `pois` - Points of Interest with location data
3. `tours` - Collections of POIs forming a tour
4. `tour_pois` - Mapping of POIs to tours with sequence
5. `group_sessions` - Live tour session management
6. `session_participants` - Participants in group sessions

## Setup Instructions

1. Create a new Supabase project at https://app.supabase.com
2. Get your project URL and anon key from Settings > API
3. Run the initial migration:
   ```bash
   # From project root
   supabase init
   supabase link --project-ref your-project-ref
   supabase db push
   ```

## Features

- **Geofencing**: Using PostGIS for location-based queries
- **Real-time**: Enabled for group sessions and participants
- **RLS Policies**: Secure access control for all tables
- **Automatic timestamps**: Created/updated timestamps for all tables

## Environment Variables

Add these to your `.env` file:
```bash
SUPABASE_URL=your-project-url
SUPABASE_ANON_KEY=your-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```
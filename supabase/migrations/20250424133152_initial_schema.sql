-- Create users table (extends Supabase auth.users)
create table public.profiles (
  id uuid references auth.users primary key,
  username text unique,
  avatar_url text,
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Create points of interest table
create table public.pois (
  id uuid primary key default uuid_generate_v4(),
  title text not null,
  description text,
  latitude double precision not null,
  longitude double precision not null,
  audio_url text,
  created_by uuid references public.profiles(id),
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Create tours table
create table public.tours (
  id uuid primary key default uuid_generate_v4(),
  title text not null,
  description text,
  created_by uuid references public.profiles(id),
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  updated_at timestamp with time zone default timezone('utc'::text, now()) not null
);

-- Create tour_pois table for mapping POIs to tours with sequence
create table public.tour_pois (
  tour_id uuid references public.tours(id) on delete cascade,
  poi_id uuid references public.pois(id) on delete cascade,
  sequence_number integer not null,
  primary key (tour_id, poi_id)
);

-- Create group_sessions table for live tours
create table public.group_sessions (
  id uuid primary key default uuid_generate_v4(),
  tour_id uuid references public.tours(id),
  leader_id uuid references public.profiles(id),
  current_poi_id uuid references public.pois(id),
  session_code text unique not null,
  status text not null check (status in ('active', 'completed', 'cancelled')),
  created_at timestamp with time zone default timezone('utc'::text, now()) not null,
  ended_at timestamp with time zone
);

-- Create session_participants table
create table public.session_participants (
  session_id uuid references public.group_sessions(id) on delete cascade,
  user_id uuid references public.profiles(id) on delete cascade,
  joined_at timestamp with time zone default timezone('utc'::text, now()) not null,
  left_at timestamp with time zone,
  primary key (session_id, user_id)
);

-- Create RLS policies
alter table public.profiles enable row level security;
alter table public.pois enable row level security;
alter table public.tours enable row level security;
alter table public.tour_pois enable row level security;
alter table public.group_sessions enable row level security;
alter table public.session_participants enable row level security;

-- Profiles policies
create policy "Public profiles are viewable by everyone"
  on public.profiles for select
  using (true);

create policy "Users can insert their own profile"
  on public.profiles for insert
  with check (auth.uid() = id);

create policy "Users can update own profile"
  on public.profiles for update
  using (auth.uid() = id);

-- POIs policies
create policy "POIs are viewable by everyone"
  on public.pois for select
  using (true);

create policy "Authenticated users can create POIs"
  on public.pois for insert
  with check (auth.role() = 'authenticated');

create policy "POI creators can update their POIs"
  on public.pois for update
  using (auth.uid() = created_by);

-- Tours policies
create policy "Tours are viewable by everyone"
  on public.tours for select
  using (true);

create policy "Authenticated users can create tours"
  on public.tours for insert
  with check (auth.role() = 'authenticated');

create policy "Tour creators can update their tours"
  on public.tours for update
  using (auth.uid() = created_by);

-- Create indexes for performance
create index pois_location_idx on public.pois using gist (
  ll_to_earth(latitude, longitude)
);
create index tour_pois_tour_id_idx on public.tour_pois(tour_id);
create index tour_pois_sequence_idx on public.tour_pois(tour_id, sequence_number);
create index group_sessions_code_idx on public.group_sessions(session_code);

-- Create functions for geofencing
create or replace function public.pois_within_radius(
  lat double precision,
  lng double precision,
  radius_meters int
) returns setof public.pois
language sql
as $$
  select *
  from public.pois
  where earth_distance(
    ll_to_earth(latitude, longitude),
    ll_to_earth(lat, lng)
  ) <= radius_meters;
$$;

-- Enable realtime subscriptions for group features
alter publication supabase_realtime add table public.group_sessions;
alter publication supabase_realtime add table public.session_participants;

-- Trigger for updating timestamps
create or replace function public.handle_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

create trigger handle_profiles_updated_at
  before update on public.profiles
  for each row
  execute procedure public.handle_updated_at();

create trigger handle_pois_updated_at
  before update on public.pois
  for each row
  execute procedure public.handle_updated_at();

create trigger handle_tours_updated_at
  before update on public.tours
  for each row
  execute procedure public.handle_updated_at();
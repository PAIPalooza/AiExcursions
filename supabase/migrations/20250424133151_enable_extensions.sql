-- Enable required extensions
create extension if not exists "uuid-ossp";
create extension if not exists postgis;
create extension if not exists postgis_topology;
create extension if not exists earthdistance cascade;
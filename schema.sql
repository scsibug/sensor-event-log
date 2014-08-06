create extension if not exists hstore;

-- Agents authenticate and publish data to the collector
create table agents (
  id serial primary key,
  name text unique not null,
  signing_key text,
  description text,
  created timestamp with time zone,
  attr hstore -- agent metadata
);

-- Sensors interact with the environment to read values/detect change
create table sensors (
  id serial primary key,
  agent serial references agents(id), -- which agent created this sensor?
  name text,
  units text, -- "count", "celsius", "seconds", "event"; some indication of what a reading means
  description text, -- human readable description of the sensor
  coalesce boolean, -- should we attempt to coalesce identical readings into the same row?
  created timestamp with time zone, -- when the reading occurred
  attr hstore -- sensor metadata
);

-- Store numeric or discrete (event) samples from a sensor
create table samples (
  id bigserial primary key,
  sensor serial references sensors(id),
  tstamp timestamp with time zone,
  numeric_val numeric, -- sample from a numeric sensor
  event text, -- event or state from a discrete sensor
  last_seen timestamp with time zone, -- for coalesced sensors, when was the last time we saw this value?
  times_seen integer, -- how many readings have been sent with this same value?
  attr hstore -- sample metadata
);


-- Store details about monitoring points
create table monitor_points (
  id serial primary key,
  name text unique not null,
  units text, -- units for the recorded data points.  May be null for unitless event.
  description text
);

-- Store values and events recorded at monitoring points.
create table point_values (
  id serial primary key,
  monitor_point serial references monitor_points(id),
  numeric_val numeric, -- sample from a sensor
  event text, -- event identifier
  tstamp timestamp with time zone
);

-- Store events recorded at monitoring points
--create table point_events (
--  id serial primary key,
--  monitor_point serial references monitor_points(id),
--  event text,
--  tstamp timestamp with time zone
--);
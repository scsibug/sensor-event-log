CREATE extension IF NOT EXISTS hstore;

-- simple table for testing
CREATE TABLE supersimple (
  id serial primary key,
  created timestamp with time zone,
  reading numeric
);


sensor-event-log
================

Logging events from sensors on remote machines.

This is a simple server that receives values (such as temperature or
humidity readings) and events (such as motion detection or door
open/close) and persists them to a database.

Requirements
================

Twisted (14.0.0)

Protocol
================

We assume that the values/events sent are not sensitive, and only care
about authenticity/integrity of messages from clients.  An HMAC
generated from a shared secret is used to verify messages before they
are accepted into the database.

Messages are in JSON.  Sample messages below.  Authentication is
through an HTTP Authorization header which contains the string "HMAC "
concatenated with the HMAC of the shared secret and the message
content.  We aren't worried about replay attacks, because each message
has a timestamp, messages with duplicate value/events for the same
timestamp can be ignored.

Sample event:

{
  "type": "event",
  "monitor_point": "rpi.door.1",
  "event": "open",
  "timestamp": "1403407813.868718"
}

Sample value:

{
  "type": "value",
  "monitor_point": "rpi.tempsoc.1",
  "value": "23.39",
  "timestamp": "1403407813.868718"
}
# -*- encoding: utf-8 -*-
$:.push File.expand_path("../lib", __FILE__)

Gem::Specification.new do |s|
  s.name        = "fluent-plugin-sensordb"
  s.version     = "0.0.1"
  s.authors     = ["Greg Heartsfield"]
  s.email       = ["glh@eml.cc"]
  s.homepage    = "https://github.com/scsibug/sensor-event-log"
  s.summary     = %q{Output sensor data to a PostgreSQL database}
  s.description = %q{Output sensor data to a PostgreSQL database}

#  s.rubyforge_project = "fluent-plugin-pghstore"

  s.files         = ["lib/fluent/plugin/out_sensordb.rb"]
  s.require_paths = ["lib"]

  # specify any dependencies here; for example:
  s.add_development_dependency "rspec"
  # s.add_runtime_dependency "rest-client"
  s.add_development_dependency "fluentd"
  s.add_development_dependency "pg"
  s.add_runtime_dependency "fluentd"
  s.add_runtime_dependency "pg"
end

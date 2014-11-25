class Fluent::SensorDBOutput < Fluent::BufferedOutput
  Fluent::Plugin.register_output('sensordb', self)

  config_param :database, :string
  config_param :table, :string, :default => 'fluentd_store'
  config_param :host, :string, :default => 'localhost'
  config_param :port, :integer, :default => 5432
  config_param :user, :string, :default => nil
  config_param :password, :string, :default => nil

  def initialize
    super
    log.info "initializing sensordb 0.0.1"
    require 'pg'
    require 'time'
  end

  def start
    super
  end

  def shutdown
    super
    if @conn != nil and @conn.finished?() == false
      conn.close()
    end
  end
  
  def format(tag, time, record)
    #log.info "format called"
    #log.info "#{tag}, #{time}, #{record}"
    [tag, time, record].to_msgpack
  end

  def write(chunk)
    r = 0
    beginning_time = Time.now()
    conn = get_connection()
    return if conn == nil  # TODO: chunk will be dropped. should retry?
    @conn.transaction do |conn|
      chunk.msgpack_each {|(tag, time_str, record)|
        begin
          r=r+1
          # Determine what type of message this is.
          mtype = record["msg_type"]
          if (mtype == nil or mtype == "sample")
            log.info "SAMPLE message"
            record_sample(conn, time_str, record)
          elsif (mtype == "sensor_metadata")
            log.info "SENSOR METADATA message"
            record_metadata(conn, time_str, record)
          elsif (mtype == "heartbeat")
            log.info "HEARTBEAT message"
            record_heartbeat(conn, time_str, record)
          else
            log.error "Unknown message type #{mtype}"
          end
          # time is a unix integer, convert this into 8601 format
          isotime = Time.at(time_str).iso8601
          conn.exec_params('INSERT INTO supersimple (created, reading) VALUES ($1, $2)', [isotime, record["value"]])
        rescue PGError => e 
          log.error "PGError: " + e.message  # dropped if error
        end
      }
    end
    conn.close()
    end_time = Time.now()
    elapsed_ms = (end_time - beginning_time)*1000
    log.info "Time elapsed #{(end_time - beginning_time)*1000}ms"
    log.info "  Wrote #{r} records, #{elapsed_ms/r}ms per record"
    log.info "  This is #{(r/elapsed_ms)*1000} rows/sec"
  end

  def record_sample(conn, time_str, record)
    log.info "sample metadata received, ignoring for now"
    log.info "time was #{time_str}"
  end

  def record_metadata(conn, time_str, record)
    log.info "sensor metadata received, ignoring for now"
  end

  def record_heartbeat(conn, time_str, record)
    log.info "heartbeat received, ignoring for now"
  end

  def get_connection()
    if @conn != nil and @conn.finished?() == false
      return @conn  # connection is alived
    end

    begin
        @conn = PG.connect(:dbname => @database, :host => @host, :port => @port,
                           :user => @user, :password => @password)
        @conn.exec("SET synchronous_commit = on")

    rescue PGError => e
      log.error "Error: could not connect database:" + @database
      return nil
    end

    return @conn
  end
end

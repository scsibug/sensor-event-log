package com.gregheartsfield.sel.collector.dao;

import com.gregheartsfield.sel.collector.core.Agent;
import org.skife.jdbi.v2.tweak.ResultSetMapper;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.HashMap;
import org.skife.jdbi.v2.StatementContext;

// Transform Result sets from queries on the "agent" table into Agent objects
public class AgentMapper implements ResultSetMapper<Agent> {
	public Agent map(int index, ResultSet r, StatementContext ctx) throws SQLException {
		return new Agent(r.getLong("id"),
										 r.getString("name"),
										 r.getString("description"),
										 r.getTimestamp("created"),
										 r.getBoolean("active"),
										 (HashMap<String,String>)r.getObject("attr")
										 );
	}
}

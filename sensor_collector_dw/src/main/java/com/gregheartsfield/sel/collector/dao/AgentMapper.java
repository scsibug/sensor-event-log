package com.gregheartsfield.sel.collector.dao;

import com.gregheartsfield.sel.collector.core.Agent;
import org.skife.jdbi.v2.tweak.ResultSetMapper;
import java.sql.ResultSet;
import java.sql.SQLException;
import org.skife.jdbi.v2.StatementContext;

public class AgentMapper implements ResultSetMapper<Agent> {
	public Agent map(int index, ResultSet r, StatementContext ctx) throws SQLException {
		return new Agent(r.getLong("id"), r.getString("name"));
	}
}

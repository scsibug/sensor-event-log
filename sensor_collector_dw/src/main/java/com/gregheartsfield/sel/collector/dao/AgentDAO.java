package com.gregheartsfield.sel.collector.dao;

import org.skife.jdbi.v2.sqlobject.SqlQuery;
import java.util.List;

public interface AgentDAO {
	@SqlQuery("select name from agents where active=true")
	List<String> findActiveAgents();

	void close();
}

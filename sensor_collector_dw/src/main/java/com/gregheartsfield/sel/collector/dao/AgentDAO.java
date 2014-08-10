package com.gregheartsfield.sel.collector.dao;

import org.skife.jdbi.v2.sqlobject.SqlQuery;
import org.skife.jdbi.v2.sqlobject.customizers.Mapper;
import java.util.List;
import com.gregheartsfield.sel.collector.core.Agent;

public interface AgentDAO {
	@SqlQuery("select id, name from agents where active=true")
	@Mapper(AgentMapper.class)
	List<Agent> findActiveAgents();

	void close();
}

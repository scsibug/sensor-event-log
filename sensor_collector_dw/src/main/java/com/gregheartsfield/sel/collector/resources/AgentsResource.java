package com.gregheartsfield.sel.collector.resources;

import com.gregheartsfield.sel.collector.core.Agent;
import com.gregheartsfield.sel.collector.dao.AgentDAO;
import com.google.common.base.Optional;
import com.codahale.metrics.annotation.Timed;

import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.MediaType;
import java.util.List;
import java.util.Vector;

@Path("/agents")
@Produces(MediaType.APPLICATION_JSON)
public class AgentsResource {
	private final AgentDAO agentdao;
	public AgentsResource(AgentDAO agentdao) {
		this.agentdao = agentdao;
	}
    @GET
    @Timed
    public List<Agent> listAgents() {
			// Retrieve agents from database
			return agentdao.findActiveAgents();
			//			Vector<Agent> v = new Vector<Agent>();
			//			v.add(new Agent(1L, "test"));
			//			return v;
    }
}

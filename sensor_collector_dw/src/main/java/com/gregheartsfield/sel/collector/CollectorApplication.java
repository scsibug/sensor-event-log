package com.gregheartsfield.sel.collector;

import io.dropwizard.Application;
import io.dropwizard.setup.Bootstrap;
import io.dropwizard.setup.Environment;
import io.dropwizard.jdbi.DBIFactory;
import org.skife.jdbi.v2.DBI;
import com.gregheartsfield.sel.collector.resources.HelloWorldResource;
import com.gregheartsfield.sel.collector.resources.AgentsResource;
import com.gregheartsfield.sel.collector.dao.AgentDAO;
import com.gregheartsfield.sel.collector.health.TemplateHealthCheck;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class CollectorApplication extends Application<CollectorConfiguration> {
	private static final Logger log = LoggerFactory.getLogger(CollectorApplication.class);
	public static void main(String[] args) throws Exception {
		new CollectorApplication().run(args);
	}

	@Override
    public String getName() {
		return "collector";
	}

	@Override
    public void initialize(Bootstrap<CollectorConfiguration> bootstrap) {
		log.info("initializing application...");
		// nothing to do yet
	}

	@Override
		public void run(CollectorConfiguration configuration,
										Environment environment) throws Exception {
		// Setup Database
		log.info("Setting up database");
		final DBIFactory factory = new DBIFactory();
		final DBI jdbi = factory.build(environment, configuration.getDataSourceFactory(), "postgresql");
		
		// Initialize DAOs
		log.info("Initializing DAOs");
		final AgentDAO agentdao = jdbi.onDemand(AgentDAO.class);
		
		log.info("Creating resources");
		/******* Create Resources *******/
		/** Agents Resource
		 * List all agents that currently exist
		 * TODO: Allow creation of new agents
		 */
		AgentsResource agents_resource = new AgentsResource(agentdao);
		
		/** Agent Resource
		 * Provide details about specific agents,
		 * particularly what sensors they own.
		 * Allow creation of 
		 */
		
		/** Sensors Resource
		 * List all sensors that currently exist
		 */
		
		// Create Health Checks
		//			final TemplateHealthCheck healthCheck =
		//        new TemplateHealthCheck(configuration.getTemplate());
		
		// Register Health Checks
		//environment.healthChecks().register("template", healthCheck);
		
		log.info("Registering resources with Jersey");
		// Register Resources
		environment.jersey().register(agents_resource);
	}
}

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

public class CollectorApplication extends Application<CollectorConfiguration> {
    public static void main(String[] args) throws Exception {
        new CollectorApplication().run(args);
    }

    @Override
    public String getName() {
        return "collector";
    }

    @Override
    public void initialize(Bootstrap<CollectorConfiguration> bootstrap) {
        // nothing to do yet
    }

		@Override
			public void run(CollectorConfiguration configuration,
											Environment environment) throws Exception {
			// Setup Database
			final DBIFactory factory = new DBIFactory();
			final DBI jdbi = factory.build(environment, configuration.getDataSourceFactory(), "postgresql");

			// Initialize DAOs
			final AgentDAO agentdao = jdbi.onDemand(AgentDAO.class);

			// Create Resources
			final HelloWorldResource demoResource = new HelloWorldResource(
																																 configuration.getTemplate(),
																																 configuration.getDefaultName()
																																 );


			// Create Health Checks
			final TemplateHealthCheck healthCheck =
        new TemplateHealthCheck(configuration.getTemplate());

			// Register Health Checks
			environment.healthChecks().register("template", healthCheck);

			// Register Resources
			environment.jersey().register(new AgentsResource(agentdao));
			environment.jersey().register(demoResource);
		}
}

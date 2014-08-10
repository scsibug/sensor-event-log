package com.gregheartsfield.sel.collector;

import io.dropwizard.Application;
import io.dropwizard.setup.Bootstrap;
import io.dropwizard.setup.Environment;
import io.dropwizard.jdbi.DBIFactory;
import org.skife.jdbi.v2.DBI;
import com.gregheartsfield.sel.collector.resources.HelloWorldResource;
import com.gregheartsfield.sel.collector.resources.AgentsResource;
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
											Environment environment) {
			final HelloWorldResource demoResource = new HelloWorldResource(
																																 configuration.getTemplate(),
																																 configuration.getDefaultName()
																																 );
			final AgentsResource agentsResource = new AgentsResource();
			final TemplateHealthCheck healthCheck =
        new TemplateHealthCheck(configuration.getTemplate());

			final DBIFactory factory = new DBIFactory();

			try {
				final DBI jdbi = factory.build(environment, configuration.getDataSourceFactory(), "postgresql");
			} catch (ClassNotFoundException cnf) {
				// add logging / this is fatal
			}
			//final UserDAO dao = jdbi.onDemand(UserDAO.class);
			//environment.jersey().register(new UserResource(dao));

			environment.healthChecks().register("template", healthCheck);
			environment.jersey().register(demoResource);
			environment.jersey().register(agentsResource);
		}
}

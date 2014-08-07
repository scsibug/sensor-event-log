package com.gregheartsfield.sel.collector;

import io.dropwizard.Application;
import io.dropwizard.setup.Bootstrap;
import io.dropwizard.setup.Environment;
import com.gregheartsfield.sel.collector.resources.HelloWorldResource;
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
			final HelloWorldResource resource = new HelloWorldResource(
																																 configuration.getTemplate(),
																																 configuration.getDefaultName()
																																 );
			final TemplateHealthCheck healthCheck =
        new TemplateHealthCheck(configuration.getTemplate());
			environment.healthChecks().register("template", healthCheck);
			environment.jersey().register(resource);
		}
}

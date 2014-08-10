package com.gregheartsfield.sel.collector;

import io.dropwizard.Configuration;
import com.fasterxml.jackson.annotation.JsonProperty;
import org.hibernate.validator.constraints.NotEmpty;
import io.dropwizard.db.DataSourceFactory;

public class CollectorConfiguration extends Configuration {

	@JsonProperty
	private DataSourceFactory database = new DataSourceFactory();

	//	@NotEmpty
	//	private String defaultName = "Stranger";

	@JsonProperty
	public DataSourceFactory getDataSourceFactory() {
		return database;
	}
}

package com.gregheartsfield.sel.collector;

import io.dropwizard.Configuration;
import com.fasterxml.jackson.annotation.JsonProperty;
import org.hibernate.validator.constraints.NotEmpty;
import io.dropwizard.db.DataSourceFactory;

public class CollectorConfiguration extends Configuration {

	@JsonProperty
	private DataSourceFactory database = new DataSourceFactory();

	@NotEmpty
	private String template;

	@NotEmpty
	private String defaultName = "Stranger";

	@JsonProperty
	public String getTemplate() {
		return template;
	}

	@JsonProperty
	public void setTemplate(String template) {
		this.template = template;
	}

	@JsonProperty
	public String getDefaultName() {
		return defaultName;
	}

	@JsonProperty
	public void setDefaultName(String name) {
		this.defaultName = name;
	}

	@JsonProperty
	public DataSourceFactory getDataSourceFactory() {
		return database;
	}
}

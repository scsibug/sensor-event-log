package com.gregheartsfield.sel.collector.core;

import com.fasterxml.jackson.annotation.JsonProperty;
import org.hibernate.validator.constraints.Length;

public class Agent {
	private long id;

	private String name;

	public Agent() {
		// Jackson deserialization
	}
	
	public Agent(long id, String name) {
		this.id = id;
		this.name = name;
	}

	@JsonProperty
	public long getId() {
		return id;
	}

	@JsonProperty
	public String getName() {
		return name;
	}
}

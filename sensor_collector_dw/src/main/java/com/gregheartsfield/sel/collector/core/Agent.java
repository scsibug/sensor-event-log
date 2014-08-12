package com.gregheartsfield.sel.collector.core;

import com.fasterxml.jackson.annotation.JsonProperty;
import org.hibernate.validator.constraints.Length;
import java.sql.Timestamp;
import java.util.HashMap;

public class Agent {
	private long id;
	private String name;
	private String description;
	private Timestamp created;
	private Boolean active;

	private HashMap<String,String> attr;

	public Agent() {
		// Jackson deserialization
	}
	
	public Agent(long id, String name, String description, Timestamp created, Boolean active, HashMap<String,String> attr) {
		this.id = id;
		this.name = name;
		this.description = description;
		this.created = created;
		this.active = active;
		this.attr = attr;
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

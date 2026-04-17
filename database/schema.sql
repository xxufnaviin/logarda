CREATE TABLE metrics (
    metricTime TIMESTAMP NOT NULL,
    instanceID VARCHAR NOT NULL,
    cpu DOUBLE PRECISION NOT NULL,
    network DOUBLE PRECISION NOT NULL,
    memory DOUBLE PRECISION NOT NULL, 
    
    PRIMARY KEY (metricTime, instance_id) --composite primary key to prevent double entries at same timestamp for single instance
);

CREATE TABLE predicted_metrics (
    metricTime TIMESTAMP NOT NULL,
    instanceID VARCHAR NOT NULL,
    cpu DOUBLE PRECISION NOT NULL,
    network DOUBLE PRECISION NOT NULL,
    memory DOUBLE PRECISION NOT NULL, 
    
    PRIMARY KEY (metricTime, instance_id) --composite primary key to prevent double entries at same timestamp for single instance
);

CREATE TABLE logs (
    eventTime TIMESTAMP NOT NULL,
    errorCode VARCHAR NOT NULL,-- only store error logs
    errorMessage TEXT NOT NULL,
    serviceName VARCHAR NOT NULL,
    eventName VARCHAR NOT NULL
);
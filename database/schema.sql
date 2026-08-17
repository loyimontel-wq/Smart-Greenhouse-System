CREATE DATABASE greenhouses;  

USE greenhouses;  


CREATE TABLE sensor_data (
    id INT AUTO_INCREMENT PRIMARY KEY,  
    sensor_type VARCHAR(50),             -- e.g., soil, ultrasonic, pir, dht, ldr
    value1 FLOAT,                       -- Primary reading (moisture %, temp, distance, etc.)
    value2 FLOAT,                       -- Secondary reading (raw ADC, humidity, etc.)
    status VARCHAR(50),                 
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP  -- Auto-generated time of insertion
);
CREATE DATABASE IF NOT EXISTS greenhouses;
USE greenhouses;
CREATE TABLE workers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(100),
    employee_id VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(30),
    role VARCHAR(50),
    username VARCHAR(50) UNIQUE NOT NULL,      -- Add UNIQUE constraint
    password VARCHAR(255) NOT NULL             -- Store hashed passwords in production
);

-- Insert default admin user (password stored as plain text for demo only)
INSERT INTO workers (fullname,employee_id,email,phone,role,username,password
) VALUES ('System Administrator','ADMIN001','admin@greenhouse.com','0000000000','Administrator','admin','admin');

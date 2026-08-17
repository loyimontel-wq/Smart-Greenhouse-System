# Smart Greenhouse Monitoring System

An IoT-based automated greenhouse monitoring system using an ESP32 microcontroller, multiple sensors, a Flask web server, and a MySQL database.

## Features
- **Light tracking:** Uses LDR sensors to monitor light intensity for automated lighting control.
- **Water level monitoring:** Ultrasonic sensor measures water tank levels with buzzer alerts.
- **Environmental sensing:** DHT22 sensor measures temperature and humidity.
- **Soil moisture monitoring:** Capacitive sensor measures soil moisture percentage.
- **Intrusion detection:** PIR sensor detects motion and activates a buzzer alarm.
- **Web dashboard:** Real-time sensor data visualization with historical graphs.
- **Data logging:** MySQL database stores all sensor readings with timestamps.

## Technologies Used
- **Microcontroller:** ESP32 (Wemos D1 R32)
- **Sensors:** LDR, HC-SR04, DHT22, Capacitive Soil Moisture, PIR
- **Actuators:** Servo motor, 2x buzzers, LCD 16x2 (I2C)
- **Backend:** Python Flask
- **Database:** MySQL
- **Frontend:** HTML, CSS, JavaScript (AJAX)
- **IDE:** Arduino IDE

## Hardware Setup
- ESP32 powered via laptop USB (primary) with solar-charged battery backup.
- All sensors connected to ESP32 GPIO pins.

## Software Setup
1. Install Arduino IDE and add ESP32 board support.
2. Install required libraries: DHT, LiquidCrystal I2C, ESP32Servo, ArduinoJson.
3. Upload the code from `/esp32_firmware/` to the ESP32.
4. Install Python dependencies: `pip install -r requirements.txt`.
5. Set up MySQL database using the schema in `/database/schema.sql`.
6. Run the Flask server: `python app.py`.
7. Access the dashboard at `http://localhost:5000`.

## Project Structure
Smart-Greenhouse-System/
├── esp32_firmware/ # ESP32 Arduino code
├── flask_backend/ # Flask server and web dashboard
├── database/ # SQL schema
├── hardware/ # Circuit diagrams and wiring
├── docs/ # Report and images
└── README.md


## Author
**Loyiso Ndotho** – https://github.com/loyimontel-wq

## Acknowledgments
- Vaal University of Technology – Department of Electrical Engineering
- Supervisor: Mr. D.F Ojo-Seriki

version: '3'
services:
  mosquitto:
    image: eclipse-mosquitto
    container_name: mosquitto
    ports:
      - "1883:1883"  # MQTT port
      - "9001:9001"  # WebSockets port
    volumes:
      - ./mosquitto/config:/mosquitto/config
      - ./mosquitto/data:/mosquitto/data
      - ./mosquitto/log:/mosquitto/log
    networks:
      - mqtt_network

networks:
  mqtt_network:

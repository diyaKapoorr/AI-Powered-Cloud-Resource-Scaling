import wmi
import psutil
import time
import datetime
import requests  # For sending data to Node-RED

# Function to simulate temperature (as not all systems provide this)
def get_cpu_temp_wmi():
    w = wmi.WMI(namespace="root\\OpenHardwareMonitor")
    temperature_info = w.Sensor()
    for sensor in temperature_info:
        if sensor.SensorType == "Temperature" and "CPU" in sensor.Name:
            return sensor.Value  # Returns temperature in °C

# Function to get network bandwidth usage (in Mbps)
def get_network_bandwidth():
    net_io = psutil.net_io_counters()
    return net_io.bytes_sent / 1024 / 1024 * 8  # Convert bytes sent to Mbps

# URL for Node-RED endpoint
url = 'http://localhost:1880/metrics'  # Update this to match your Node-RED endpoint

# Initialize the starting timestamp (01-01-2022 00:00:00)
timestamp = datetime.datetime(2022, 1, 1, 0, 0, 0)

# Loop to collect data every simulated hour
while True:
    # Get current CPU, memory, battery usage
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    battery = psutil.sensors_battery()
    battery_level = battery.percent if battery else None
    temperature = get_cpu_temp_wmi()
    network_bandwidth = get_network_bandwidth()

    # Create data dictionary to send to Node-RED
    data = {
        "timestamp": timestamp.isoformat(),
        "temperature": temperature,
        "cpu_usage": cpu_usage,
        "memory_usage": memory_usage,
        "battery_level": battery_level,
        "network_bandwidth": network_bandwidth,
    }

    # Print the collected metrics
    print(f"Timestamp: {timestamp}")
    print(f"Temperature: {temperature:.2f} °C" if temperature else "Temperature: N/A")
    print(f"CPU Usage: {cpu_usage}%")
    print(f"Memory Usage: {memory_usage}%")
    print(f"Battery Level: {battery_level}%" if battery_level is not None else "Battery Level: N/A")
    print(f"Network Bandwidth Usage: {network_bandwidth:.2f} Mbps")
    print("------------------------------------------------------------")

    # Send data to Node-RED
    try:
        response = requests.post(url, json=data)
        print(f"Sent to Node-RED: {response.status_code}")
    except Exception as e:
        print(f"Error sending data to Node-RED: {e}")

    # Increment the timestamp by 1 hour
    timestamp += datetime.timedelta(hours=1)

    # Wait for 2 seconds before simulating the next hour (for demonstration)
    time.sleep(2)

from rplidar import RPLidar

PORT_NAME = '/dev/ttyUSB0'
MIN_DISTANCE = 5000  # Minimum distance for object detection in cm

def check_object_presence(scan):
    for _, angle, distance in scan:
        if ((0 <= angle <= 30) or (330 <= angle <= 360)) and (distance < MIN_DISTANCE):
            return True
    return False

def run():
    lidar = RPLidar(PORT_NAME)
    try:
        iterator = lidar.iter_scans()
        for scan in iterator:
            if check_object_presence(scan):
                print("Object detected in specified angles (0-30 degrees and 330-360 degrees) at a distance less than 5cm")
    except KeyboardInterrupt:
        print("Stopping...")
    lidar.stop()
    lidar.disconnect()

if __name__ == '__main__':
    run()

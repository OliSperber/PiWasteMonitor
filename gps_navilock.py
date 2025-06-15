import serial
import pynmea2

class GPSNaviLock:
    def __init__(self, port="/dev/ttyUSB0", baudrate=4800):
        self.port = port
        self.baudrate = baudrate

    def get_coords(self):
        try:
            with serial.Serial(self.port, self.baudrate, timeout=1) as ser:
                while True:
                    line = ser.readline().decode('ascii', errors='replace')
                    if line.startswith('$GPGGA'):
                        msg = pynmea2.parse(line)
                        lat = self._convert_to_decimal(msg.lat, msg.lat_dir)
                        lon = self._convert_to_decimal(msg.lon, msg.lon_dir)
                        return lat, lon
        except Exception as e:
            print(f"GPS fout: {e}")
            # fallback coords of choice:
            return 0.0, 0.0

    def _convert_to_decimal(self, raw_value, direction):
        if not raw_value:
            return 0.0
        degrees = int(float(raw_value) / 100)
        minutes = float(raw_value) - degrees * 100
        dec = degrees + minutes / 60
        if direction in ['S', 'W']:
            dec *= -1
        return dec

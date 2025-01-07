import serial
import time

# Configure the serial connection (adjust COM port and baud rate as per your machine's settings)
ser = serial.Serial(
    port='COM3',  # Replace with your COM port or '/dev/ttyUSB0' on Linux
    baudrate=9600,  # Replace with the baud rate of your machine
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1  # Timeout in seconds
)

def get_sartorius_result():
    try:
        # Ensure the serial port is open
        if not ser.is_open:
            ser.open()

        # Command to request data from Sartorius machine (check machine manual for correct command)
        ser.write(b'REQUEST_DATA\r\n')

        # Read data from the machine
        time.sleep(0.5)  # Wait for a response
        response = ser.readline().decode('latin-1').strip()

        # Process the response
        if response:
            print("Sartorius Machine Result:", response)
        else:
            print("No data received from the Sartorius machine.")
    
    except serial.SerialException as e:
        print("Serial error:", e)
    
    finally:
        # Close the serial connection
        ser.close()

if __name__ == "__main__":
    get_sartorius_result()

import RPi.GPIO as GPIO
import csv
import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from datetime import datetime
from math import pi
from time import time, sleep

# Constants
trig = False
INPUT_PIN = 17
CSV_FILE = 'Motor_Speed_Measurement_System.csv'
ENCODER_RES = 12

# Initialize CSV file with headers
def initialize_csv():
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Method', 'Frequency (Hz)', 'Angular Velocity (RPM)', 'Angular Velocity (rad/s)'])

# Append data to CSV
def append_csv(timestamp, method, frequency, angular_velocity_rpm, angular_velocity_rad_s):
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, method, f"{frequency:.3f}", f"{angular_velocity_rpm:.3f}", f"{angular_velocity_rad_s:.3f}"])

# GPIO settings
def gpio_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(INPUT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    return INPUT_PIN

# Pulse Counter with Rising Edge Detection
def count_pulses(input_pin, timeout_sec=None, pulse_limit=None):
    count = 0
    start_time = time()
    events = []

    def pulse_callback(channel):
        nonlocal count
        count += 1
        events.append(time())

    GPIO.add_event_detect(input_pin, GPIO.RISING, callback=pulse_callback)

    try:
        while True:
            if timeout_sec and (time() - start_time) >= timeout_sec:
                break
            if pulse_limit and count >= pulse_limit:
                break
            sleep(0.01)
    finally:
        GPIO.remove_event_detect(input_pin)

    return count, events

# Method 1: Fixed Time Interval
def fixed_time(input_pin):
    while True:
        try:
            period = int(input("Enter time interval (1 - 9 seconds): "))
            if 1 <= period <= 9:
                break
            else:
                print("Please choose a number within the range.")
        except ValueError:
            print("Invalid number.")

    print(f"Counting pulses for {period} seconds.....")
    start_time = time()
    count, events = count_pulses(input_pin, timeout_sec=period)
    end_time = time()
    elapsed_time = end_time - start_time

    angular_velocity_rpm = (count * 60) / (period * ENCODER_RES)
    angular_velocity_rad_s = (angular_velocity_rpm * 2 * pi) / 60
    frequency = count / period

    print("\n--------Fixed Time Results--------\n")
    print(f"Pulse Count: {count}")
    print(f"Elapsed Time: {elapsed_time:.2f} seconds")
    print(f"Frequency: {frequency:.3f} Hz")
    print(f"Angular Velocity: {angular_velocity_rpm:.3f} RPM")
    print(f"Angular Velocity: {angular_velocity_rad_s:.3f} rad/s")
    print("\n---------------------------------------\n")

    timestamp = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    append_csv(timestamp, "Fixed Time Interval", frequency, angular_velocity_rpm, angular_velocity_rad_s)

# Method 2: Fixed Number of Pulses
def fixed_pulses(input_pin):
    while True:
        try:
            pulse_limit = int(input("Enter number of pulses to count (1 - 100): "))
            if 1 <= pulse_limit <= 100:
                break
            else:
                print("Please enter a number between 1 and 100.")
        except ValueError:
            print("Invalid input")

    print(f"Counting {pulse_limit} pulses.....")
    start_time = time()
    count, events = count_pulses(input_pin, pulse_limit=pulse_limit)
    end_time = time()
    elapsed_time = end_time - start_time

    if elapsed_time == 0:
        frequency = 0
        angular_velocity_rpm = 0
        angular_velocity_rad_s = 0
        print("Error in measurement!")
    else:
        frequency = count / elapsed_time
        angular_velocity_rpm = (count * 60) / (elapsed_time * ENCODER_RES)
        angular_velocity_rad_s = (angular_velocity_rpm * 2 * pi) / 60

    print("\n--------Fixed Pulses Results--------\n")
    print(f"Pulse Count: {count}")
    print(f"Elapsed Time: {elapsed_time:.2f} seconds")
    print(f"Frequency: {frequency:.3f} Hz")
    print(f"Angular Velocity: {angular_velocity_rpm:.3f} RPM")
    print(f"Angular Velocity: {angular_velocity_rad_s:.3f} rad/s")
    print("\n--------------------------------------------\n")

    timestamp = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    append_csv(timestamp, "Fixed Pulse Count", frequency, angular_velocity_rpm, angular_velocity_rad_s)

# Real-time data animation with subplots
def animate_data():
    plt.style.use('fivethirtyeight')
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 8))
    xs = []
    ys_rpm = []
    ys_rad_s = []
    ys_frequency = []

    def animate(i):
        try:
            with open(CSV_FILE, 'r') as file:
                reader = list(csv.reader(file))
                if len(reader) < 2:
                    return

                xs.clear()
                ys_rpm.clear()
                ys_rad_s.clear()
                ys_frequency.clear()

                for row in reader[1:]:
                    xs.append(row[0])
                    ys_rpm.append(float(row[2]))
                    ys_rad_s.append(float(row[3]))
                    ys_frequency.append(float(row[4]))

            ax1.clear()
            ax1.plot(xs, ys_rpm, label='Angular Velocity (RPM)', color='blue')
            ax1.set_ylabel('RPM')

            ax2.clear()
            ax2.plot(xs, ys_rad_s, label='Angular Velocity (rad/s)', color='green')
            ax2.set_ylabel('Rad/s')

            ax3.clear()
            ax3.plot(xs, ys_frequency, label='Frequency (Hz)', color='red')
            ax3.set_xlabel('Timestamp')
            ax3.set_ylabel('Hz')

            fig.autofmt_xdate()
            plt.tight_layout()

        except Exception as e:
            print(f"Error in animation: {e}")

    ani = animation.FuncAnimation(fig, animate, interval=1000, cache_frame_data=False)
    plt.show()

# Menu Display
def display_menu():
    print("\n-------------Group 5 Motor Speed Measurement System-------------\n")
    print("1. ILHAN HASHIM BIN MOHD NOR FAZLY\n2. TAN KAI XIAN\n3. ARSYAD HILMI\n4. DANISH KLOPP\n")
    print("Please select the measuring method: ")
    print("[1] Fixed Time ")
    print("[2] Fixed Pulse ")
    print("[3] Exit program")

# Main program
def main():
    # initialize_csv()
    input_pin = gpio_setup()
    print("GPIO initialized")

    while True:
        display_menu()
        choice = input("Enter your choice (1 - 3): ").strip()

        if choice == '1':
            fixed_time(input_pin)
            animate_data()

        elif choice == '2':
            fixed_pulses(input_pin)
            animate_data()

        elif choice == '3':
            print("Exiting the program")
            break

        else:
            print("Invalid input.")

    GPIO.cleanup()

# Execute program
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        GPIO.cleanup()

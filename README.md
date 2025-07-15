# Motor Speed DAQ

This project is created to build a Data Acquisition System (DAQ) for measuring motor speeds. The following are the hardware needed to build the system

- Raspberry Pi 4
- HPAC-08 Motor Trainer Kit
- Oscilloscope
- LM324 Op Amp IC
- 3 5.6K Ohm Resistors
- 2 4.6K Ohm Resistors
- 1 0.7 uF Capacitor
- Variable Power Supply

The hardware was connected as shown in the image below. Please refer to the datasheet  for LM324 Op Amp Pinout

## HARDWARE SETUP

![Alt text](Images/Motor%20Speed%20DAQ%20Annotated.JPG)

- A power supply of 5.2 V is used for the power rails because the voltage received from the HPAC-08 trainer is 5.2V
- Buffer is used for impedance matching and isolation

## Low Pass Filter

- A low pass filter is used to filter the circuit with a cutoff frequency of 30 Hz.
  f<sub>cutoff</sub> = 30 Hz. This value is taken from the oscilloscope.
- By utilizing the following equation, f<sub>c</sub> = 1 / 2πRC, the resistor is arbitratily set to 5.6K Ω. Then by utilizing the equation, a capacitance of 0.9 µF was calculated. However, only a 0.7 µF was available.

![Alt Text](Images/filtered%20signal.JPG)

## Comparator

- Converts the analog signal into a digital signal with reference to a desired voltage. A voltage divider is used to create a 3.3 V reference from a 6 V source.
- When the voltage from the second buffer is more than 3.3 V, the comparator outputs a HIGH signal. when it is lower than 3.3 V, it outputs a LOW signal

![Alt Text](Images/comparator%20signal.JPG)

## Step Down

- A voltage divider is used to step down the 5.2 V to 3.3 V  to be used in the Raspberry Pi. This is because the Pi can only accept up to 3.3V as an input signal.

## Impedance Matching
- Causes a voltage drop between high impedance souce and low impedance load.

    <pre> [High-Z Sensor] --(1MΩ)--|--(10kΩ)-- [ADC input] </pre>

- This creates a voltage divider  
    ```
    [SOURCE] ----[R_source]----+----[R_load]---- GND
                               |
                               +--> V_measured (to ADC)
    ```

    V<sub>measured</sub> = V<sub>source</sub> × (R<sub>load</sub> / (R<sub>source</sub> + R<sub>load</sub>))

    V<sub>source</sub> = 1.0 V

    R<sub>source</sub> = 100K Ω

    R<sub>load</sub> = 10K Ω

    V<sub>measured</sub> = 0.091 V

    Only 91mV instead of 1 V

    ### Solution

    ```
    [SOURCE] ----[R_source]---- [Op-Amp Buffer] ----[Low-Z Load]
                           ↑
                    High input impedance (~1MΩ+)
    ```

    V<sub>measured</sub> = V<sub>source</sub> × (∞ / (R<sub>source</sub> + ∞)) = V<sub>source</sub>

- Op Amp prevents current draw which preserves the source signal

    ```
    [Buffer output] --(1kΩ)---+---(10kΩ)--- GND
                            |
                        V_measured
    ```

    V<sub>measured</sub> = V<sub>buffer</sub> × ( 10K / ( 10K + 1K )) = 0.909 x V<sub>buffer</sub>

    9% Loss in signal

    If Resistance is < 10 Ω
    
    V<sub>measured</sub> = V<sub>buffer</sub> × ( 10K / ( 10 + 10K )) = 0.999 x V<sub>buffer</sub>

## SOFTWARE SETUP

Clone this project into a folder

```
git clone https://github.com/IlhanHashimEng/MotorSpeedDAQ.git
```

Then move into the src folder

```
cd src
```

Run the python script

```
python main.py
```
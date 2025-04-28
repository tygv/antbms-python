#!/usr/bin/env python3
"""
serial_logger.py — Poll an ANT-BMS over classic Bluetooth-UART and log
timestamped voltage, current, temperature, dV/dt, cycle index, discharge,
and SoC (%) to bms_data.csv every 10 seconds.
"""
import csv, time, struct
from binascii import unhexlify
from datetime import datetime
import serial  # pip install pyserial

PORT = "COM13"       # e.g., '/dev/rfcomm0' on Linux
BAUD = 9600
INTERVAL = 10        # seconds
CSV = "bms_data.csv"

# Pack constants for 20S × LG INR18650-MJ1
VNOM, E_WH = 3.7, 192.4
AH_TOTAL = E_WH / VNOM  # ≈52 Ah

ser = serial.Serial(PORT, BAUD, timeout=1)

# Initialize CSV with header if needed
try:
    with open(CSV, "x", newline="") as f:
        csv.writer(f).writerow([
            "timestamp","voltage_V","current_A","temp_C",
            "dVdt_V/s","cycle_idx","discharge_Ah","SoC_%"
        ])
except FileExistsError:
    pass

prev_v, prev_t = None, None

def parse_frame(hexstr):
    """Decode 140-byte frame (hex) into metrics."""
    global prev_v, prev_t
    v = struct.unpack(">H", unhexlify(hexstr[8:12]))[0] * 0.1
    i = struct.unpack(">H", unhexlify(hexstr[12:16]))[0] * 0.1
    temps = [struct.unpack(">H", unhexlify(hexstr[16+4*j:20+4*j]))[0]*0.01 for j in range(4)]
    t_avg = sum(temps)/4
    now = time.time()
    dvdt = (v - prev_v)/(now-prev_t) if prev_v else 0.0
    prev_v, prev_t = v, now
    cyc = int(hexstr[4:8], 16)
    soc = int(hexstr[148:150], 16)
    rem = AH_TOTAL*(soc/100)
    dis = AH_TOTAL - rem
    return dict(voltage=v, current=i, temp=t_avg,
                dvdt=dvdt, cycle=cyc, discharge=dis, soc=soc)

def main():
    print(f"[ANT-BMS] Logging → {CSV}")
    try:
        while True:
            ser.write(bytes.fromhex("DBDB00000000"))
            time.sleep(1)
            data = ser.read(140).hex()
            if len(data)!=280:
                print("⚠️ Incomplete frame, retrying…")
                continue
            row = parse_frame(data)
            with open(CSV, "a", newline="") as f:
                csv.writer(f).writerow([
                    datetime.now().isoformat(),
                    row["voltage"], row["current"], row["temp"],
                    row["dvdt"], row["cycle"], row["discharge"], row["soc"]
                ])
            print(f"V={row['voltage']:.2f}V I={row['current']:.2f}A "
                  f"T={row['temp']:.1f}°C dVdt={row['dvdt']:.4f}V/s "
                  f"Cyc={row['cycle']} Dis={row['discharge']:.2f}Ah "
                  f"SoC={row['soc']}%")
            time.sleep(INTERVAL-1)
    except KeyboardInterrupt:
        pass
    finally:
        ser.close()

if __name__ == "__main__":
    main()

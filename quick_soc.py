#!/usr/bin/env python3
"""
quick_soc.py — One-shot SoC (%) and pack voltage readout.
"""
import serial, struct, time, sys
from binascii import unhexlify

port = sys.argv[1] if len(sys.argv)>1 else "COM13"
ser  = serial.Serial(port,9600,timeout=1)
ser.write(bytes.fromhex("DBDB00000000"))
time.sleep(1)
raw = ser.read(140).hex()
if len(raw)==280:
    soc  = int(raw[148:150],16)
    volt = struct.unpack(">H",unhexlify(raw[8:12]))[0]*0.1
    print(f"SoC: {soc}% | Voltage: {volt:.2f}V")
else:
    print("No valid frame received")
ser.close()

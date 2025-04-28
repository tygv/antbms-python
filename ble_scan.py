#!/usr/bin/env python3
"""
ble_scan.py — Async BLE scan for nearby devices (name, MAC, RSSI).
"""
import asyncio
from bleak import BleakScanner  # pip install bleak

async def scan(sec=5):
    print(f"Scanning for {sec}s…")
    devices = await BleakScanner.discover(timeout=sec)
    for d in devices:
        print(f"{d.name or '(no-name)'} {d.address} RSSI {d.rssi}dBm")

if __name__=="__main__":
    asyncio.run(scan())

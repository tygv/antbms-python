#!/usr/bin/env python3
"""
ble_services.py — Dump BLE service & characteristic UUIDs for a given MAC.
"""
import sys, asyncio
from bleak import BleakClient

async def dump(mac):
    async with BleakClient(mac) as client:
        print(f"Connected to {mac}")
        for svc in await client.get_services():
            print(f"[Service] {svc.uuid}")
            for ch in svc.characteristics:
                props = ",".join(ch.properties)
                print(f"  └─ {ch.uuid} ({props})")

if __name__=="__main__":
    if len(sys.argv)<2:
        sys.exit("Usage: python ble_services.py AA:BB:CC:DD:EE:FF")
    asyncio.run(dump(sys.argv[1]))

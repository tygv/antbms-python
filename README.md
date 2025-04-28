# ANT-BMS Python Interface

**Lightweight, dependency-light Python scripts** for talking to ANT BMS battery-management systems over classic Bluetooth-UART and BLE.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)]()
[![PyPI Version](https://img.shields.io/pypi/v/antbms-python.svg)]()

---

## 🚀 Table of Contents

1. [Description](#description)  
2. [Features](#features)  
3. [Quick Start](#quick-start)  
4. [Installation](#installation)  
5. [Configuration](#configuration)  
6. [Usage Examples](#usage-examples)  
7. [Scripts & API Reference](#scripts--api-reference)  
8. [Data & Output](#data--output)  
9. [Troubleshooting](#troubleshooting)  
10. [Directory Structure](#directory-structure)  
11. [Contributing](#contributing)  
12. [License](#license)  
13. [Contact & Links](#contact--links)  

---

## 📖 Description

The **ANT-BMS Python Interface** provides four standalone scripts to interact with ANT BMS battery-management hardware:

- **`serial_logger.py`** — Polls the pack over classic Bluetooth-UART every _N_ seconds, parses voltage, current, temperature, incremental dV/dt, cycle index, discharge capacity (Ah), and State-of-Charge (%) and appends to a CSV file.  
- **`ble_scan.py`** — Performs a quick asynchronous scan of nearby BLE devices, listing name, MAC address, and RSSI.  
- **`ble_services.py`** — Connects to a specified BLE device and dumps all GATT services & characteristic UUIDs for reverse engineering.  
- **`quick_soc.py`** — One-shot reader that prints pack voltage and SoC (%) then exits—ideal for shell scripts.  

This repo requires only **pyserial** and **bleak**—no heavy dependencies or frameworks.

---

## ⭐ Features

- **Robust UART polling** with timeout and incomplete-frame detection.  
- **Incremental dV/dt** calculation for capacity analysis.  
- **Average cell temperature** from 4 thermistor readings.  
- **Async BLE operations**—no blocking.  
- **Self-contained scripts** with no additional wrappers.  
- **Minimal footprint**: Lean code, pure-Python, MIT-licensed.

---

## ⚡ Quick Start

```bash
git clone https://github.com/tygv/antbms-python.git
cd antbms-python

python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
.venv\Scripts\activate       # Windows

pip install -r requirements.txt
```

---

## ⚙️ Configuration

Edit the constants at the top of each script to match your environment:

**serial_logger.py**
```python
PORT     = "COM13"        # Windows COM port or '/dev/rfcomm0' on Linux
BAUD     = 9600           # BMS default baud rate
INTERVAL = 10             # seconds between polls
CSV_FILE = "bms_data.csv" # output CSV
```

**ble_scan.py**, **ble_services.py**, and **quick_soc.py** use sensible defaults but can be tuned in code.

---

## 🏃 Usage Examples

### 1. Continuous Serial Logging

```bash
python serial_logger.py
```

Console output:

```
[ANT-BMS] Logging → bms_data.csv
V=74.00 V  I=0.00 A  T=25.2 °C  dV/dt=0.0000 V/s  Cyc=1  Dis=0.00 Ah  SoC=100%
```

### 2. BLE Device Scan

```bash
python ble_scan.py
```

### 3. BLE Service Dump

```bash
python ble_services.py AA:BB:CC:11:22:33
```

### 4. Quick SoC Reader

```bash
python quick_soc.py COM13
```

---

## 🛠 Troubleshooting

- **Permission errors on `/dev/rfcomm0`**: Ensure your user is in the `dialout` or `bluetooth` group.  
- **Incomplete frames**: Verify baud rate and wiring; increase timeout in `serial_logger.py`.  
- **BLE scan hangs**: Update `bleak` to the latest version; ensure Bluetooth adapter drivers support BLE.  

---

## 🔧 Directory Structure

```
antbms-python/
├── serial_logger.py
├── ble_scan.py
├── ble_services.py
├── quick_soc.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```

---

## 🤝 Contributing

1. Fork this repository  
2. Create a feature branch (`git checkout -b feature-name`)  
3. Commit your changes (`git commit -m "feat: describe"`)  
4. Push to your fork (`git push origin feature-name`)  
5. Open a Pull Request

---

## 📄 License

Licensed under the **MIT License**. See the [LICENSE](LICENSE) file.

---

## 📬 Contact & Links

- Repo: https://github.com/tygv/antbms-python
- ANT BMS: https://antbms.vip

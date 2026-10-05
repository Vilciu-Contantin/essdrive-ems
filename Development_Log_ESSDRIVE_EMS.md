# ESSDRIVE EMS — Development Log

## Project

**Project:** ESSDRIVE Energy Management System (EMS)  
**Version:** V1.0  
**Start:** 2026  
**Current status:** Sprint 1 — Core EMS

---

## 1. Development Environment

- OS: Windows
- IDE: Visual Studio Code
- Language: Python
- Framework: FastAPI
- Environment: `.venv`
- API documentation/testing: Swagger
- Local server:

```powershell
python -m uvicorn app.main:app --reload
```

### Project structure

```text
essdrive-ems/
├── .venv/
├── app/
├── requirements.txt
├── .gitignore
├── README.md
└── JOURNAL.md
```

---

# 2. Sprint 1 — EMS Core

## Sprint Goal

Construim nucleul EMS care poate primi:

- date PV
- date consum
- date baterie
- date rețea
- prețuri pe intervale de 15 minute

și poate calcula ulterior strategii de încărcare / descărcare.

---

# 3. Backlog Sprint 1

| ID | Task | Status |
|---|---|---|
| EMS-001 | Project structure + FastAPI | ✅ DONE |
| EMS-002 | Energy Data Model | ✅ DONE |
| EMS-003 | PV Simulator | ✅ DONE |
| EMS-004 | Load Simulator | ✅ DONE |
| EMS-005 | Battery + SOC | ⏳ NEXT |
| EMS-006 | Price Model | ⬜ TODO |
| EMS-007 | Energy Flow Engine | ⬜ TODO |
| EMS-008 | Grid Import / Export | ⬜ TODO |
| EMS-009 | Battery Optimizer | ⬜ TODO |
| EMS-010 | Trading Simulation | ⬜ TODO |
| EMS-011 | PostgreSQL | ⬜ TODO |
| EMS-012 | REST API | ⬜ TODO |
| EMS-013 | Dashboard V1 | ⬜ TODO |

---

# 4. Tasks Finalizate

## EMS-001 — Project Structure + FastAPI

**Status:** DONE

Implementat:

- structură proiect
- Python virtual environment
- FastAPI
- configurare aplicație
- endpoint `/`
- endpoint `/health`
- Swagger

Swagger:

```text
http://127.0.0.1:8000/docs
```

Server:

```powershell
python -m uvicorn app.main:app --reload
```

---

## EMS-002 — Energy Data Model

**Status:** DONE

Fișier:

```text
app/energy/models.py
```

Modele implementate:

- `DeviceType`
- `EnergyData`
- `PVData`
- `LoadData`
- `GridData`
- `BatteryData`
- `EnergySnapshot`

Principalele date:

- timestamp
- power kW
- energy kWh
- voltage V
- current A
- reactive power
- reactive energy
- battery capacity
- SOC %
- charge power
- discharge power
- minimum SOC
- maximum SOC

---

## EMS-003 — PV Simulator

**Status:** DONE

Fișier:

```text
app/energy/pv_simulator.py
```

Caracteristici:

- simulare 24h
- 96 intervale
- interval de 15 minute
- capacitate PV configurabilă
- curbă simplificată de producție
- energie calculată în kWh

Endpoint:

```text
GET /api/v1/energy/pv/simulate
```

Exemplu:

```text
capacity_kw = 100
interval_minutes = 15
intervals = 96
```

Rezultat verificat în Swagger.

Curba V1:

```text
00:00–06:00 → 0 kW
06:00–12:00 → creștere
12:00 → putere maximă
12:00–18:00 → scădere
18:00–24:00 → 0 kW
```

---

## EMS-004 — Load Simulator

**Status:** DONE

Fișier:

```text
app/energy/load_simulator.py
```

Caracteristici:

- simulare consum 24h
- 96 intervale
- interval de 15 minute
- consum configurabil
- curbă simplificată de consum

Endpoint:

```text
GET /api/v1/energy/load/simulate
```

Test efectuat:

```text
base_load_kw = 15
peak_load_kw = 30
interval_minutes = 15
intervals = 96
```

Rezultatul a fost verificat în Swagger.

---

# 5. CURRENT CHECKPOINT

## Ultimul task finalizat

**EMS-004 — Load Simulator**

Status:

```text
✅ TESTAT CU SUCCES
```

Ultimul lucru verificat:

```text
/api/v1/energy/load/simulate
```

cu:

```text
base_load_kw = 15
peak_load_kw = 30
```

---

# 6. NEXT TASK

## EMS-005 — Battery + SOC

**Status:** NEXT

Obiectiv:

Construim modelul bateriei și logica de State of Charge (SOC).

Trebuie să putem simula:

- capacitate baterie kWh
- SOC %
- SOC minim
- SOC maxim
- putere maximă de încărcare
- putere maximă de descărcare
- eficiență încărcare
- eficiență descărcare
- încărcare baterie
- descărcare baterie
- actualizare SOC la fiecare 15 minute

Exemplu de baterie pentru test:

```text
capacity = 266 kWh
SOC = 50%
min SOC = 10%
max SOC = 100%
charge power = 60 kW
discharge power = 60 kW
```

---

# 7. Planned EMS Architecture

Fluxul principal:

```text
PV
 │
 ▼
┌─────────────────┐
│   Energy Data   │
│     Engine      │
└────────┬────────┘
         │
         ├──────────► LOAD
         │
         ├──────────► BATTERY
         │
         └──────────► GRID
                    │
                    ▼
              Energy Flow
                 Engine
                    │
                    ▼
             Battery Optimizer
                    │
                    ▼
               Control Layer
                    │
                    ▼
             Device Interface
```

---

# 8. Future EMS Modules

## Data Engine

Va primi:

- PV
- Load
- Battery
- Grid
- Meter
- Inverter

## Price Engine

Va lucra cu:

- prețuri energie
- intervale de 15 minute
- import
- export
- semnale de piață

## Battery Optimizer

Va calcula:

- charge
- discharge
- idle

în funcție de:

- SOC
- preț
- producție PV
- consum
- limite baterie
- eficiență
- degradare
- forecast

## Control Layer

Structură planificată:

```text
Optimizer
   ↓
Safety Validator
   ↓
Limits Validator
   ↓
Command Queue
   ↓
Device Driver
   ↓
Inverter
```

**Important:** AI/optimizer-ul nu trebuie să controleze direct invertorul fără stratul de siguranță.

---

# 9. Future Hardware Integration

Ținte de integrare:

- Huawei
- Sungrow
- Deye
- SolaX
- Victron
- Smart Meters
- RS485 Modbus
- Modbus TCP
- MQTT

Arhitectura planificată:

```text
ESSDRIVE Cloud
       │
       │ MQTT / HTTPS
       ▼
ESSDRIVE Edge
       │
       │ RS485 / Modbus
       ▼
Meter ─── Inverter ─── Battery
```

---

# 10. VPP / Trading — FUTURE

Ulterior:

```text
EMS
 │
 ▼
Optimizer
 │
 ▼
VPP
 │
 ├── Price Signals
 ├── Fleet Management
 ├── Dispatch
 └── Settlement
```

În V1 se lucrează inițial cu **simulare**, nu cu tranzacționare reală și nu cu control real al echipamentelor.

---

# 11. Development Rules

Pentru fiecare task:

1. Construim componenta.
2. Pornim serverul.
3. Testăm în Swagger.
4. Verificăm rezultatul.
5. Dacă funcționează → `DONE`.
6. Actualizăm acest jurnal.
7. Trecem la următorul task.

Nu trecem peste task-uri fără validare.

---

# 12. Commands

Activare `.venv` în PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Pornire server:

```powershell
python -m uvicorn app.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

Root:

```text
http://127.0.0.1:8000/
```

Health:

```text
http://127.0.0.1:8000/health
```

---

# 13. NEXT SESSION

La următoarea sesiune de lucru:

```text
START → EMS-005 — Battery + SOC
```

Primul obiectiv:

```text
app/energy/battery.py
```

Vom construi bateria V1 și o vom testa în Swagger înainte de a trece la EMS-006.

---

# 14. Change Log

## 2026-10-05

- EMS-001 finalizat
- EMS-002 finalizat
- EMS-003 finalizat
- EMS-004 finalizat
- PV Simulator testat
- Load Simulator testat
- Sprint 1 în desfășurare
- Următorul task: **EMS-005 Battery + SOC**

---

## IMPORTANT

**Nu șterge acest fișier.**

Acesta este jurnalul principal al dezvoltării ESSDRIVE EMS.

După fiecare task important, actualizează:

```text
Status
Current Checkpoint
Next Task
Change Log
```

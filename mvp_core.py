#!/usr/bin/env python3
import os
import math
import json
from multiprocessing import Pool, cpu_count

# --- App State & Persistence ---
CREDITS = 0
TERMINAL_ENV = {}
STATE_FILE = "app_state.json"

def load_state():
    global CREDITS
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            CREDITS = int(data.get("credits", 0))
    except Exception:
        CREDITS = 0

def save_state():
    try:
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"credits": CREDITS}, f)
    except Exception:
        pass

# --- Utilities ---
def add_credits(amount=1):
    global CREDITS
    CREDITS += amount
    save_state()

# =========================
# FPS: File Processing System
# =========================

def read_in_chunks(path, chunk_size=4096):
    """Yield bytes chunks from file safely."""
    with open(path, "rb") as f:
        while True:
            data = f.read(chunk_size)
            if not data:
                break
            yield data

def process_chunk(chunk_bytes):
    """Placeholder processing for a chunk: count bytes and lines and checksum."""
    byte_len = len(chunk_bytes)
    line_count = chunk_bytes.count(b"")
    checksum = sum(chunk_bytes) % 9973
    return {"bytes": byte_len, "lines": line_count, "checksum": checksum}

def fps_chunk_and_process():
    print("=== FPS: Chunk & Process File ===")
    print("Enter a file path (text file recommended). Type 'back' to return.")
    path = input("Path: ").strip()
    if path.lower() in ("back", "exit", "quit"):
        print("Returning...")
        return
    if not os.path.isfile(path):
        print("File not found. Please provide a valid path.")
        return

    try:
        sz = input("Chunk size in bytes (default 4096): ").strip()
        chunk_size = int(sz) if sz else 4096
    except ValueError:
        print("Invalid size, using 4096.")
        chunk_size = 4096

    total_bytes = os.path.getsize(path)
    est_chunks = math.ceil(total_bytes / max(1, chunk_size))
    print(f"File size: {total_bytes} bytes, estimated chunks: {est_chunks}")

    results = []
    try:
        for idx, chunk in enumerate(read_in_chunks(path, chunk_size), start=1):
            res = process_chunk(chunk)
            results.append(res)
            if idx % 10 == 0 or idx == est_chunks:
                print(f"Processed {idx}/{est_chunks} chunks...")
        add_credits(min(5, est_chunks))
        print("FPS completed. Summary:")
        total_b = sum(r["bytes"] for r in results)
        total_l = sum(r["lines"] for r in results)
        avg_cs = round(sum(r["checksum"] for r in results) / max(1, len(results)), 2)
        print(f"- Total bytes seen: {total_b}")
        print(f"- Total lines counted: {total_l}")
        print(f"- Avg checksum: {avg_cs}")
    except KeyboardInterrupt:
        print("Paused by user. Partial progress retained. Resume anytime.")

# =========================
# DPS: Distributed Processing (Simulation via Multiprocessing)
# =========================

def heavy_compute(x):
    # Simulate heavy CPU work per unit of data (tuned for mobile safety)
    s = 0
    for i in range(5000):
        s = (s + (x * i)) % 1000003
    return s

def dps_parallel_process():
    print("=== DPS: Parallel Processing Demo ===")
    print("This will simulate distributing work across CPU cores.")
    try:
        n = int(input("How many units of work? (e.g., 50): ").strip() or "50")
    except ValueError:
        n = 50
    n = min(n, 200)  # safety cap
    data = list(range(1, n + 1))
    workers = max(1, min(cpu_count(), 4))  # conservative on mobile
    print(f"Using {workers} worker processes...")

    # Keep this line intact (single line) and ending with colon
    with Pool(processes=workers) as pool:
        out = pool.map(heavy_compute, data)

    print("DPS completed. Sample results:")
    print(f"- First 5 outputs: {out[:5]}")
    print(f"- Last 5 outputs:  {out[-5:]}")
    add_credits(5)

# --- Learning Chatbot (VSTS basics) ---
def learning_chatbot():
    print("=== Learning Chatbot Mode ===")
    print("Styles: simple | detailed | compare")
    print("Commands: style <name>, back")
    print("Try: style simple,what is python   OR set style first and ask on next line.")

    style = "simple"
    def answer(q):
        q = q.lower().strip()
        if q == "what is python":
            if style == "simple":
                return "Python is a general-purpose language used for many tasks."
            if style == "detailed":
                return "Python is a high-level, interpreted language great for AI, data, web, and automation."
            if style == "compare":
                return "Python vs C++: Python is easier and slower; C++ is faster and lower-level."
        if q == "how to win hackathon":
            if style == "simple":
                return "Ship a stable MVP and give a clear 3-min demo."
            if style == "detailed":
                return "Focus on theme fit, robust demo, clean UX, and a tight pitch."
            if style == "compare":
                return "MVP vs Prototype: MVP is stable and minimal; prototype is a quick demo with possible gaps."
        return "Sorry, not in knowledge base yet."

    while True:
        q = input("You: ").strip()
        low = q.lower()

        if low in ("back", "exit", "quit"):
            print("Returning to menu...")
            break

        # Accept forms like: style simple,what is python
        if low.startswith("style "):
            rest = q[6:].strip()
            if "," in rest:
                s, _, after = rest.partition(",")
                s = s.strip().lower()
                if s in ("simple", "detailed", "compare"):
                    style = s
                    print(f"Style set to: {style}")
                    q2 = after.strip()
                    if q2:
                        resp = answer(q2)
                        print("Bot:", resp)
                        add_credits(1)
                    continue
                else:
                    print("Unknown style. Use: simple | detailed | compare")
                    continue
            else:
                s = rest.strip().lower()
                if s in ("simple", "detailed", "compare"):
                    style = s
                    print(f"Style set to: {style}")
                else:
                    print("Unknown style. Use: simple | detailed | compare")
                continue

        resp = answer(q)
        print("Bot:", resp)
        add_credits(1)

# --- Python Terminal with integrated commands and shared env ---
def python_terminal():
    print("=== Python Terminal Mode ===")
    print("Enter Python expressions or use commands:")
    print("Commands: fp (FPS), dp (DPS), help, back")

    while True:
        code_line = input("py> ").strip()
        low = code_line.lower()

        if low in ("back", "exit", "quit"):
            print("Returning to menu...")
            break
        if low == "help":
            print("Commands:")
            print("- fp : run File Processing System demo")
            print("- dp : run Distributed Processing demo")
            print("- back : return to menu")
            continue
        if low == "fp":
            fps_chunk_and_process()
            continue
        if low == "dp":
            dps_parallel_process()
            continue
        if not code_line:
            continue

        try:
            result = eval(code_line, TERMINAL_ENV, TERMINAL_ENV)
            if result is not None:
                print(result)
            add_credits(1)
        except SyntaxError:
            try:
                exec(code_line, TERMINAL_ENV, TERMINAL_ENV)
                add_credits(1)
            except Exception as e:
                print("Error:", e)
        except Exception as e:
            print("Error:", e)

# --- Earnings Dashboard with quick actions ---
def earnings_dashboard():
    while True:
        print("=== Earnings Dashboard ===")
        print(f"Total Credits Earned: {CREDITS}")
        print("1) Run FPS demo")
        print("2) Run DPS demo")
        print("3) Back")
        choice = input("Enter choice (1-3): ").strip()
        if choice == "1":
            fps_chunk_and_process()
        elif choice == "2":
            dps_parallel_process()
        elif choice == "3":
            print()
            break
        else:
            print("Invalid choice.")

# --- Main Menu ---
def main_menu():
    while True:
        print("===============================")
        print("      Welcome to MVP App")
        print("===============================")
        print("Select a mode:")
        print("1) Learning (VSTS basics)")
        print("2) Developer Terminal (with FPS/DPS)")
        print("3) Earnings Dashboard (quick actions)")
        print("4) Exit")
        choice = input("Enter choice (1-4): ").strip()

        if choice == "1":
            learning_chatbot()
        elif choice == "2":
            python_terminal()
        elif choice == "3":
            earnings_dashboard()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    load_state()
    main_menu()
# --- Constants (customizable, realistic)
FREE_ROM_MB, FREE_RAM_MB, FREE_CAP = 500, 256, 25
BAT_ROM_MB, BAT_RAM_MB, BAT_CAP = 2000, 1024, 100
PRO_ROM_MB, PRO_RAM_MB, PRO_CAP = 5000, 2048, 200

# --- App state (ensure this merges with your existing state)
STATE = {
    "CREDITS": 0,
    "tier": "free",  # free | battery | pro
    "usage_counters": {
        "messages_used_today": 0,
        "last_usage_date": None
    },
    "workspace": {
        "bytes_written_today": 0,
        "bytes_read_today": 0,
        "daily_history": {}  # "YYYY-MM-DD": {"written": int, "read": int}
    },
    "contribution": {
        "battery_share_percent": 0,
        "contrib_days": 0,
        "entitlement_expires": None  # ISO date string or None
    },
}
from datetime import datetime, timedelta

def _today_str():
    return datetime.utcnow().strftime("%Y-%m-%d")

def _ensure_daily_rollover():
    today = _today_str()
    last = STATE["usage_counters"]["last_usage_date"]
    if last != today:
        # roll over message counters
        STATE["usage_counters"]["messages_used_today"] = 0
        STATE["usage_counters"]["last_usage_date"] = today
        # roll over workspace today to history
        ws = STATE["workspace"]
        if ws["bytes_written_today"] or ws["bytes_read_today"]:
            hist = ws["daily_history"]
            if last:
                day = last
            else:
                day = today
            prev = hist.get(day, {"written": 0, "read": 0})
            prev["written"] += ws["bytes_written_today"]
            prev["read"] += ws["bytes_read_today"]
            hist[day] = prev
        ws["bytes_written_today"] = 0
        ws["bytes_read_today"] = 0
        save_state()
def set_tier(tier):
    if tier not in ("free", "battery", "pro"):
        return False
    STATE["tier"] = tier
    # battery entitlement expiry cleared for pro/free
    if tier != "battery":
        STATE["contribution"]["entitlement_expires"] = None
    save_state()
    return True

def get_tier():
    # auto-downgrade battery if expired
    exp = STATE["contribution"]["entitlement_expires"]
    if STATE["tier"] == "battery" and exp:
        try:
            if datetime.utcnow().date() > datetime.fromisoformat(exp).date():
                STATE["tier"] = "free"
                STATE["contribution"]["entitlement_expires"] = None
                save_state()
        except Exception:
            pass
    return STATE["tier"]

def get_effective_resources():
    tier = get_tier()
    if tier == "free":
        return {"workspace_cache_mb": FREE_ROM_MB, "processing_memory_mb": FREE_RAM_MB,
                "cpu_priority": "standard", "daily_cap": FREE_CAP}
    if tier == "battery":
        return {"workspace_cache_mb": BAT_ROM_MB, "processing_memory_mb": BAT_RAM_MB,
                "cpu_priority": "high", "daily_cap": BAT_CAP}
    return {"workspace_cache_mb": PRO_ROM_MB, "processing_memory_mb": PRO_RAM_MB,
            "cpu_priority": "maximum", "daily_cap": PRO_CAP}
def increment_messages_used():
    _ensure_daily_rollover()
    cap = get_effective_resources()["daily_cap"]
    used = STATE["usage_counters"]["messages_used_today"]
    if used >= cap:
        return False
    STATE["usage_counters"]["messages_used_today"] = used + 1
    save_state()
    return True

def workspace_write(n_bytes):
    _ensure_daily_rollover()
    STATE["workspace"]["bytes_written_today"] += int(n_bytes)
    save_state()

def workspace_read(n_bytes):
    _ensure_daily_rollover()
    STATE["workspace"]["bytes_read_today"] += int(n_bytes)
    save_state()

def get_mb_today():
    wr = STATE["workspace"]["bytes_written_today"] / (1024*1024)
    rd = STATE["workspace"]["bytes_read_today"] / (1024*1024)
    return round(wr, 2), round(rd, 2)

def get_last_7_days_mb():
    # returns list of tuples (date, read_mb, written_mb), most-recent first up to 7 days
    hist = STATE["workspace"]["daily_history"]
    dates = sorted(hist.keys(), reverse=True)
    out = []
    for d in dates[:7]:
        rd = hist[d].get("read", 0)/(1024*1024)
        wr = hist[d].get("written", 0)/(1024*1024)
        out.append((d, round(rd,2), round(wr,2)))
    return out
def simulate_battery_contribution(percent):
    # percent contributed for today; if >=15, count it
    _ensure_daily_rollover()
    c = STATE["contribution"]
    c["battery_share_percent"] = int(percent)
    if percent >= 15:
        c["contrib_days"] = int(c["contrib_days"]) + 1
    # grant battery plan if 7+ contributing days and not already active
    if c["contrib_days"] >= 7:
        STATE["tier"] = "battery"
        expiry = (datetime.utcnow() + timedelta(days=7)).date().isoformat()
        c["entitlement_expires"] = expiry
        # reset counter for next cycle
        c["contrib_days"] = 0
    save_state()
    return {
        "tier": STATE["tier"],
        "battery_share_percent": c["battery_share_percent"],
        "entitlement_expires": c["entitlement_expires"]
    }
import random

def process_data_service():
    # generate mock dataset
    items = [{"value": random.randint(1, 100)} for _ in range(200)]
    # process: compute average
    s = sum(x["value"] for x in items)
    avg = s/len(items)
    # assume 5KB read per item
    bytes_read = len(items) * 5 * 1024
    workspace_read(bytes_read)
    add_credits(3)
    return {"items": len(items), "avg": round(avg, 2), "bytes_mb": round(bytes_read/(1024*1024), 2)}
def stress_compute(iterations=200000, steps=10, progress_cb=None):
    # simple CPU loop broken into steps
    chunk = max(1, iterations//steps)
    acc = 0
    for i in range(steps):
        for j in range(chunk):
            acc = (acc + j) % 1000003
        if progress_cb:
            try: progress_cb(i+1, steps)
            except Exception: pass
    # pretend some write due to logs/output
    workspace_write(64*1024)
    return {"iterations": iterations, "steps": steps, "acc": acc}
_QA = {
    "what is python": {
        "simple": "Python is a general-purpose programming language.",
        "detailed": "Python is a high-level, interpreted language great for data, AI, web, and automation.",
        "compare": "Python vs C++: Python is easier and slower; C++ is faster and lower-level."
    },
    "what is a function": {
        "simple": "A function is a reusable block of code.",
        "detailed": "A function groups statements under a name, accepts inputs (params), and can return a value.",
        "compare": "Function vs Method: a method is a function bound to an object (has self)."
    },
    "what is a module": {
        "simple": "A module is a Python file with code.",
        "detailed": "Modules organize code into files; import them to reuse functions, classes, and variables.",
        "compare": "Module vs Package: package is a folder of modules with __init__.py."
    },
    "how to read a file": {
        "simple": "Use open('file.txt').read().",
        "detailed": "Use with open('file.txt') as f: data = f.read(); it safely closes the file.",
        "compare": "read vs readline: read gets all, readline gets one line."
    },
    "what is oop": {
        "simple": "OOP organizes code with classes and objects.",
        "detailed": "OOP uses classes (blueprints) and objects (instances) with encapsulation and inheritance.",
        "compare": "OOP vs FP: OOP focuses on objects; FP focuses on pure functions and immutability."
    },
    "what is multiprocessing": {
        "simple": "It runs code on multiple CPU cores.",
        "detailed": "Multiprocessing creates separate processes to run tasks in parallel, avoiding GIL limits.",
        "compare": "Multiprocessing vs Threading: processes bypass GIL; threads share memory but hit GIL."
    },
    "dps vs fps": {
        "simple": "DPS is parallel compute; FPS is chunked file processing.",
        "detailed": "DPS parallelizes CPU work across cores; FPS splits file input into manageable chunks.",
        "compare": "DPS gains with CPU; FPS gains with streaming/chunking I/O."
    },
    "how to win hackathon": {
        "simple": "Solve a real problem and demo clearly.",
        "detailed": "Align with judging; show polished demo, monetization, and reliability under constraints.",
        "compare": "MVP vs MLP: MVP functions; MLP delights with polish."
    },
    "what is mvp vs prototype": {
        "simple": "MVP is minimal and usable; prototype is a quick demo.",
        "detailed": "MVP is functional and testable; prototype explores ideas and may be incomplete.",
        "compare": "MVP aims for users; prototype aims for validation."
    },
    "what is api": {
        "simple": "An API lets apps talk to each other.",
        "detailed": "APIs define endpoints and data formats to request and exchange information.",
        "compare": "REST vs GraphQL: REST has fixed endpoints; GraphQL lets clients ask for specific data."
    }
}

def explainer_answer(style, question):
    style = (style or "simple").strip().lower()
    q = (question or "").strip().lower()
    if not increment_messages_used():
        return "Daily cap reached for your current plan. Upgrade or contribute battery to increase the cap."
    entry = _QA.get(q)
    if not entry:
        add_credits(1)
        return "Answer not in local knowledge yet. Try another topic."
    msg = entry.get(style) or entry.get("simple")
    add_credits(1)
    return msg

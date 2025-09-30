# lde_cli.py
import json, os, time
import mvp_core as core

def show_state(tag=""):
    res = core.get_effective_resources()
    wr, rd = core.get_mb_today()
    print(f"[{tag}] Tier={core.get_tier()} cap={res['daily_cap']} ROM={res['workspace_cache_mb']}MB RAM={res['processing_memory_mb']}MB CPU={res['cpu_priority']}")
    print(f"[{tag}] Today: read {rd} MB, written {wr} MB, Credits={core.STATE.get('CREDITS',0)}")

def run_demo():
    try:
        core.load_state()
    except Exception as e:
        print("State load warning:", e)

    print("=== LDE CLI Demo ===")
    show_state("start")

    # Learning Q&A
    print("Explainer:", core.explainer_answer("simple", "what is python"))

    # Simulate battery contributions for a week
    for i in range(7):
        core.simulate_battery_contribution(18)
    show_state("after_battery")

    # Upgrade to pro (mock)
    core.set_tier("pro")
    show_state("pro")

    # Process Data Service
    s = core.process_data_service()
    print("Process Data Service:", s)
    show_state("after_service")

    # Stress compute
    r = core.stress_compute(100000, 5)
    print("Stress compute:", r)
    show_state("after_stress")

    # Seven day history
    print("7-day history:", core.get_last_7_days_mb())
    print("=== Demo complete ===")

if __name__ == "__main__":
    run_demo()

"""Independent calculations for the Gemini review of the one-pass vs three-pass experiment.
All inputs are typed from SHA-verified source pages (physical NTU13/21-23, PAN48-50; see source_pages/)
or read from preserved receipts. Writes calculations.json. No network, no model calls."""
import json, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
RUN = Path(__file__).resolve().parents[1]
EV = RUN.parent
ORIG = EV / "20261029T112944Z_three_pass_experiment"
NEW = EV / "20261029T114212Z_three_pass_pan_resume"
OZ_PER_KG = 32.1507466
out = {}

def pct(a, b):
    return round((b - a) / a * 100, 2)

# ---------------- NTU (physical p21-23 capture; p13 outside capture, used only as confirmation) -------------
p22 = {  # principal book, other financial assets (FV), trade, other loans: carrying values
    "2026-03-31": dict(pb_gross=3414, pb_gain=431, pb_net=3845, ofa=644, trade=390, loans=5, total=4884),
    "2025-03-31": dict(pb_gross=3066, pb_gain=624, pb_net=3690, ofa=663, trade=504, loans=2, total=4859),
    "2025-09-30": dict(pb_gross=3377, pb_gain=598, pb_net=3975, ofa=702, trade=378, loans=4, total=5059),
}
question_pbd = {"2026-03-31": 4489, "2025-03-31": 4353, "2025-09-30": 4677}  # figures quoted in incoming Q-e4497d9112cd4e9d
ntu = {}
for d, v in p22.items():
    ntu[d] = {
        "pb_gross_plus_gain": v["pb_gross"] + v["pb_gain"], "pb_net_printed": v["pb_net"],
        "pb_net_plus_ofa": v["pb_net"] + v["ofa"], "question_pbd_figure": question_pbd[d],
        "reconciles_to_question_figure": v["pb_net"] + v["ofa"] == question_pbd[d],
        "carrying_total_check": v["loans"] + v["trade"] + v["pb_net"] + v["ofa"] == v["total"],
    }
ntu["note1_p13_confirmation"] = {"total_pbd_printed_p13": [4489, 4353, 4677], "pb_rollforward_h1_impairment": -167,
                                 "rollforward": "3975+382-728+383-167", "rollforward_result": 3975 + 382 - 728 + 383 - 167}
seg = {"unsecured": ((2482, 468, 2950), (2371, 227, 2598)), "debt_review": ((793, 72, 865), (951, 141, 1092)),
       "retail": ((48, 47, 95), (46, 51, 97)), "secured": ((54, 11, 65), (46, 12, 58))}
ntu["segment_h1"] = {k: {"gross_chg": b[0] - a[0], "gain_chg": b[1] - a[1], "net_chg": b[2] - a[2], "net_pct": pct(a[2], b[2])} for k, (a, b) in seg.items()}
ntu["h1_movements"] = {"net": (3845 - 3975, pct(3975, 3845)), "gain": (431 - 598, pct(598, 431)), "gross": (3414 - 3377, pct(3377, 3414)),
                       "yoy_net": (3845 - 3690, pct(3690, 3845)), "yoy_gain": (431 - 624, pct(624, 431)), "yoy_gross": (3414 - 3066, pct(3066, 3414))}
out["ntu"] = ntu

# ---------------- PAN gold produced (physical p48 components, p49 totals) -------------
fy26 = dict(bm_ug=65233, ev_ug=40246, bm_surf=2428, btrp_tail=10974, elik_tail=56475, mtr_tail=46164,
            bm_buy=4337, ev_buy=6609, btrp_buy=1958, mtr_buy=5763, ten_feed=32124)
fy25 = dict(bm_ug=65895, ev_ug=26748, bm_surf=2654, btrp_tail=15224, elik_tail=52606, mtr_tail_leaf=25043, mtr_tail_totalcol=30806,
            ev_buy=1081, ten_feed=1513)
pan = {}
pan["fy26_leaf_sum"] = sum(fy26.values())
pan["fy26_group_printed"] = 272310
pan["fy26_disjoint_rows"] = {"expr": "105478+2428+113613+18667+32124", "result": 105478 + 2428 + 113613 + 18667 + 32124}
pan["fy26_barberton_mines_mining_col"] = {"expr": "65233+2428+4337", "result": 65233 + 2428 + 4337, "printed": 71997}
pan["fy26_barberton_total_col_from_p48"] = {"expr": "65233+2428+10974+(4337+1958)", "result": 65233 + 2428 + 10974 + 4337 + 1958}
pan["fy26_barberton_total_from_p49_components"] = {"expr": "71997+12932", "result": 71997 + 12932, "printed_total": 94929, "diff": 94929 - (71997 + 12932)}
pan["fy26_barberton_sold_check"] = {"expr": "70086+12826", "result": 70086 + 12826, "printed": 82912}
pan["fy26_evander_total"] = {"expr": "46855+56475", "result": 46855 + 56475, "printed": 103330}
pan["fy26_total_operation_columns"] = {"expr": "94929+103330+51927+32124", "result": 94929 + 103330 + 51927 + 32124, "group": 272310}
pan["fy26_total_operation_columns_if_84929"] = 84929 + 103330 + 51927 + 32124
pan["fy26_mining_plus_surface"] = {"expr": "118853+153458", "result": 118853 + 153458, "group": 272310}
pan["fy25_disjoint"] = {"expr": "92643+2654+98636+1081+1513", "result": 92643 + 2654 + 98636 + 1081 + 1513, "printed": 196527}
pan["fy25_overlap_totalcol_underground"] = {"expr": "93724+2654+98636+1081+1513", "result": 93724 + 2654 + 98636 + 1081 + 1513, "printed": 196527}
pan["fy25_evander_totalcol_underground"] = {"expr": "26748+1081", "result": 26748 + 1081, "printed": 27829}
pan["fy25_tailings_row_subtotal"] = {"with_30806": 15224 + 52606 + 30806, "with_25043": 15224 + 52606 + 25043, "printed": 98636}
pan["fy25_mtr_gap"] = {"expr": "30806-25043", "result": 30806 - 25043, "coincides_with_fy26_mtr_buyin": 30806 - 25043 == 5763}
pan["fy25_total_operation_columns"] = {"expr": "83773+80435+30806+1513", "result": 83773 + 80435 + 30806 + 1513, "group": 196527}
d = {"underground": (92643, 105478), "surface": (2654, 2428), "tailings": (98636, 113613), "buy_in": (1081, 18667), "surface_feedstock": (1513, 32124)}
pan["fy25_to_fy26_growth_by_source"] = {k: {"chg": b - a, "share_of_total_chg_pct": round((b - a) / (272310 - 196527) * 100, 1)} for k, (a, b) in d.items()}
pan["underground_oz_growth_pct"] = pct(92643, 105478)
pan["group_produced_growth"] = (272310 - 196527, pct(196527, 272310))
pan["mtr_tailings_fy26_vs_total"] = {"tailings": 46164, "buy_in": 5763, "total": 46164 + 5763, "printed_total": 51927}
out["pan_production"] = pan

# ---------------- PAN per-unit cost cross-checks (p49 vs p50) -------------
def per_kg(amount_m, oz):
    return round(amount_m * 1e6 / (oz / OZ_PER_KG))
xc = {}
xc["tennant_fy25_allin_A$kg_from_A$58.1m_sold1179"] = {"derived": per_kg(58.1, 1179), "range": [per_kg(58.05, 1179), per_kg(58.15, 1179)], "printed": 1584835}
xc["tennant_fy25_us$oz_from_A$kg"] = {"derived": round(1584835 / OZ_PER_KG / 1.54), "printed": 32041}
xc["tennant_fy26_allin_A$kg_from_A$209.3m_sold32124"] = {"derived": per_kg(209.3, 32124), "range": [per_kg(209.25, 32124), per_kg(209.35, 32124)], "printed": 205143}
xc["tennant_fy26_aisc_A$kg_from_A$106.8m"] = {"derived": per_kg(106.8, 32124), "printed": 106900}
xc["tennant_fy26_cash_A$kg_from_A$81.0m"] = {"derived": per_kg(81.0, 32124), "printed": 81099}
xc["tennant_fy26_us$oz_from_205143"] = {"derived": round(205143 / OZ_PER_KG / 1.47), "printed": 4339}
xc["elikhulu_fy26_allin_from_1515.8m_sold57092"] = {"derived": per_kg(1515.8, 57092), "printed": 853597}
xc["elikhulu_fy25_aisc_from_1039.4m_sold53092"] = {"derived": per_kg(1039.4, 53092), "printed": 629441}
xc["elikhulu_fy25_allin_from_1130.9m_sold53092"] = {"derived": per_kg(1130.9, 53092), "range": [per_kg(1130.85, 53092), per_kg(1130.95, 53092)], "printed": 68843}
xc["fy25_aisc_ex_buyin_mining_total_vs_components"] = {"barberton": 1880, "evander": 1418, "mining_total_printed": 2688,
                                                       "total_exceeds_both_components": 2688 > max(1880, 1418)}
xc["fy25_barberton_aisc_vs_ex_buyin"] = {"aisc": 2065, "ex_buyin": 1880, "fy25_barberton_buyin_oz": 0}
out["pan_cost_crosschecks"] = xc

# ---------------- PAN US$ AISC change decomposition (FX vs ZAR cost vs Tennant mix), approximate -------------
sa25 = 934517 / 18.17 / OZ_PER_KG
sa26 = 985551 / 16.90 / OZ_PER_KG
fx_only = sa25 * (18.17 / 16.90) - sa25
out["pan_aisc_decomposition"] = {
    "us$_aisc_group": [1600, 1867, 267],
    "sa_only_us$_from_zar_kg": [round(sa25, 1), round(sa26, 1)],
    "fx_effect_us$": round(fx_only, 1), "zar_cost_effect_us$": round(sa26 - sa25 - fx_only, 1),
    "residual_tennant_mix_us$": round(1867 - sa26, 1) - round(1600 - sa25, 1),
    "fx_share_of_increase_pct": round(fx_only / 267 * 100, 1),
    "caveat": "Approximation: ZAR/kg rows exclude Tennant; per-unit denominators and rounding not disclosed in capture.",
}
out["pan_zar_revenue_decomposition"] = {
    "zar_price_sa_pct": pct(1595761, 2308329),
    "sa_sold_oz": [196926 - 1179, 272373 - 32124], "sa_sold_pct": pct(196926 - 1179, 272373 - 32124),
    "price_x_volume": round((2308329 / 1595761) * ((272373 - 32124) / (196926 - 1179)) * 100 - 100, 2),
    "zar_revenue_pct": pct(9715.6, 17249.1), "us$_price_pct": pct(2735, 4235),
}
out["pan_other_sums"] = {
    "capex_fy26_ops": round(40.1 + 70.9 + 32.6 + 71.3, 1), "capex_fy25_ops": round(27.6 + 47.9 + 52.2 + 35.8, 1),
    "ebitda_fy26_leaves": round(142.4 + 120.9 + 29.4 + 171.4 + 155.9 + 43.0, 1), "ebitda_fy26_ops": round(171.9 + 292.3 + 155.9 + 43.0, 1),
    "revenue_minus_cop": round(17249.1 - 6431.7, 1), "ebitda_zar_at_16.90": round(663.1 * 16.90, 2),
    "buyin_tonnes_pct": pct(92536, 887646), "single_group_check_118853_plus_153458": 118853 + 153458,
}

# ---------------- Accounting from receipts -------------
def rec(p):
    j = json.loads(Path(p).read_text(encoding="utf-8"))
    u = j.get("usage", {}) or {}
    return {"cost": j.get("cost_usd"), "prompt": u.get("prompt_tokens"), "completion": u.get("completion_tokens"), "elapsed": j.get("elapsed_seconds")}
calls = {
    "ntu_single": rec(ORIG / "receipts/ntu_assets_single.json"), "ntu_meaning": rec(ORIG / "receipts/ntu_assets_meaning.json"),
    "ntu_movement": rec(ORIG / "receipts/ntu_assets_movement.json"), "ntu_why": rec(ORIG / "receipts/ntu_assets_why.json"),
    "pan_meaning": rec(ORIG / "receipts/pan_dense_meaning.json"), "pan_movement": rec(ORIG / "receipts/pan_dense_movement.json"),
    "pan_why": rec(NEW / "receipts/pan_dense_why_attempt1.json"), "pan_single": rec(NEW / "receipts/pan_dense_single_attempt1.json"),
}
def tot(keys, f):
    vals = [calls[k][f] for k in keys]
    return None if any(v is None for v in vals) else round(sum(vals), 10)
acc = {"calls": calls}
for case in ("ntu", "pan"):
    three = [f"{case}_meaning", f"{case}_movement", f"{case}_why"]
    acc[case] = {"single": {f: calls[f"{case}_single"][f] for f in ("cost", "prompt", "completion", "elapsed")},
                 "three": {f: tot(three, f) for f in ("cost", "prompt", "completion", "elapsed")}}
    acc[case]["cost_ratio"] = round(acc[case]["three"]["cost"] / acc[case]["single"]["cost"], 3)
    acc[case]["time_ratio"] = round(acc[case]["three"]["elapsed"] / acc[case]["single"]["elapsed"], 3)
acc["all_successful_cost"] = round(sum(c["cost"] for c in calls.values()), 10)
out["accounting"] = acc

(RUN / "calculations.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
print(json.dumps(out, indent=1))

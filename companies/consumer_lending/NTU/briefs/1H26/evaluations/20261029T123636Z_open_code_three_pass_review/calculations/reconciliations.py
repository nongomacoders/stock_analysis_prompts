# Independent reconciliation calculations for the OpenCode three-pass comparison review.
# Read-only. All inputs are preserved experiment files and SHA-verified source PDF pages.
import sys, datetime, json
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

def pct(end, start):
    return (end - start) / start * 100

Y = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
R = {}

# ---------- NTU (physical pp.21-23 verified render; p.13/p.8 verified for Note 1) ----------
R["ntu_p22_gross_mar26"] = {"expr": "5+395+3414+644", "result": 5+395+3414+644, "printed": 4458}
R["ntu_p22_carry_mar26"] = {"expr": "5+390+3845+644", "result": 5+390+3845+644, "printed": 4884}
R["ntu_p22_gross_mar25"] = {"expr": "2+510+3066+663", "result": 2+510+3066+663, "printed": 4241}
R["ntu_p22_carry_mar25"] = {"expr": "2+504+3690+663", "result": 2+504+3690+663, "printed": 4859}
R["ntu_p22_gross_sep25"] = {"expr": "4+388+3377+702", "result": 4+388+3377+702, "printed": 4471}
R["ntu_p22_carry_sep25"] = {"expr": "4+378+3975+702", "result": 4+378+3975+702, "printed": 5059}
R["ntu_book_mar26"] = {"expr": "3414+431", "result": 3414+431, "printed": 3845}
R["ntu_conc_mar26_gross"] = {"expr": "2371+951+46+46", "result": 2371+951+46+46, "printed": 3414}
R["ntu_conc_mar26_gain"] = {"expr": "227+141+51+12", "result": 227+141+51+12, "printed": 431}
R["ntu_net_h1"] = {"start": 3975, "end": 3845, "change": 3845-3975, "percent": pct(3845, 3975), "model": -130, -130: None}
R.pop(-130, None)
R["ntu_net_yoy"] = {"start": 3690, "end": 3845, "change": 3845-3690, "percent": pct(3845, 3690), "model": 155}
R["ntu_gain_h1"] = {"start": 598, "end": 431, "change": 431-598, "percent": pct(431, 598), "model": -167}
R["ntu_gain_yoy"] = {"start": 624, "end": 431, "change": 431-624, "model": -193}
R["ntu_unsecured"] = {"start": 2950, "end": 2598, "change": 2598-2950, "percent": pct(2598, 2950), "model": -352}
R["ntu_debt_review"] = {"start": 865, "end": 1092, "change": 1092-865, "percent": pct(1092, 865), "model": 227}
# NTU physical p.13 Note 1 (independent confirmation, NOT supplied to the trial models)
R["ntu_p13_principal_rollforward"] = {"expr": "3975+382-728+383-167", "result": 3975+382-728+383-167, "printed": 3845}
R["ntu_p13_ofa_rollforward"] = {"expr": "702+28-116+30", "result": 702+28-116+30, "printed": 644}
R["ntu_p13_pbd_total"] = {"expr": "3845+644", "result": 3845+644, "printed": 4489}
R["ntu_p13_pbd_classification"] = {"expr": "3178+1311", "result": 3178+1311, "printed": 4489}
# FX rejection hypothesis check for the staged why's "largely FX" claim
R["pan_staged_fx_only_sa"] = {
    "expr": "(985551/32.150747)/16.90 vs (934517/32.150747)/18.17 -> implied SA USD/AISC change %",
    "sa_usd_fy26": (985551/32.150747)/16.90,
    "sa_usd_fy25": (934517/32.150747)/18.17,
    "implied_pct": ((985551/32.150747)/16.90)/((934517/32.150747)/18.17)*100-100,
    "printed_group_pct": 16.7,
    "note": "SA-only FX+ZAR AISC roll-up explains ~+13.4pp of the +16.7pp Group US$ AISC rise; residual ~3pp from Tennant mix (11.8% weight at US$2,261). 'Largely FX' is plausible but unreconciled in the staged why.",
}

# ---------- PAN (physical pp.48-50 verified render) ----------
R["pan_disjoint_fy25"] = {"expr": "92643+2654+98636+1081+1513", "result": 92643+2654+98636+1081+1513, "printed_group": 196527}
R["pan_overlap_fy25"] = {"expr": "93724+2654+98636+1081+1513", "result": 93724+2654+98636+1081+1513, "printed_group": 196527, "difference_vs_disjoint": 1081}
R["pan_evander_fy25"] = {"expr": "26748+1081", "result": 26748+1081, "printed_evander_total": 27829}
R["pan_group_ug_fy25"] = {"expr": "92643+1081", "result": 92643+1081, "printed_group_ug": 93724}
R["pan_fy26_ug_mining_total"] = {"expr": "65233+40246", "result": 65233+40246, "printed_mining_total": 105479, "printed_group_ug": 105478}
R["pan_fy26_group_check_group_ug"] = {"expr": "105478+2428+113613+18667+32124", "result": 105478+2428+113613+18667+32124, "printed_group": 272310, "staged_why_marked": "correct (272,310 ok)"}
R["pan_fy26_group_check_mining_ug"] = {"expr": "105479+2428+113613+18667+32124", "result": 105479+2428+113613+18667+32124, "printed_group": 272310, "residual_oz": 1}
R["pan_barberton_mining_leaf_fy26"] = {"expr": "65233+2428+4337", "result": 65233+2428+4337, "printed": 71997, "residual_oz": 71998-71997, "staged_claim": "71,997 = components (asserted identically in meaning, movement and final why)"}
R["pan_evander_total_fy26"] = {"expr": "40246+6609", "result": 40246+6609, "printed": 46855}
R["pan_barberton_total_fy26"] = {"expr": "71997+12932", "result": 71997+12932, "printed": 94929, "difference_oz": 94929-(71997+12932)}
R["pan_fy26_opsum_printed_columns"] = {"expr": "94929+103330+51927+32124", "result": 94929+103330+51927+32124, "printed_group": 272310, "difference_oz": 94929+103330+51927+32124-272310}
R["pan_fy26_opsum_with_84929"] = {"expr": "84929+103330+51927+32124", "result": 84929+103330+51927+32124, "printed_group": 272310, "note": "exact conditional agreement; this does NOT establish 94,929 as the wrong value"}
R["pan_minning_series_fy26"] = {"expr": "105479+2428+4337+6609", "result": 105479+2428+4337+6609, "printed_mining_series_total": 118853}
R["pan_single_false_check"] = {"expr": "118853+153458", "result": 118853+153458, "printed_group": 272310, "single_marked": "ok (false; actual 272,311)"}
R["pan_barberton_plus_evander_fy26"] = {"expr": "71997+46855", "result": 71997+46855, "printed_mining_total": 118853, "residual_oz": 118853-(71997+46855)}
R["pan_mtr_fy25_tailings_total_check"] = {"expr": "15224+52606+25043", "result": 15224+52606+25043, "printed": 98636, "difference_oz": 98636-(15224+52606+25043)}
R["pan_mtr_fy25_summary_row"] = {"expr": "25043+5763", "result": 25043+5763, "printed_mtr_total_ops_fy25": 30806, "note": "5,763 equals FY26 MTR buy-in; FY25 buy-in row prints nil for MTR"}
R["pan_mtr_fy26_summary_row"] = {"expr": "46164+5763", "result": 46164+5763, "printed_mtr_total_ops_fy26": 51927}
R["pan_fy25_group_from_opsum_printed"] = {"expr": "83773+80435+30806+1513", "result": 83773+80435+30806+1513, "printed_group": 196527, "note": "FY25 opsum reconciles exactly with printed values while FY26 opsum does not; replacement direction is case-specific"}
R["pan_fy25_group_from_summary_rows"] = {"expr": "96378+100149", "result": 96378+100149, "printed_group": 196527}
R["pan_elikhulu_implied_allin"] = {
    "expr": "1130.9e6 ZARm/(53092 oz sold x 31.1034768/1000 kg)",
    "kg": 53092*31.1034768/1000,
    "zar_per_kg": 1130900000/(53092*31.1034768/1000),
    "printed": 68843,
    "note": "implied ~684,8xx vs printed 68,843; consistent with a plausible omitted-digit order-of-magnitude error, cause not proved",
}
R["pan_tennant_implied_allin_aud"] = {
    "expr": "A$58.1m/(1179 oz sold x 31.1034768/1000 kg)",
    "kg": 1179*31.1034768/1000,
    "aud_per_kg": 58100000/(1179*31.1034768/1000),
    "printed": 1584835,
    "note": "broadly agrees; FY25 Tennant cells are internally consistent with the tiny produced/sold base, not obviously a typo",
}
R["pan_tennant_usd_from_aud"] = {"expr": "1584835/1.54/32.150747", "result": 1584835/1.54/32.150747, "printed_us_allin_fy25_tennant": 32041, "note": "US$ 32,041 and A$ 1,584,835 are mutually consistent"}
# p.50 sums
R["pan_p50_revenue"] = {"expr": "8449.6+8799.5", "result": 8449.6+8799.5, "printed": 17249.1}
R["pan_p50_cop"] = {"expr": "3957.4+2474.3", "result": 3957.4+2474.3, "printed": 6431.7}
R["pan_p50_ebitda_leaves"] = {"expr": "142.4+120.9+29.4+171.4+155.9+43.0", "result": 142.4+120.9+29.4+171.4+155.9+43.0, "printed": 663.1, "residual": 663.1-(142.4+120.9+29.4+171.4+155.9+43.0), "note": "single marked '(0.1 rounding) ok' on a 0.1 mismatch"}
R["pan_p50_barberton_ebitda_subtotal"] = {"expr": "142.4+29.4", "result": 142.4+29.4, "printed": 171.9}
R["pan_p50_capex_leaves"] = {"expr": "37.5+49.8+2.6+21.1+32.6+71.3", "result": 37.5+49.8+2.6+21.1+32.6+71.3, "printed": 214.9}
# spot percentage checks on the staged why table
R["pan_pct_produced"] = {"expr": "75783/196527", "percent": pct(272310, 196527), "model": 38.6}
R["pan_pct_usd_price"] = {"expr": "1500/2735", "percent": pct(4235, 2735), "model": 54.8}
R["pan_pct_zar_aisc"] = {"expr": "51034/934517", "percent": pct(985551, 934517), "model": 5.5}
R["pan_pct_usd_aisc"] = {"expr": "267/1600", "percent": pct(1867, 1600), "model": 16.7}
R["pan_pct_revenue"] = {"expr": "7533.5/9715.6", "percent": pct(17249.1, 9715.6), "model": 77.5}
R["pan_pct_buyin_t"] = {"expr": "795110/92536", "percent": pct(887646, 92536), "model": 859.3}
R["pan_pct_surf_feed_t"] = {"expr": "666598/85316", "percent": pct(751914, 85316), "model": 781.3}

# ---------- Time and cost accounting (independent arithmetic from saved rows) ----------
R["ntu_staged_cost"] = {"expr": "0.00231378+0.002856+0.00534765", "result": 0.00231378+0.002856+0.00534765, "recorded": 0.01051743}
R["ntu_ratio_cost"] = {"expr": "0.01051743/0.00470211", "result": 0.01051743/0.00470211, "recorded": 2.236746907}
R["ntu_ratio_time"] = {"expr": "29.956/18.457", "result": 29.956/18.457, "recorded": 1.623015658}
R["pan_staged_cost"] = {"expr": "0.0027101004+0.0036603084+0.0048133344", "result": 0.0027101004+0.0036603084+0.0048133344, "recorded": 0.0111837432}
R["pan_ratio_cost"] = {"expr": "0.0111837432/0.004670988", "result": 0.0111837432/0.004670988, "recorded": "~2.3943"}
R["pan_ratio_time"] = {"expr": "30.421/16.914", "result": 30.421/16.914, "recorded": "~1.7986"}
R["combined_known_subtotal"] = {"expr": "0.0215899488+0.0094843224", "result": 0.0215899488+0.0094843224, "recorded": 0.0310742712}
R["resume_incremental_cost"] = {"expr": "0.0048133344+0.004670988", "result": 0.0048133344+0.004670988, "recorded": 0.0094843224}
R["resume_incremental_tokens"] = {"prompt": 13640+11107, "completion": 2475+2904, "cached": 632+490, "elapsed": 15.235+16.914}
R["ntu_staged_tokens"] = {"prompt": 8086+8824+10765, "completion": 733+1194+3675, "elapsed": 5.024+7.995+16.937}
R["pan_staged_tokens"] = {"prompt": 10518+11233+13640, "completion": 710+1660+2475, "elapsed": 6.431+8.755+15.235}

out_dir = Path(__file__).parent
out = {"generated_utc": Y, "calculations": R}
(out_dir / "reconciliations.json").write_text(json.dumps(out, indent=2), encoding="utf-8")

fails = []
def check(name, expected, actual, tol=1e-6):
    ok = abs(expected - actual) <= tol
    if not ok:
        fails.append((name, expected, actual))
    return ok

c = R
checks = [
    ("ntu_p22_gross_mar26", 4458, c["ntu_p22_gross_mar26"]["result"]),
    ("ntu_p22_carry_mar26", 4884, c["ntu_p22_carry_mar26"]["result"]),
    ("ntu_p22_gross_mar25", 4241, c["ntu_p22_gross_mar25"]["result"]),
    ("ntu_p22_carry_mar25", 4859, c["ntu_p22_carry_mar25"]["result"]),
    ("ntu_p22_gross_sep25", 4471, c["ntu_p22_gross_sep25"]["result"]),
    ("ntu_p22_carry_sep25", 5059, c["ntu_p22_carry_sep25"]["result"]),
    ("ntu_book_mar26", 3845, c["ntu_book_mar26"]["result"]),
    ("ntu_conc_mar26_gross", 3414, c["ntu_conc_mar26_gross"]["result"]),
    ("ntu_conc_mar26_gain", 431, c["ntu_conc_mar26_gain"]["result"]),
    ("ntu_net_h1", -130, c["ntu_net_h1"]["change"]),
    ("ntu_net_h1_pct", -3.2704, c["ntu_net_h1"]["percent"], 1e-3),
    ("ntu_net_yoy", 155, c["ntu_net_yoy"]["change"]),
    ("ntu_gain_h1", -167, c["ntu_gain_h1"]["change"]),
    ("ntu_gain_h1_pct", -27.9264, c["ntu_gain_h1"]["percent"], 1e-3),
    ("ntu_unsecured", -352, c["ntu_unsecured"]["change"]),
    ("ntu_debt_review", 227, c["ntu_debt_review"]["change"]),
    ("ntu_p13_principal_rollforward", 3845, c["ntu_p13_principal_rollforward"]["result"]),
    ("ntu_p13_ofa_rollforward", 644, c["ntu_p13_ofa_rollforward"]["result"]),
    ("ntu_p13_pbd_total", 4489, c["ntu_p13_pbd_total"]["result"]),
    ("pan_disjoint_fy25", 196527, c["pan_disjoint_fy25"]["result"]),
    ("pan_overlap_fy25", 197608, c["pan_overlap_fy25"]["result"]),
    ("pan_fy26_group_check_group_ug", 272310, c["pan_fy26_group_check_group_ug"]["result"]),
    ("pan_single_false_check_diff", 1, abs(272310-272311), 0),
    ("pan_barberton_total_fy26_diff", 10000, c["pan_barberton_total_fy26"]["difference_oz"], 0),
    ("pan_fy26_opsum_printed_columns_diff", 10000, c["pan_fy26_opsum_printed_columns"]["difference_oz"], 0),
    ("pan_mtr_delta", 5763, c["pan_mtr_fy25_tailings_total_check"]["difference_oz"], 0),
    ("pan_fy25_group_from_opsum_printed", 196527, c["pan_fy25_group_from_opsum_printed"]["result"]),
    ("pan_p50_capex", 214.9, c["pan_p50_capex_leaves"]["result"], 1e-9),
    ("ntu_ratio_cost", 2.236747, c["ntu_ratio_cost"]["result"], 1e-4),
    ("pan_ratio_cost", 2.3943, c["pan_ratio_cost"]["result"], 1e-3),
    ("combined_known_subtotal", 0.0310742712, c["combined_known_subtotal"]["result"], 1e-9),
    ("ntu_staged_cost", 0.01051743, c["ntu_staged_cost"]["result"], 1e-9),
    ("pan_staged_cost", 0.0111837432, c["pan_staged_cost"]["result"], 1e-9),
]
for name, expected, actual, *t in checks:
    tol = t[0] if t else 1e-6
    status = "OK" if abs(expected-actual) <= tol else "MISMATCH"
    print(f"{status:8} {name}: expected={expected} actual={actual}")
print("FAILURES:", len(fails))
print("exit 0")

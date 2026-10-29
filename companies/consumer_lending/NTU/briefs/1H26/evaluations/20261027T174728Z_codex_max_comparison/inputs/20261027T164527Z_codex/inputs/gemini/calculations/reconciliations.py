import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

output_lines = []

def log(msg=""):
    print(msg)
    output_lines.append(msg)

log("================================================================================")
log("INDEPENDENT RECONCILIATIONS & FORENSIC AUDIT CALCULATIONS — NTU 1H26")
log("Evaluator: Gemini (Gemini 3.8 Flash High) | Date: 2026-10-27 | Target: Nutun Ltd")
log("================================================================================\n")

# 1. SOTP ARITHMETIC, DOUBLE DISCOUNTING & PLUG ANALYSIS
log("1. SOTP ARITHMETIC, DOUBLE DISCOUNTING & CIRCULAR PLUG ANALYSIS")
log("----------------------------------------------------------------")
cev_sa_pbd = 3845.0 * 0.55       # 2114.75 -> 2115
cev_sa_other = 644.0 * 0.70      # 450.8 -> 451
cev_sa_agency = 250.0 * 3.0      # 750.0
cev_intl_bpo = 180.0 * 4.0       # 720.0
total_ev = cev_sa_pbd + cev_sa_other + cev_sa_agency + cev_intl_bpo
log(f"Component TEVs: SA PBD={cev_sa_pbd:.2f}, SA Other={cev_sa_other:.2f}, SA Agency={cev_sa_agency:.2f}, Intl BPO={cev_intl_bpo:.2f}")
log(f"Sum of Components (TEV): {total_ev:.2f} (Model reports 4,036)")

# Net debt deduction in DeepSeek model (FY27E)
ibd = 3850.0
od = 310.0
leases = 335.0
cash = 95.0
net_debt = ibd + od + leases - cash
equity_val_pre_discount = total_ev - net_debt
log(f"FY27E Net Debt: IBD({ibd}) + OD({od}) + Leases({leases}) - Cash({cash}) = {net_debt:.2f}")
log(f"Pre-discount Equity Value from operations: TEV({total_ev:.2f}) - Net Debt({net_debt:.2f}) = {equity_val_pre_discount:.2f} (Model reports -364)")

# The plug row: "Add: Other assets net of other liabilities: 1,479"
plug_row = 1479.0
adj_equity = equity_val_pre_discount + plug_row
log(f"DeepSeek Plug Row: {plug_row:.2f} -> Adjusted Equity: {adj_equity:.2f} (Model reports 1,115)")
log(f"Note: On DeepSeek's FY27E Balance Sheet: Other Assets = 1,315, Other Liab = 765 -> Net = 550, NOT 1,479!")
log(f"The 1,479 is a circular plug to force Adjusted Equity to equal FY27E Book Value of Equity (1,115).\n")

# DeepSeek Per-share and Discount arithmetic
shares = 780.7
val_per_share_pre_discount = adj_equity / shares
log(f"Step 1: Adjusted Equity / Shares = {adj_equity:.2f} / {shares} = R{val_per_share_pre_discount:.4f} per share")

disc_25_pct_equity = adj_equity * 0.25
target_equity_after_25 = adj_equity - disc_25_pct_equity
per_share_after_single_25 = target_equity_after_25 / shares
log(f"Step 2: Aggregate 25% discount: {adj_equity:.2f} - {disc_25_pct_equity:.2f} = {target_equity_after_25:.2f}")
log(f"        Per share after 25% discount: {target_equity_after_25:.2f} / {shares} = R{per_share_after_single_25:.4f}")
log(f"        (Model reports SOTP Fair Value per Share: R1.07)")

disc_25_again = per_share_after_single_25 * 0.75
log(f"Step 3: DeepSeek's double-discounting error: 1.07 * (1 - 0.25) = R{disc_25_again:.4f}")
log(f"        (Model claims pre-discount R1.43 less 25% = R0.80, which is mathematically false! R1.428 * 0.75 = R1.071)")

haircut_to_055 = 0.55 / disc_25_again
haircut_pct = (1.0 - haircut_to_055) * 100
total_discount_from_143 = (1.0 - 0.55 / val_per_share_pre_discount) * 100
log(f"Step 4: Further haircut from R0.8034 to R0.55: {haircut_pct:.2f}% unmodeled reduction")
log(f"        Total cumulative discount from pre-discount R1.43 to target R0.55: {total_discount_from_143:.2f}%\n")

# 2. PBD AMORTISATION FOOTNOTE RECONCILIATION
log("2. PBD AMORTISATION FOOTNOTE ARITHMETIC RECONCILIATION")
log("-----------------------------------------------------")
# Note 1.1:
caeir_interest = 383.0
impairment_loss = 167.0
net_collections = 728.0
# Note 1.2:
fv_movements = 30.0
cash_collections_12 = 116.0

# DeepSeek sum:
naive_sum = caeir_interest + impairment_loss + net_collections + fv_movements + cash_collections_12
log(f"DeepSeek naive un-signed sum: 383 + 167 + 728 + 30 + 116 = {naive_sum:.1f} (DeepSeek reported 1,424 and alleged error)")

# True algebraic accounting formula:
# Amortisation = (Net collections - Income)
# Note 1.1 Net Run-off: Net collections (728) - [CAEIR interest (383) - Impairment (167)] = 728 - 216 = 512
pbd_11_runoff = net_collections - caeir_interest + impairment_loss
# Note 1.2 Net Run-off: Collections (116) - Fair value gain (30) = 86
pbd_12_runoff = cash_collections_12 - fv_movements
total_amortisation = pbd_11_runoff + pbd_12_runoff
log(f"True Note 1.1 principal run-off: 728 - 383 + 167 = {pbd_11_runoff:.1f}")
log(f"True Note 1.2 principal run-off: 116 - 30 = {pbd_12_runoff:.1f}")
log(f"Total Portfolio Amortisation: {pbd_11_runoff:.1f} + {pbd_12_runoff:.1f} = {total_amortisation:.1f} (matches reported R597m within 1m rounding)")
log(f"Verdict: Footnote is mathematically correct under net portfolio run-off signs; DeepSeek's claim of non-reconciliation is a FALSE ALLEGATION.\n")

# 3. POCI ACCOUNTING VS CONVENTIONAL ECL
log("3. POCI CUMULATIVE IMPAIRMENT GAIN VS CONVENTIONAL ECL")
log("-----------------------------------------------------")
gross_carrying_amt = 3414.0
cumulative_impairment_gain = 431.0
carrying_value = gross_carrying_amt + cumulative_impairment_gain
log(f"Gross carrying amount (p.23): {gross_carrying_amt:.1f}")
log(f"Cumulative impairment gain (p.23, p.24): +{cumulative_impairment_gain:.1f}")
log(f"Net carrying value (p.23, p.8): {carrying_value:.1f}")
log(f"Ratio 431 / 3414 = {cumulative_impairment_gain / gross_carrying_amt * 100:.2f}%")
log(f"DeepSeek treated 431m as an ECL loss reserve that collapsed from 20.4% to 12.6%.")
log(f"Primary note states: 'The cumulative impairment gain of R431 million relates to elevated performance, above the investment base-case.'")
log(f"The unwinding of this gain (-167m P&L impairment) reflects deteriorating collections vs base case, but it is NOT an ECL loss coverage reserve.\n")

# 4. BOOK VALUE PER SHARE VS SHARE CAPITAL
log("4. BOOK VALUE PER SHARE VS SHARE CAPITAL ATTRIBUTION")
log("----------------------------------------------------")
share_cap = 5410.0
retained_loss = -4111.0
other_res = 30.0
total_equity_statutory = share_cap + retained_loss + other_res
shares_outstanding = 780.651033

log(f"Gross Share Capital: R{share_cap:.1f}m / {shares_outstanding:.2f}m shares = R{share_cap / shares_outstanding:.2f}")
log(f"Statutory Total Equity: R{total_equity_statutory:.1f}m / {shares_outstanding:.2f}m shares = R{total_equity_statutory / shares_outstanding:.2f}")
log(f"DeepSeek's claim that treasury shares were bought at R1 vs 'R6.90 book value' was an error: R6.90 is contributed capital, not book value (R1.70).\n")

# 5. MARKET PRICING, RATINGS & SENSITIVITY
log("5. MARKET PRICING, TARGET PRICE & DYNAMIC BANDS")
log("-----------------------------------------------")
target = 0.55
ref_price = 0.89
live_price = 0.90
sb_max = 0.42
buy_max = 0.48
hold_max = 0.58
sell_max = 0.65

upside_ref = (target - ref_price) / ref_price * 100
upside_live = (target - live_price) / live_price * 100
log(f"Target: R{target:.2f} | Reference: R{ref_price:.2f} -> Upside: {upside_ref:.2f}%")
log(f"Live Price: R{live_price:.2f} -> Live Upside: {upside_live:.2f}%")
log(f"Rating Bands: SB <= {sb_max} | B <= {buy_max} | H <= {hold_max} | S <= {sell_max} | Strong Sell > {sell_max}")
log(f"At Reference R0.89: R0.89 > {sell_max} -> Band is STRONG SELL (Model static note had SELL)")
log(f"At Live Price R0.90: R0.90 > {sell_max} -> Band is STRONG SELL")

out_file = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T163950Z_gemini/calculations/reconciliations_output.txt")
out_file.write_text("\n".join(output_lines), encoding="utf-8")
py_file = Path("companies/consumer_lending/NTU/briefs/1H26/evaluations/20261027T163950Z_gemini/calculations/reconciliations.py")
py_file.write_text(Path(__file__).read_text(encoding="utf-8") if "__file__" in locals() else "", encoding="utf-8")
log(f"\nSaved calculations to {out_file}")

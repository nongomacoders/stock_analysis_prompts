import sys, json
from pathlib import Path

cols = {
    'FY25A': {'rev': 1435, 'cor': -732, 'gp': 703, 'pbd': 244, 'opc': -1063, 'nfc': -91, 'noi': 69, 'eq': -48, 'op': -186, 'non_op': 38, 'pbt': -148, 'tax': 35, 'pat_cont': -113, 'disc': -125, 'pat_tot': -238},
    '1H26A': {'rev': 711, 'cor': -385, 'gp': 326, 'pbd': 69, 'opc': -445, 'nfc': -39, 'noi': 11, 'eq': -1, 'op': -79, 'non_op': -13, 'pbt': -92, 'tax': 29, 'pat_cont': -63, 'disc': 0, 'pat_tot': -63},
    'FY26E': {'rev': 1410, 'cor': -770, 'gp': 640, 'pbd': 131, 'opc': -845, 'nfc': -80, 'noi': 20, 'eq': 0, 'op': -134, 'non_op': 0, 'pbt': -134, 'tax': 34, 'pat_cont': -100, 'disc': 0, 'pat_tot': -100},
    'FY27E': {'rev': 1420, 'cor': -760, 'gp': 660, 'pbd': 100, 'opc': -730, 'nfc': -70, 'noi': 20, 'eq': 0, 'op': -20, 'non_op': 0, 'pbt': -20, 'tax': 5, 'pat_cont': -15, 'disc': 0, 'pat_tot': -15},
    'FY28E': {'rev': 1450, 'cor': -750, 'gp': 700, 'pbd': 90, 'opc': -640, 'nfc': -70, 'noi': 20, 'eq': 0, 'op': 100, 'non_op': 0, 'pbt': 100, 'tax': -25, 'pat_cont': 75, 'disc': 0, 'pat_tot': 75}
}

print("=== INCOME STATEMENT ARITHMETIC ===")
for name, c in cols.items():
    gp_chk = c['rev'] + c['cor'] == c['gp']
    op_calc = c['gp'] + c['pbd'] + c['opc'] + c['nfc'] + c['noi'] + c['eq']
    pbt_calc = c['op'] + c['non_op']
    pat_calc = c['pbt'] + c['tax']
    tot_calc = c['pat_cont'] + c['disc']
    print(f"{name}: GP: {gp_chk}, OP calc: {op_calc} (stated {c['op']}), PBT calc: {pbt_calc} (stated {c['pbt']}), PAT calc: {pat_calc} (stated {c['pat_cont']}), Tot: {tot_calc} (stated {c['pat_tot']})")

print("\n=== HEPS ARITHMETIC ===")
heps_data = {
    'FY25A': {'pat': -113, 'shares': 784.3, 'stated_heps': -14.4},
    '1H26A': {'pat': -63, 'shares': 782.1, 'stated_heps': -8.1},
    'FY26E': {'pat': -100, 'shares': 782.1, 'stated_heps': -12.8},
    'FY27E': {'pat': -15, 'shares': 780.7, 'stated_heps': -1.9},
    'FY28E': {'pat': 75, 'shares': 780.7, 'stated_heps': 9.6}
}
for name, h in heps_data.items():
    calc_heps = (h['pat'] / h['shares']) * 100
    print(f"{name}: calc HEPS = {calc_heps:.2f}c, stated = {h['stated_heps']}c, diff = {calc_heps - h['stated_heps']:.2f}c")

print("\n=== EQUITY ROLLFORWARD / BOOK VALUE RECONCILIATION ===")
# Equity opening + PAT - dividends/buybacks = Equity closing
# FY25A equity 1396 -> 1H26A equity 1329 (drop of 67; PAT was -63, treasury share buyback was R4m -> -63 - 4 = -67 -> exactly 1329!)
# FY26E equity 1229: 1329 - 100 = 1229 (exact!)
# FY27E equity 1214: 1229 - 15 = 1214 (exact!)
# FY28E equity 1289: 1214 + 75 = 1289 (exact!)
print("Equity rollforwards:")
print(f"FY26E: 1329 - 100 = {1329 - 100} (stated 1229)")
print(f"FY27E: 1229 - 15 = {1229 - 15} (stated 1214)")
print(f"FY28E: 1214 + 75 = {1214 + 75} (stated 1289)")

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

adj_equity = 1115.0
shares = 780.7
val_per_share_pre_discount = adj_equity / shares
print(f"Value per share pre-discount: {adj_equity} / {shares} = {val_per_share_pre_discount:.4f}")

disc_25_pct = val_per_share_pre_discount * 0.75
print(f"After single 25% discount: {disc_25_pct:.4f}")

disc_25_pct_twice = disc_25_pct * 0.75
print(f"After double 25% discount: {disc_25_pct_twice:.4f}")

haircut_to_055 = 0.55 / disc_25_pct_twice
print(f"Haircut from 0.8028 to 0.55: {1 - haircut_to_055:.4%}")

haircut_from_107_to_055 = 0.55 / disc_25_pct
print(f"Haircut from 1.0712 to 0.55: {1 - haircut_from_107_to_055:.4%}")

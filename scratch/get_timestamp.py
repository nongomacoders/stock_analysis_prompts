from datetime import datetime, timezone

utc_now = datetime.now(timezone.utc)
stamp = utc_now.strftime("%Y%m%dT%H%M%SZ")
print("UTC timestamp:", stamp)

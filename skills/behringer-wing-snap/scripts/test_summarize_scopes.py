"""Self-check for summarize_scopes: nested string scopes must not report 0."""
from inspect_wing_snap import summarize_scope_value, summarize_scopes

# compact string
s = summarize_scope_value("++-+")
assert s["enabled_count"] == 3 and s["disabled_count"] == 1, s

# dict of booleans (legacy form)
b = summarize_scope_value({"a": True, "b": False})
assert b["enabled_count"] == 1 and b["disabled_count"] == 1, b

# nested WING scope: dict of compact strings (the bug this fixes)
out = summarize_scopes({"output": {"LCL": "++++++++", "A": "----"}})
assert out["output"]["LCL"]["enabled_count"] == 8, out
assert out["output"]["A"]["disabled_count"] == 4, out
print("ok")

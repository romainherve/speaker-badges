"""Check module footprints (with clearance) for XY overlaps within each layer,
and report gaps between neighbors so we know if a divider wall can even fit.

A negative gap = the pockets (or modules) overlap.
"""

import speaker_badge as sb

CLEAR = sb.FIT_CLEAR
RIB = sb.RIB_T


def span(center, w, h):
    cx, cy = center
    return (cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2)


def gap_y(a, b):
    """Vertical gap between module a (upper) and b (lower): a.ymin - b.ymax."""
    return a[2] - b[3]


def gap_x(a, b):
    """Horizontal gap between module a (right) and b (left): a.xmin - b.xmax."""
    return a[0] - b[1]


def report(name, modules):
    print(f"\n=== {name} ===")
    for n, c, w, h in modules:
        s = span(c, w, h)
        print(f"  {n:14s} x[{s[0]:7.2f},{s[1]:7.2f}]  y[{s[2]:7.2f},{s[3]:7.2f}]")


# Cavity interior (rough, straight section)
CAV_TOP = sb.CAVITY_TOP            # 38.0
CAV_BOT = -sb.H / 2 + sb.WALL      # -47.0
print(f"Cavity usable Y: {CAV_BOT:.1f} .. {CAV_TOP:.1f}  (height {CAV_TOP-CAV_BOT:.1f} mm)")

# --- Back layer: ESP + battery, both centered x=0 (same column) ---
esp = span(sb.ESP_CXY, sb.ESP_W, sb.ESP_H)
bat = span(sb.BAT_CXY, sb.BAT_W, sb.BAT_H)
report("BACK layer footprints", [
    ("esp32", sb.ESP_CXY, sb.ESP_W, sb.ESP_H),
    ("battery", sb.BAT_CXY, sb.BAT_W, sb.BAT_H),
])
print(f"  ESP top vs cavity top: {esp[3]:.2f} vs {CAV_TOP:.2f}  -> "
      f"{'OK' if esp[3] <= CAV_TOP else f'OVER by {esp[3]-CAV_TOP:.2f}'}")
print(f"  battery bottom vs cavity bottom: {bat[2]:.2f} vs {CAV_BOT:.2f}  -> "
      f"{'OK' if bat[2] >= CAV_BOT else f'OVER by {CAV_BOT-bat[2]:.2f}'}")
g = gap_y(esp, bat)
print(f"  ESP<->battery gap (no clear): {g:.2f} mm  "
      f"(need {2*CLEAR+RIB:.2f} for a divider, {2*CLEAR:.2f} for clearances)")
print(f"  stacked height needed: {sb.ESP_H+sb.BAT_H:.2f} vs cavity {CAV_TOP-CAV_BOT:.1f}")

# --- Front layer: TP + SD ---
tp = span(sb.TP_CXY, sb.TP_W, sb.TP_H)
sd = span(sb.SD_CXY, sb.SD_W, sb.SD_H)
report("FRONT layer footprints", [
    ("tp4056", sb.TP_CXY, sb.TP_W, sb.TP_H),
    ("sd", sb.SD_CXY, sb.SD_W, sb.SD_H),
])
gx = gap_x(tp, sd)  # tp is to the right of sd
print(f"  TP<->SD horizontal gap: {gx:.2f} mm  (need {2*CLEAR+RIB:.2f} for a divider)")

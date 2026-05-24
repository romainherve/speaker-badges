"""Speaker badge enclosure — portrait two-piece shell.

Outer: 54 x 105 x 14.5 mm. Round body bulge follows the screen. A webbing strap
threads through a slot on the top face and loops around an internal bar (no clips
or screws). USB-C exits the bottom edge, the micro SD slot the left edge, and two
tactile buttons the right edge.

The shell splits evenly at the mid-plane: the FRONT shell holds the front
layer (screen + adapter, TP4056, SD); the BACK shell holds the back layer
(ESP32, battery). No internal shelf is needed. The mid-plane split also lets
the USB-C opening and the strap slot/bar sit centered in the thickness.

Bill of materials (see component_layout.py for the in-case fit check):
  - AMOLED 1.73" round touch, glass Ø48.4 (Ø44.16 visible), 2.21 mm thick
  - AMOLED adapter board (CO5300), ~50 x 50 mm
  - ESP32-S3 N16R8 devkit, 28.2 x 64.4 x 4.8 mm (long board — drives the height)
  - LiPo 503040, 40 x 30 x 5 mm, 600 mAh
  - TP4056 + 5V boost, USB-C, 18 x 23.6 mm  (the charge port)
  - micro SD module, 17.8 x 17.9 mm
  - tactile side switch
"""

from build123d import (
    Align,
    Axis,
    Box,
    Circle,
    Compound,
    Cone,
    Cylinder,
    GeomType,
    Plane,
    Pos,
    Rectangle,
    RectangleRounded,
    Rotation,
    SlotOverall,
    chamfer,
    extrude,
    fillet,
    offset,
)

# --- Outer envelope (portrait, with body bulge around screen) ---
W = 54.0                   # base width (X); floor set by the 50 mm adapter + walls
H = 105.0                  # body height (Y); sized so the 64.4 mm ESP + battery
                           # stack fits in the cavity below the 7 mm header
HEADER_H = 7.0             # solid top strip housing the strap slot + internal bar
BULGE_DIA = 57.0           # gentle bulge (~1.5 mm proud of base) so the screen
                           # nearly fills the width — screen-forward proportion
CORNER_R = 4.0             # smoothing radius for outer silhouette
WALL = 1.8                 # thinned from 2.0 to keep adapter clearance at W=54
T_FRONT = 7.25             # even split at the mid-plane (total 14.5 mm)
T_BACK = 7.25
TOTAL_T = T_FRONT + T_BACK
CAVITY_TOP = H / 2 - HEADER_H   # cavity stops here; header above stays solid

# --- Screen (1.73" round LCD, ~48.4 mm glass OD, 44.16 mm viewable) ---
SCREEN_CUTOUT_DIA = 45.0   # covers the viewable area + small margin
SCREEN_CY = 7.0            # below lanyard, sized to fit bulge

# --- Bezel recess around screen (stepped face) ---
BEZEL_DIA = 50.0           # 2.5 mm rim around the screen cutout
BEZEL_DEPTH = 1.5          # recessed below the outer face
BEZEL_LIP_FILLET = 0.4     # soft transition at the recess entry

# --- Exterior edge fillet (rounded outer edges, mating face stays flat) ---
EDGE_FILLET = 1.5

# --- Strap mount (through-slot on the top face + SEPARATE drop-in wrap bar) ---
# The webbing drops through the slot, loops under the bar, and folds back up
# (sewn into a loop) — no clips or screws. The wrap bar is a SEPARATE part
# (wrap_bar.py — print it OR cut a Ø3 steel rod) that drops into a half-round
# cradle groove; each shell carries half the cradle, so closing the enclosure
# captures the bar. STRAP_FLOOR_Y keeps a thin floor above the cavity; the load
# runs bar -> cradle -> thick header side walls, not the floor.
STRAP_SLOT_X = 22.0        # along width, for ~20 mm webbing + threading tolerance
STRAP_SLOT_Z = 8.0         # along thickness — room for two strap passes + the bar
STRAP_FLOOR_Y = CAVITY_TOP + 1.0   # chamber floor, 1 mm above the cavity ceiling
STRAP_RIM_CHAMFER = 0.8    # ease the top-face entry edge (anti-wear)
STRAP_BAR_D = 3.0          # wrap-bar diameter (Ø3 printed bar or steel rod/pin)
STRAP_BAR_SPAN = 30.0      # cradle socket length (X); the ends (outboard of the
                           # Ø22 slot) groove ~4 mm into each header side wall
STRAP_BAR_Y = 49.3         # bar height (Y), suspended in the slot chamber
BAR_CRADLE_CLEAR = 0.2     # radial clearance: Ø3 bar in a Ø3.4 socket (drop-in fit)
BAR_LEN = STRAP_BAR_SPAN - 0.6     # separate bar part length (0.6 mm axial play)
STRAP_HEADER_W = 36.0      # the solid header is only this central block (carries the
                           # strap mount); top corners stay open so all 4 bosses match

# --- Closure: M2 countersunk (90° flat) head screw + M2 brass heat-set insert.
#     Lid (front): Ø2.4 clearance through-hole + Ø4.4 × 90° countersink so the
#       Ø3.8 flat head seats flush on the conical seat (self-centering; m2_screw.py).
#       Use an M2 × 10 mm screw (length includes the flush head).
#     Body (back): Ø3.2 blind hole for the insert (OD ~3.5, len 4.0), pressed in
#       from the seam; the screw threads into the insert's metal M2 bore. ---
SCREW_INSET = 4.0          # countersink rim (Ø4.4) sits ~1.8 mm off the edge; the
                           # Ø5.0 insert boss clears the 40 mm battery by ~0.5 mm.
                           # NB: a countersink wedges the thin corner wall outward
                           # (hoop stress) — drive to moderate torque, don't crank.
M2_CLEAR_DIA = 2.4         # M2 shaft clearance through the lid (ISO normal fit)
CSK_DIA = 4.4              # countersink rim Ø at the screen face (head Ø3.8 + margin
                           # → flush / slightly recessed flat head)
CSK_DEPTH = (CSK_DIA - M2_CLEAR_DIA) / 2   # 1.0 mm: 90° cone meets the clearance hole
INSERT_HOLE_DIA = 3.2      # melt hole for the M2 heat-set insert (insert OD ~3.5)
INSERT_HOLE_DEPTH = 5.0    # blind (stops ~0.45 mm short of the outer wall); insert is
                           # 4.0 mm, the rest is shaft clearance
INSERT_LEADIN_DIA = 3.8    # shallow lead-in counterbore so the insert starts square
INSERT_LEADIN_DEPTH = 0.6
BOSS_OD = 5.0              # ≥0.9 mm wall around the insert; merges into the perimeter wall

# Edge ports/buttons are given in GLOBAL z (0 = front face); they straddle the
# mid-plane seam so each shell cuts its own portion. Back-shell-native z is
# TOTAL_T - global z.
USB_GZ = TOTAL_T / 2       # USB-C centered in the thickness
USB_W = 11.0               # opening width (along X)
USB_H = 6.5                # opening height (along Z) — clears the plug overmold
USB_CX = 1.0               # USB-C is left-offset on the TP4056 board (per datasheet),
                           # not centered — opening tracks the connector, not TP_CXY[0]

SD_GZ = 5.0                # SD card-slot height (SD module seats near the front)
SD_CY = -32.0              # aligned to the SD module center (SD_CXY[1])
SD_SLOT_W = 13.0           # along Y (card width)
SD_SLOT_H = 3.0            # along Z

# --- Buttons: two recessed vertical pills on the right edge (dYdX-style) ---
BTN_GZ = TOTAL_T / 2       # centered in the thickness
BTN_LEN = 9.0              # pill length (along Y)
BTN_WID = 4.0              # pill width (along Z)
BTN_CHAN_DEPTH = 0.8       # recessed channel depth in the side wall
BTN1_CY = -15.0
BTN2_CY = -26.0

# --- Internal retention (printed pockets/ribs; screen on a ledge + foam) ---
RIB_T = 1.6                # pocket / rib wall thickness
FIT_CLEAR = 0.5            # clearance around each module
POCKET_GAP = 0.8           # stop pocket walls short of the seam so the front and
                           # back shells' walls never butt together at the mid-plane
FRONT_POCKET_TOP = T_FRONT - POCKET_GAP
BACK_POCKET_TOP = T_BACK - POCKET_GAP

GLASS_DIA = 48.4
GLASS_RING_ID = GLASS_DIA + 0.8         # locating-ring inner diameter
GLASS_RING_H = T_FRONT - WALL - POCKET_GAP   # ring stays short of the seam

# Module footprints (X, Y) and pocket centers (shared by both shells in XY)
ESP_W, ESP_H, ESP_CXY = 28.2, 64.4, (0.0, 12.8)      # back layer; top registers on header ceiling (4.8 mm thick)
BAT_W, BAT_H, BAT_CXY = 40.0, 30.0, (0.0, -35.7)     # back layer; bottom rests on perimeter wall
TP_W, TP_H, TP_CXY = 18.0, 23.6, (4.0, -35.0)        # front layer; rests against SD's divider wall
SD_W, SD_H, SD_CXY = 17.8, 17.9, (-15.8, -32.0)      # front layer; -x registers on left perimeter


def _outer_sketch():
    """Body silhouette: rounded base rectangle unioned with the screen bulge."""
    base = Rectangle(W, H)
    bulge = Pos(0, SCREEN_CY) * Circle(BULGE_DIA / 2)
    return fillet((base + bulge).vertices(), radius=CORNER_R)


def _cavity_sketch():
    """Interior cavity: inset silhouette. The solid header is only a CENTRAL block
    (STRAP_HEADER_W wide) that carries the strap mount; the top corners stay open
    so all four screw bosses stand in the cavity alike."""
    cav = offset(_outer_sketch(), -WALL)
    remove = Pos(0, CAVITY_TOP + H / 2) * Rectangle(STRAP_HEADER_W, H)
    return cav - remove


def _corners():
    for sx in (-1, 1):
        for sy in (-1, 1):
            yield sx * (W / 2 - SCREW_INSET), sy * (H / 2 - SCREW_INSET)


def _walls(w, h, center, z0, z1, sides, t=RIB_T, clear=FIT_CLEAR):
    """Pocket wall segments around a w*h footprint; `sides` picks which to add."""
    cx, cy = center
    iw, ih = w + 2 * clear, h + 2 * clear
    mid, dz = (z0 + z1) / 2, z1 - z0
    segs = []
    if "+x" in sides:
        segs.append(Pos(cx + iw / 2 + t / 2, cy, mid) * Box(t, ih + 2 * t, dz))
    if "-x" in sides:
        segs.append(Pos(cx - iw / 2 - t / 2, cy, mid) * Box(t, ih + 2 * t, dz))
    if "+y" in sides:
        segs.append(Pos(cx, cy + ih / 2 + t / 2, mid) * Box(iw + 2 * t, t, dz))
    if "-y" in sides:
        segs.append(Pos(cx, cy - ih / 2 - t / 2, mid) * Box(iw + 2 * t, t, dz))
    out = segs[0]
    for s in segs[1:]:
        out += s
    return out


def _glass_ring():
    """Locating ring on the front-shell inner face that centers the AMOLED glass."""
    outer = Pos(0, SCREEN_CY, WALL) * extrude(Circle(GLASS_RING_ID / 2 + RIB_T), GLASS_RING_H)
    inner = Pos(0, SCREEN_CY, WALL) * extrude(Circle(GLASS_RING_ID / 2), GLASS_RING_H + 0.02)
    return outer - inner


def _usb_cut(z):
    """USB-C opening through the bottom edge, centered at local z."""
    return Pos(USB_CX, -H / 2, z) * extrude(
        Plane.XZ * RectangleRounded(USB_W, USB_H, 1.0), WALL * 2, both=True
    )


def _sd_cut(z):
    """micro SD slot through the left edge, centered at local z."""
    return Pos(-W / 2, SD_CY, z) * extrude(
        Plane.YZ * RectangleRounded(SD_SLOT_W, SD_SLOT_H, 0.4), WALL * 2, both=True
    )


def _button_cuts(z):
    """Two pill buttons + their recessed channel on the right edge, centered at local z."""
    btn_mid = (BTN1_CY + BTN2_CY) / 2
    chan_len = abs(BTN1_CY - BTN2_CY) + BTN_LEN + 3.0
    cut = Pos(W / 2, btn_mid, z) * extrude(
        Plane.YZ * RectangleRounded(chan_len, BTN_WID + 4.0, 2.0), -BTN_CHAN_DEPTH
    )
    for cy in (BTN1_CY, BTN2_CY):
        cut += Pos(W / 2, cy, z) * extrude(
            Plane.YZ * SlotOverall(BTN_LEN, BTN_WID), WALL * 1.5, both=True
        )
    return cut


def _shell_body(thickness):
    """Outer block with rounded exterior edge and a header-clipped cavity."""
    solid = extrude(_outer_sketch(), thickness)
    solid = fillet(solid.edges().group_by(Axis.Z)[0], radius=EDGE_FILLET)
    cavity = Pos(0, 0, WALL) * extrude(_cavity_sketch(), thickness - WALL + 0.01)
    return solid - cavity


def _add_strap_mount(solid, t):
    """Cut the top-face strap slot and the wrap-bar cradle, for a shell whose seam
    is at z=t. Slot and cradle are symmetric about the seam, so identical local
    coords serve both shells (the back is mirrored later). The wrap bar itself is a
    SEPARATE drop-in part (wrap_bar.py) — not split between the halves."""
    top = H / 2
    slot = Pos(0, (STRAP_FLOOR_Y + top + 1) / 2, t) * Box(
        STRAP_SLOT_X, (top + 1) - STRAP_FLOOR_Y, STRAP_SLOT_Z
    )
    slot = fillet(slot.edges().filter_by(Axis.Y), radius=3.0)   # rounded slot section
    solid -= slot

    # Ease the slot entry on the top face — the edge the strap folds over.
    rim = (
        solid.edges()
        .group_by(Axis.Y)[-1]                       # top face (y = H/2)
        .filter_by_position(Axis.X, -12, 12)        # the slot, not the outer
        .filter_by_position(Axis.Z, 2.5, t + 0.5)   # top-face perimeter
    )
    if rim:
        solid = chamfer(rim, length=STRAP_RIM_CHAMFER)

    # Wrap-bar cradle: a half-round groove along X at the seam. The separate bar
    # drops into this shell's half-trough; the other shell caps it into a full
    # socket. Cutting a full cylinder centered on the seam leaves each shell its
    # own half automatically. Only the ends (outboard of the open slot) have
    # header material to groove — the central span stays clear for the strap.
    cradle = Pos(0, STRAP_BAR_Y, t) * Rotation(0, 90, 0) * Cylinder(
        STRAP_BAR_D / 2 + BAR_CRADLE_CLEAR, STRAP_BAR_SPAN
    )
    return solid - cradle


def front_shell():
    """Front shell (z=0 exterior .. z=T_FRONT seam): screen + TP4056 + SD."""
    solid = _shell_body(T_FRONT)

    # Bezel recess + softened rim
    solid -= Pos(0, SCREEN_CY, 0) * extrude(Circle(BEZEL_DIA / 2), BEZEL_DEPTH)
    bezel_rim = [
        e for e in solid.edges()
        if e.geom_type == GeomType.CIRCLE and abs(e.radius - BEZEL_DIA / 2) < 0.05
    ]
    if bezel_rim:
        solid = fillet(bezel_rim, radius=BEZEL_LIP_FILLET)

    # Screen cutout + M2 clearance through-holes & 90° head countersinks
    solid -= Pos(0, SCREEN_CY, 0) * extrude(Circle(SCREEN_CUTOUT_DIA / 2), T_FRONT)
    for x, y in _corners():
        solid -= Pos(x, y, 0) * extrude(Circle(M2_CLEAR_DIA / 2), T_FRONT)
        # countersink: cone wide (Ø4.4) at the screen face, narrowing to the
        # clearance hole at CSK_DEPTH — a flush conical seat for the flat head.
        solid -= Pos(x, y, 0) * Cone(
            CSK_DIA / 2, M2_CLEAR_DIA / 2, CSK_DEPTH,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )

    # Screen locating ring + front-layer module pockets (walls stop short of seam)
    solid += _glass_ring()
    solid += _walls(TP_W, TP_H, TP_CXY, WALL, FRONT_POCKET_TOP, ["+x", "+y"])         # USB exits -Y; rests on SD's +x divider
    solid += _walls(SD_W, SD_H, SD_CXY, WALL, FRONT_POCKET_TOP, ["+x", "+y", "-y"])  # +x is the shared divider; card exits -X (perimeter)

    # Edge ports / buttons (this shell's portion; local z = global z)
    solid -= _usb_cut(USB_GZ)
    solid -= _sd_cut(SD_GZ)
    solid -= _button_cuts(BTN_GZ)

    # Top-face strap slot + wrap-bar cradle
    solid = _add_strap_mount(solid, T_FRONT)

    return solid


def back_shell():
    """Back shell (z=0 exterior .. z=T_BACK seam): ESP32 + battery."""
    solid = _shell_body(T_BACK)

    cavity_depth = T_BACK - WALL
    for x, y in _corners():
        # Boss + blind hole for an M2 heat-set insert, pressed in from the seam.
        solid += Pos(x, y, WALL) * extrude(Circle(BOSS_OD / 2), cavity_depth)
        solid -= Pos(x, y, T_BACK - INSERT_HOLE_DEPTH) * extrude(
            Circle(INSERT_HOLE_DIA / 2), INSERT_HOLE_DEPTH + 0.01
        )
        solid -= Pos(x, y, T_BACK - INSERT_LEADIN_DEPTH) * extrude(
            Circle(INSERT_LEADIN_DIA / 2), INSERT_LEADIN_DEPTH + 0.01
        )

    # Back-layer module pockets (walls stop short of seam). ESP and battery
    # face each other across a clear gap with no divider — the gap doubles as
    # the JST-lead route. ESP top registers on the header ceiling; the battery
    # bottom rests on the perimeter wall.
    solid += _walls(ESP_W, ESP_H, ESP_CXY, WALL, BACK_POCKET_TOP, ["+x", "-x"])

    # Battery side ribs (+x / -x). Built explicitly rather than via _walls, and
    # stopped ~4 mm ABOVE the bottom insert bosses so the ribs don't run down
    # alongside the inserts (per the design review) — the bosses stand free for
    # clean heat-set access. The rib backs the upper ~2/3 of the battery's sides;
    # the bottom corners are located by the bosses + the perimeter wall. (Free rib
    # ends just add footprint loops to the floor face — verified NOT through-holes.)
    rib_x = BAT_W / 2 + FIT_CLEAR + RIB_T / 2
    rib_top = BAT_CXY[1] + BAT_H / 2 + FIT_CLEAR + RIB_T          # +y end (matches _walls)
    rib_bot = -(H / 2 - SCREW_INSET) + BOSS_OD / 2 + 4.0          # ~4 mm above the bosses
    for sx in (-1, 1):
        solid += Pos(sx * rib_x, (rib_top + rib_bot) / 2, (WALL + BACK_POCKET_TOP) / 2) * Box(
            RIB_T, rib_top - rib_bot, BACK_POCKET_TOP - WALL
        )

    # Edge ports / buttons (back-shell portion; native z = TOTAL_T - global)
    solid -= _usb_cut(TOTAL_T - USB_GZ)
    solid -= _sd_cut(TOTAL_T - SD_GZ)
    solid -= _button_cuts(TOTAL_T - BTN_GZ)

    # Top-face strap slot + wrap-bar cradle
    solid = _add_strap_mount(solid, T_BACK)

    return solid


def gen_step():
    front = front_shell()
    front.label = "front_shell"

    back = back_shell()
    back = Pos(BULGE_DIA + 8, 0, 0) * back
    back.label = "back_shell"

    return Compound(label="speaker_badge", children=[front, back])


if __name__ == "__main__":
    from build123d import export_step
    export_step(gen_step(), "speaker_badge.step")
    print("wrote speaker_badge.step")

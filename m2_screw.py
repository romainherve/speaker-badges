"""Simplified M2 countersunk (flat) head screw (90°, ISO 10642 / DIN 965) for
visualization and for fit-checking the lid countersink + insert engagement. This
is bought hardware (steel), NOT printed — modeled as a plain shank + 90° conical
head + hex socket, no cosmetic threads. Pair with an M2 brass heat-set insert in
the back-shell boss.

Reference dims (M2 countersunk, 90°): head Ø3.8, head height ~0.9, hex socket.
Use an M2 × 10 mm screw (length includes the flush head): ~5 mm through the lid,
~3 mm engages the insert. A countersunk head's length is measured head-top to
tip, so it needs to be longer than the cap-head version for the same grip.
"""

from build123d import Align, Cone, Cylinder, Pos, RegularPolygon, extrude

SHANK_DIA = 2.0                       # M2 nominal
HEAD_DIA = 3.8                        # flat head Ø (top of the cone)
HEAD_H = (HEAD_DIA - SHANK_DIA) / 2   # 0.9 mm — 90° cone from shaft to head Ø
SHANK_LEN = 9.1                       # so head-top..tip = SHANK_LEN + HEAD_H = 10 (M2×10)
HEX_AF = 1.3                          # hex socket across-flats (M2 countersunk)
HEX_DEPTH = 0.6

_MIN = (Align.CENTER, Align.CENTER, Align.MIN)


def gen_step():
    shank = Cylinder(SHANK_DIA / 2, SHANK_LEN, align=_MIN)
    # 90° conical head: Ø2.0 at the shaft (bottom) flaring to Ø3.8 at the top.
    head = Pos(0, 0, SHANK_LEN) * Cone(SHANK_DIA / 2, HEAD_DIA / 2, HEAD_H, align=_MIN)
    screw = shank + head
    # Hex socket sunk into the flat top (circumradius from across-flats).
    hex_r = HEX_AF / 3 ** 0.5
    socket = Pos(0, 0, SHANK_LEN + HEAD_H) * extrude(RegularPolygon(hex_r, 6), -HEX_DEPTH)
    return screw - socket


if __name__ == "__main__":
    from build123d import export_step
    export_step(gen_step(), "m2_screw.step")
    print("wrote m2_screw.step")

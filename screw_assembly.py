"""Assembled enclosure with the four M2 countersunk screws + heat-set inserts and
the drop-in wrap bar, to check the lid countersink, shaft/insert engagement, and
the bar seated in its cradle."""

from build123d import Compound, Plane, Pos, Rotation, mirror

import insert as ins
import m2_screw as ps
import speaker_badge as sb
import wrap_bar as wb

L_TOT = ps.SHANK_LEN + ps.HEAD_H
# Seat the countersunk head on the conical seat: the Ø3.8 head meets the Ø4.4
# countersink where their diameters match, recessing the head top by
# (CSK_DIA - HEAD_DIA)/2 below the screen face.
SEAT = (sb.CSK_DIA - ps.HEAD_DIA) / 2


def _corners():
    for sx in (-1, 1):
        for sy in (-1, 1):
            yield sx * (sb.W / 2 - sb.SCREW_INSET), sy * (sb.H / 2 - sb.SCREW_INSET)


def _screws():
    screw = ps.gen_step()
    # flip head-down, head recessed on the counterbore floor, shaft into +z
    return [Pos(cx, cy, SEAT) * Pos(0, 0, L_TOT) * Rotation(180, 0, 0) * screw
            for cx, cy in _corners()]


def _inserts():
    insert = ins.gen_step()
    # seated in each boss, entering at the seam (z=7.25), running into the body
    return [Pos(cx, cy, sb.T_FRONT) * insert for cx, cy in _corners()]


def gen_step():
    front = sb.front_shell()
    front.label = "front_shell"
    back = Pos(0, 0, sb.TOTAL_T) * mirror(sb.back_shell(), about=Plane.XY)
    back.label = "back_shell"
    children = [front, back]
    for i, s in enumerate(_screws()):
        s.label = f"screw_{i}"
        children.append(s)
    for i, s in enumerate(_inserts()):
        s.label = f"insert_{i}"
        children.append(s)
    # Drop-in wrap bar, seated in the cradle: axis along X, centered on the seam.
    bar = (Pos(0, sb.STRAP_BAR_Y, sb.TOTAL_T / 2) * Rotation(0, 90, 0)
           * Pos(0, 0, -wb.LEN / 2) * wb.gen_step())
    bar.label = "wrap_bar"
    children.append(bar)
    return Compound(label="screw_assembly", children=children)


if __name__ == "__main__":
    from build123d import export_step
    export_step(gen_step(), "screw_assembly.step")
    print("wrote screw_assembly.step")

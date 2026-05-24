"""Separate drop-in strap wrap bar.

It sits in the half-round cradle grooves at the top of the enclosure and is
captured when the two shells close — it is NOT split between the halves. Two ways
to make it, same nominal Ø3 × ~29.4 mm:

  1. Print this part (PLA/PETG), bar axis flat on the bed.
  2. Cut a Ø3 mm steel rod / dowel pin to BAR_LEN and drop it in (stronger; best
     if the strap will see real load).

The socket is Ø3.4 (0.2 mm radial clearance) and ~0.6 mm longer than the bar, so
it drops in freely and the closed shells trap it. The small end chamfers ease
insertion / stand in for a deburred rod end.
"""

from build123d import Align, Cylinder, GeomType, chamfer

import speaker_badge as sb

DIA = sb.STRAP_BAR_D     # 3.0 mm — matches a Ø3 rod
LEN = sb.BAR_LEN         # fits the cradle socket with a little axial play
END_CHAMFER = 0.3


def gen_step():
    bar = Cylinder(DIA / 2, LEN, align=(Align.CENTER, Align.CENTER, Align.MIN))
    ends = bar.edges().filter_by(GeomType.CIRCLE)
    return chamfer(ends, length=END_CHAMFER)


if __name__ == "__main__":
    from build123d import export_step
    export_step(gen_step(), "wrap_bar.step")
    print("wrote wrap_bar.step")

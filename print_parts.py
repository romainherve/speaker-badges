"""Export STL files for the 3D-PRINTED parts, ready to slice (Bambu A1).

Printed parts: front_shell, back_shell, and (optionally) wrap_bar.
NOT printed: the M2 socket-screws and the brass heat-set inserts (bought hardware).

Each shell is exported in its native pose, which is also the recommended print
orientation: OUTER FACE DOWN, cavity opening up. In that pose the USB / SD /
button cutouts and the strap slot are all open notches at the seam (top), so the
print needs NO supports. The wrap bar is laid flat (print with a brim, or just
use a Ø3 mm steel rod instead).
"""

import os

from build123d import Rotation, export_stl

import speaker_badge as sb
import wrap_bar as wb

# Fine tessellation so the round bulge / fillets print smooth.
TOL, ANG = 0.02, 0.15


def gen():
    os.makedirs("print", exist_ok=True)
    parts = {
        "front_shell": sb.front_shell(),                 # screen face down, cavity up
        "back_shell": sb.back_shell(),                   # back face down, cavity up
        "wrap_bar": Rotation(0, 90, 0) * wb.gen_step(),  # laid flat on the bed
    }
    for name, part in parts.items():
        path = f"print/{name}.stl"
        export_stl(part, path, tolerance=TOL, angular_tolerance=ANG)
        print(f"wrote {path}")


if __name__ == "__main__":
    gen()

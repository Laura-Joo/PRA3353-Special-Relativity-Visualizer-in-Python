"""

THIS FILE IS EVIL AND AI GENERATED, DONT USE IT IN THE END PROJECT


Nats super awesome Minkowski diagram in shifter.

mac run instructions:

python3 -m venv shifterenv
source shifterenv/bin/activate
pip install matplotlib numpy
python3 minkowski_lightcone.py

once you are done:
deactivate
    
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


def k_factor(beta):
    return np.sqrt((1.0 - beta) / (1.0 + beta))


def xct_to_uv(x, ct):
    return ct + x, ct - x


def uv_to_xct(u, v):
    return (u - v) / 2.0, (u + v) / 2.0


def boost_uv(u, v, beta):
    k = k_factor(beta)
    return k * u, v / k


def velocity_of_lab(endpt_xct):
    x, ct = endpt_xct
    if abs(ct) < 1e-9:
        return np.inf
    return x / ct


events = {
    "A": np.array([1.5, 7.0]),
    "B": np.array([5.0, 7.0]),
}
COLOR_A, COLOR_B = "#378ADD", "#D4537E"
beta = 0.0

U_MAX, V_MAX = 10.0, 10.0

fig, ax = plt.subplots(figsize=(8.5, 8.5))
plt.subplots_adjust(left=0.10, right=0.97, top=0.95, bottom=0.22)

ax.set_xlim(0, U_MAX)
ax.set_ylim(0, V_MAX)
ax.set_aspect("equal")
ax.set_xlabel("u = ct + x   (right-moving light ray)")
ax.set_ylabel("v = ct − x   (left-moving light ray)")
ax.grid(True, alpha=0.2)
title = ax.set_title("Light cone coordinates — β = 0.00, k = 1.000")

def clip_uv(p0, p1):
    tmin, tmax = 0.0, 1.0
    for axis, lo, hi in ((0, 0.0, U_MAX), (1, 0.0, V_MAX)):
        a, b = p0[axis], p1[axis]
        d = b - a
        if abs(d) < 1e-12:
            if a < lo - 1e-9 or a > hi + 1e-9:
                return None
            continue
        t1, t2 = (lo - a) / d, (hi - a) / d
        tmin = max(tmin, min(t1, t2))
        tmax = min(tmax, max(t1, t2))
        if tmin > tmax:
            return None
    return p0 + tmin * (p1 - p0), p0 + tmax * (p1 - p0)


def set_line(artist, p0, p1):
    seg = clip_uv(p0, p1)
    if seg is None:
        artist.set_data([], [])
        return None
    qa, qb = seg
    artist.set_data([qa[0], qb[0]], [qa[1], qb[1]])
    return qb

# worldlines + endpoint markers

(line_A,) = ax.plot([], [], "-", color=COLOR_A, lw=2.8, label="Worldline A")
(line_B,) = ax.plot([], [], "-", color=COLOR_B, lw=2.8, label="Worldline B")
endpt_A = ax.plot([], [], "o", color=COLOR_A, ms=11, mec="white", mew=1.5)[0]
endpt_B = ax.plot([], [], "o", color=COLOR_B, ms=11, mec="white", mew=1.5)[0]

(rest_axis,) = ax.plot([], [], "-", color="#0F6E56", lw=1.3, alpha=0.8,
                       label="ct' axis  (x' = 0)")

N_LINES = int(max(U_MAX, V_MAX)) + 2
equal_ct_artists = [ax.plot([], [], "--", color="#BD7A17", lw=0.9, alpha=0.5)[0]
                    for _ in range(N_LINES)]
equal_x_artists = [ax.plot([], [], ":", color="#0F6E56", lw=0.9, alpha=0.45)[0]
                   for _ in range(N_LINES)]

info_text = ax.text(
    0.02, 0.98, "",
    transform=ax.transAxes, va="top", ha="left",
    fontsize=9, family="monospace",
    bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="lightgray", alpha=0.9),
)

ax.legend(loc="lower right", fontsize=9, framealpha=0.9)

# redraw

def frame_endpoints():
    out = {}
    for k, (x, ct) in events.items():
        u, v = xct_to_uv(x, ct)
        u_, v_ = boost_uv(u, v, beta)
        out[k] = np.array([u_, v_])
    return out


def redraw():
    e = frame_endpoints()

    origin = np.array([0.0, 0.0])
    set_line(line_A, origin, e["A"])
    set_line(line_B, origin, e["B"])

    def clamp(p):
        return (max(0, min(U_MAX, p[0])), max(0, min(V_MAX, p[1])))
    pA, pB = clamp(e["A"]), clamp(e["B"])
    endpt_A.set_data([pA[0]], [pA[1]])
    endpt_B.set_data([pB[0]], [pB[1]])

    # rest-observer line (u = v)
    d = min(U_MAX, V_MAX)
    set_line(rest_axis, np.array([0.0, 0.0]), np.array([d, d]))

    # equal-ct' lines u + v = 2*n for n = 1..
    for n, art in enumerate(equal_ct_artists, start=1):
        two_t = 2 * n
        set_line(art, np.array([0.0, float(two_t)]), np.array([float(two_t), 0.0]))

    # equal-x' lines u − v = 2*n (parametrize by v: u = v + 2n)
    for n, art in enumerate(equal_x_artists, start=1):
        two_x = 2 * n
        v_lo = max(0.0, -two_x)
        v_hi = V_MAX
        set_line(art,
                 np.array([v_lo + two_x, v_lo]),
                 np.array([v_hi + two_x, v_hi]))

    k = k_factor(beta)
    g = 1.0 / np.sqrt(1 - beta * beta)

    def describe(name, uv):
        u, v = float(uv[0]), float(uv[1])
        x, ct = uv_to_xct(u, v)
        vel = x / ct if abs(ct) > 1e-9 else np.inf
        timelike = u > 0 and v > 0
        if not np.isfinite(vel):
            v_str = "— (instant)"
        elif abs(vel) >= 1:
            v_str = f"{vel:+.3f} c (spacelike!)"
        else:
            v_str = f"{vel:+.3f} c"
        tau = np.sqrt(u * v) if timelike else 0.0
        tau_str = f"{tau:.3f}" if timelike else "—"
        return (f"{name}: v = {v_str:>20s}   Δτ = √(u·v) = {tau_str:>6s}\n"
                f"    (x, ct) = ({x:+.2f}, {ct:+.2f})   (u, v) = ({u:+.2f}, {v:+.2f})")

    info_text.set_text(
        f"frame β = {beta:+.2f} c    k = {k:.3f}    γ = {g:.3f}\n"
        + describe("A", e["A"]) + "\n"
        + describe("B", e["B"])
    )
    title.set_text(f"Light-cone coordinates — β = {beta:+.2f}, k = {k:.3f}")
    fig.canvas.draw_idle()



# slider

ax_slider = plt.axes([0.15, 0.10, 0.70, 0.03])
beta_slider = Slider(ax_slider, "β (v/c)", -0.95, 0.95, valinit=0.0, valstep=0.01)


def on_beta(val):
    global beta
    beta = float(val)
    redraw()


beta_slider.on_changed(on_beta)


# buttons

def make_btn(left, label):
    return Button(plt.axes([left, 0.03, 0.18, 0.05]), label)


btn_A = make_btn(0.08, "Rest frame A")
btn_B = make_btn(0.28, "Rest frame B")
btn_lab = make_btn(0.48, "Lab frame")
btn_anim = make_btn(0.68, "Sweep β ↔")


def goto_rest_of(endpt):
    v = velocity_of_lab(endpt)
    if np.isfinite(v) and abs(v) < 0.95:
        beta_slider.set_val(round(v, 2))


btn_A.on_clicked(lambda _e: goto_rest_of(events["A"]))
btn_B.on_clicked(lambda _e: goto_rest_of(events["B"]))
btn_lab.on_clicked(lambda _e: beta_slider.set_val(0.0))


_anim = {"running": False, "timer": None, "t": 0.0}


def toggle_anim(_e):
    if _anim["running"]:
        _anim["timer"].stop()
        _anim["running"] = False
        return
    _anim["t"] = 0.0

    def tick():
        _anim["t"] += 0.05
        beta_slider.set_val(round(0.85 * np.sin(_anim["t"]), 2))

    timer = fig.canvas.new_timer(interval=50)
    timer.add_callback(tick)
    timer.start()
    _anim["timer"] = timer
    _anim["running"] = True


btn_anim.on_clicked(toggle_anim)

# drag endpoints 

_drag = {"key": None}
PICK_RADIUS = 0.5


def on_press(ev):
    if ev.inaxes is not ax or ev.xdata is None:
        return
    e = frame_endpoints()
    best, bd = None, PICK_RADIUS ** 2
    for k, p in e.items():
        d = (p[0] - ev.xdata) ** 2 + (p[1] - ev.ydata) ** 2
        if d < bd:
            bd, best = d, k
    _drag["key"] = best


def on_release(_ev):
    _drag["key"] = None


def on_motion(ev):
    if _drag["key"] is None or ev.inaxes is not ax or ev.xdata is None:
        return
    u = max(0.05, min(U_MAX, ev.xdata))
    v = max(0.05, min(V_MAX, ev.ydata))
    k = k_factor(beta)
    lab_u = u / k
    lab_v = v * k
    x, ct = uv_to_xct(lab_u, lab_v)
    events[_drag["key"]] = np.array([x, ct])
    redraw()


fig.canvas.mpl_connect("button_press_event", on_press)
fig.canvas.mpl_connect("button_release_event", on_release)
fig.canvas.mpl_connect("motion_notify_event", on_motion)


redraw()
plt.show()

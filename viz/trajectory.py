"""Render the 7-day valence/arousal trajectory as an inline SVG line chart.

Two solid polylines (history) + dashed tails (forecast). Both series share the
[-1, 1] -> y mapping so they're directly comparable. The forecast segment is
deliberately dashed and labelled so it never reads as a real model output.
"""
import config

_W, _H = 300, 150
_X0, _X1 = 24, 240      # history x-range
_XF = 276               # forecast x
_YTOP, _YBOT = 30, 110  # value band


def _y(val: float) -> float:
    # val in [-1, 1] -> y (top = +1)
    t = (val + 1) / 2
    return _YBOT - t * (_YBOT - _YTOP)


def _xs(n: int):
    if n == 1:
        return [_X0]
    step = (_X1 - _X0) / (n - 1)
    return [_X0 + i * step for i in range(n)]


def _poly(xs, ys):
    return " ".join(f"{x:.0f},{y:.0f}" for x, y in zip(xs, ys))


def svg_trajectory(valence, arousal, forecast=None) -> str:
    """valence, arousal: equal-length lists in [-1,1]. forecast: (vf, af) or None."""
    P = config.PALETTE
    xs = _xs(len(valence))
    vy = [_y(v) for v in valence]
    ay = [_y(a) for a in arousal]

    fdiv = fseg = ""
    if forecast is not None:
        vf, af = forecast
        fyv, fya = _y(vf), _y(af)
        fdiv = (
            f'<line x1="258" y1="18" x2="258" y2="118" stroke="{P["sky"]}" '
            f'stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>'
            f'<text x="261" y="26" font-size="9" fill="{P["sky"]}">prediksi</text>'
        )
        fseg = (
            f'<polyline points="{xs[-1]:.0f},{vy[-1]:.0f} {_XF},{fyv:.0f}" fill="none" '
            f'stroke="{config.VALENCE_COLOR}" stroke-width="2.5" stroke-dasharray="4 4"/>'
            f'<circle cx="{_XF}" cy="{fyv:.0f}" r="4" fill="#fff" stroke="{config.VALENCE_COLOR}" stroke-width="2"/>'
            f'<polyline points="{xs[-1]:.0f},{ay[-1]:.0f} {_XF},{fya:.0f}" fill="none" '
            f'stroke="{config.AROUSAL_COLOR}" stroke-width="2.5" stroke-dasharray="4 4"/>'
            f'<circle cx="{_XF}" cy="{fya:.0f}" r="4" fill="#fff" stroke="{config.AROUSAL_COLOR}" stroke-width="2"/>'
            f'<text x="246" y="130" text-anchor="middle" font-size="9" fill="{P["rosewood"]}">'
            f'[v: {config.fmt_v(vf)}, a: {config.fmt_a(af)}]</text>'
        )

    grid = "".join(
        f'<line x1="18" y1="{yy}" x2="282" y2="{yy}" stroke="{P["midnight"]}" '
        f'stroke-width="0.5" opacity="0.08"/>' for yy in (30, 65, 100)
    )
    return f'''<svg viewBox="0 0 {_W} {_H}" width="100%" xmlns="http://www.w3.org/2000/svg">
{grid}
{fdiv}
  <polyline points="{_poly(xs, vy)}" fill="none" stroke="{config.VALENCE_COLOR}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  <polyline points="{_poly(xs, ay)}" fill="none" stroke="{config.AROUSAL_COLOR}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
{fseg}
</svg>'''
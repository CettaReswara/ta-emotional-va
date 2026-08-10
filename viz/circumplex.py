"""Render the Russell circumplex as an inline SVG string.

Built in a fixed 240x240 coordinate space (matches the approved mockup) and
scaled via the width attribute. A (valence, arousal) point in [-1, 1] maps to
pixel coordinates; quadrants carry faint palette washes.
"""
import config

_CX = _CY = 120
_R = 100
_F = 0.82  # keep the plotted point inside the ring


def _xy(v: float, a: float):
    return _CX + v * _R * _F, _CY - a * _R * _F


def svg_circumplex(point=None, width: int = 240) -> str:
    P = config.PALETTE
    dot = ""
    if point is not None:
        v, a = point
        px, py = _xy(v, a)
        c = P["rosewood"]
        dot = (
            f'<line x1="{px:.0f}" y1="{py:.0f}" x2="{px:.0f}" y2="{_CY}" '
            f'stroke="{c}" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>'
            f'<line x1="{px:.0f}" y1="{py:.0f}" x2="{_CX}" y2="{py:.0f}" '
            f'stroke="{c}" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>'
            f'<circle cx="{px:.0f}" cy="{py:.0f}" r="7" fill="{c}" '
            f'stroke="#fff" stroke-width="2"/>'
        )
    return f'''<svg viewBox="0 0 240 240" width="{width}" xmlns="http://www.w3.org/2000/svg">
  <path d="M120,120 L120,20 A100,100 0 0 1 220,120 Z" fill="{P['blush']}" opacity="0.32"/>
  <path d="M120,120 L220,120 A100,100 0 0 1 120,220 Z" fill="{P['sage']}" opacity="0.28"/>
  <path d="M120,120 L120,220 A100,100 0 0 1 20,120 Z" fill="{P['sky']}" opacity="0.32"/>
  <path d="M120,120 L20,120 A100,100 0 0 1 120,20 Z" fill="{P['rosewood']}" opacity="0.20"/>
  <circle cx="120" cy="120" r="100" fill="none" stroke="{P['midnight']}" stroke-width="1" opacity="0.32"/>
  <line x1="20" y1="120" x2="220" y2="120" stroke="{P['midnight']}" stroke-width="1" opacity="0.26"/>
  <line x1="120" y1="20" x2="120" y2="220" stroke="{P['midnight']}" stroke-width="1" opacity="0.26"/>
  <text x="178" y="62"  text-anchor="middle" font-size="10" font-weight="500" fill="{P['midnight']}">Excited</text>
  <text x="64"  y="62"  text-anchor="middle" font-size="10" font-weight="500" fill="{P['midnight']}">Tense</text>
  <text x="64"  y="184" text-anchor="middle" font-size="10" font-weight="500" fill="{P['midnight']}">Sad</text>
  <text x="178" y="184" text-anchor="middle" font-size="10" font-weight="500" fill="{P['midnight']}">Calm</text>
  <text x="223" y="116" text-anchor="end"   font-size="9" fill="{P['sky']}">+ val</text>
  <text x="17"  y="116" text-anchor="start" font-size="9" fill="{P['sky']}">&#8722; val</text>
  <text x="125" y="28"  text-anchor="start" font-size="9" fill="{P['sky']}">+ aro</text>
  <text x="125" y="214" text-anchor="start" font-size="9" fill="{P['sky']}">&#8722; aro</text>
  {dot}
</svg>'''

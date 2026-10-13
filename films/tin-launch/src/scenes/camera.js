// Camera over the paper sheet. Framings from docs/SHOTLIST.md; every UI framing keeps the UI's top edge at or
// below stage y 360 (centre y = 180 / z + top) so the caption band stays paper.
(function () {
  const { T, BAR, BEAT, keys, drift, camTransform, css } = F;
  const DROP = [240, 24];           // the drop pull-back: decisive (≈53% of the move in 0.1 s), 3% overshoot
  let K = null, world;

  // UI framings keep the UI's top edge at stage y 392, leaving the caption band (96–340) on paper.
  const top360 = (z, top = 0) => 148 / z + top;

  function build(w) { world = w; }

  // Framings need real control positions, so they're computed after the dashboard is measured.
  function measure() {
    const D = DashTimeline;
    const ap = D.worldRect('approve'), toc = D.worldRect('toc'), last = D.worldRect('lastRow'), logo = D.worldRect('readerLogo');
    const list = D.worldRect('decList'), card = D.worldRect('decCard');
    const dash = D.windowRect();
    // Reader: from the TOC to Approve, down to the last plan row, all in frame below the caption band.
    // Bar 7 shows Tin's reader whole, logo to Approve; bar 8 pushes in to the plan and Approve.
    const oL = logo.x - 36, rL = toc.x - 40, rR = ap.x + ap.w + 40, rB = last.y + last.h + 40;
    const zR = Math.min(1.5, 1680 / (rR - oL), (1040 - 392) / (rB - dash.y));
    const zA = Math.min(1.5, 1680 / (rR - rL), (1040 - 392) / (rB - dash.y));
    const rCx = (oL + rR) / 2, aCx = (rL + rR) / 2;
    // Decisions: the list and the card together.
    const dL = list.x - 30, dR = card.x + card.w + 30;
    const zC = Math.min(1.45, 1680 / (dR - dL));
    const zW = 0.92;                                   // the drop: the dashboard alone, big
    const zD = 1.2;                                    // between sessions: rail + This week + running cards
    const dashCx = dash.x + dash.w / 2;
    const railCx = dash.x + (960 - 120) / zD;          // window's left edge at stage x 120
    K = {
      // Bar 7 is an arc, not a whip: x eases across a bar while the camera pulls out to z 0.8 (the agent and Tin
      // side by side) and pushes back in to the reader, which keeps screen speeds low enough for 4 blur subframes.
      x: [[0, (960 - 120) / 1.2], [T(2, 4), 579, 'base'], [T(7, 2), rCx, { dur: BAR * 0.6 }], [T(8, 2), aCx + 24, { dur: BAR * 0.95 }],
          [T(9, 1), dashCx, DROP], [T(10, 3), railCx, 'base'], [T(11, 3.5), (dL + dR) / 2, { dur: BAR * 0.45 }]],
      y: [[0, -(820 - 540) / 1.2], [T(2, 4), top360(1.45), 'base'], [T(7, 2), top360(0.8), { dur: BAR * 0.3 }], [T(7, 3.2), top360(zR), { dur: BAR * 0.32 }],
          [T(8, 2), top360(zA), { dur: BAR * 0.95 }],
          [T(9, 1), top360(zW), DROP], [T(10, 3), top360(zD), 'base'], [T(11, 3.5), top360(zC), { dur: BAR * 0.45 }]],
      lz: [[0, Math.log(1.2)], [0.001, Math.log(1.2 * 1.03), { dur: T(2, 4) }], [T(2, 4), Math.log(1.45), 'base'], [T(3, 1), Math.log(1.52), { dur: T(7, 1) - T(3, 1) }],
           [T(7, 2), Math.log(0.8), { dur: BAR * 0.3 }], [T(7, 3.2), Math.log(zR), { dur: BAR * 0.32 }], [T(8, 2), Math.log(zA), { dur: BAR * 0.95 }],
           [T(9, 1), Math.log(zW), DROP], [T(9, 2), Math.log(zW * 1.04), { dur: T(10, 3) - T(9, 2) }],
           [T(10, 3), Math.log(zD), 'base'], [T(10, 4), Math.log(zD * 1.04), { dur: T(11, 3) - T(10, 4) }],
           [T(11, 3.5), Math.log(zC), { dur: BAR * 0.45 }], [T(11, 4), Math.log(zC * 1.05), { dur: T(13, 1) - T(11, 4) }]],
    };
    Camera.framings = { zR, zA, zC, oL, rL, rR, dL, dR };
  }

  function at(t) {
    let x = keys(t, K.x), y = keys(t, K.y), z = Math.exp(keys(t, K.lz));
    // Always drifting: a few px and a few thousandths of zoom, seeded, smooth.
    x += drift(t, 11, 6) / z; y += drift(t, 12, 4) / z; z *= 1 + drift(t, 13, 0.004);
    return { x, y, z };
  }
  function toScreen(wx, wy, t) { const c = at(t); return { x: 960 + (wx - c.x) * c.z, y: 540 + (wy - c.y) * c.z, z: c.z }; }

  function update(t) {
    const c = at(t);
    css(world, { transform: camTransform(c.x, c.y, c.z) });
  }

  window.Camera = { build, measure, update, at, toScreen };
})();

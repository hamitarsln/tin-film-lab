// Wiring: build once, measure after fonts and images load, then seek(t) paints any frame from t alone.
(function () {
  const stage = document.getElementById('stage');
  const world = document.getElementById('world');
  const captions = document.getElementById('captions');
  const cursorLayer = F.el('div', 'layer', stage);
  const endLayer = F.el('div', 'layer', stage);
  const ASSETS = '../';

  F.css(stage, { transform: `scale(${(F.VW / F.SW).toFixed(6)})` });

  Terminal.build(world, captions);
  DashTimeline.build(world, ASSETS);
  Camera.build(world);
  Captions.build(captions);
  Cursor.build(cursorLayer);
  EndCard.build(endLayer, ASSETS);

  const fonts = ['300 40px FG', '400 40px FG', '500 40px FG', '500 24px SFM'].map(f => document.fonts.load(f));
  const imgs = [...document.images].map(img => (img.complete ? Promise.resolve() : img.decode().catch(() => {})));

  Promise.all([...fonts, ...imgs, document.fonts.ready]).then(() => {
    Terminal.measure();
    DashTimeline.measure();
    Camera.measure();
    Captions.measure();
    Cursor.measure();
    EndCard.measure();

    function seek(t) {
      t = Math.max(0, Math.min(t, window.CUE.length));
      Camera.update(t);
      Terminal.update(t);
      DashTimeline.update(t);
      Captions.update(t);
      Cursor.update(t);
      EndCard.update(t);
    }
    window.FILM = { duration: window.CUE.length, width: 1920, height: 1080 };
    window.seek = seek;
    seek(0);

    // Live preview in a normal browser (never in render mode): plays the film against the clock with the music.
    if (!F.RENDER) {
      const audio = new Audio('../music-cut/music.wav');
      let t0 = null;
      const start = () => { if (t0 === null) { t0 = performance.now(); audio.play().catch(() => {}); } };
      document.addEventListener('click', start);
      (function loop() {
        if (t0 !== null) seek(((performance.now() - t0) / 1000) % window.FILM.duration);
        requestAnimationFrame(loop);
      })();
    }
  });
})();

import * as THREE from 'three';

const DURATION_MS = 6600;

export function mountDecisionMesh(canvas, {reducedMotion = false, onStateChange} = {}) {
  const renderer = new THREE.WebGLRenderer({
    canvas,
    alpha: true,
    antialias: true,
    powerPreference: 'low-power',
    premultipliedAlpha: false,
    preserveDrawingBuffer: true,
  });
  renderer.setClearColor(0x000000, 0);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-5, 5, 3, -3, 0.1, 100);
  camera.position.z = 12;

  const geometry = new THREE.IcosahedronGeometry(3, 0);
  const material = new THREE.MeshStandardMaterial({
    color: 0xE34A32,
    roughness: 0.3,
    metalness: 0.6,
    flatShading: true,
  });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.scale.setScalar(0.145);
  scene.add(mesh);

  const keyLight = new THREE.DirectionalLight(0xffffff, 2.3);
  keyLight.position.set(-2, 5, 8);
  scene.add(keyLight);
  const rimLight = new THREE.DirectionalLight(0xffc7bb, 1.5);
  rimLight.position.set(6, -2, 5);
  scene.add(rimLight);
  scene.add(new THREE.AmbientLight(0xffffff, 1.2));

  let anchor = 0;
  let frameId = 0;
  let frameCount = 0;
  let startedAt = 0;
  let pausedAt = 0;
  let pausedDuration = 0;
  let finished = false;
  let inView = true;

  const debug = {
    geometry: 'IcosahedronGeometry',
    radius: 3,
    detail: 0,
    color: '#E34A32',
    roughness: 0.3,
    metalness: 0.6,
    flatShading: true,
    desktopAnchorX: 4.5,
    mobileAnchorX: 0,
    dpr: renderer.getPixelRatio(),
    frameCount: 0,
    rafActive: false,
    reducedMotion,
  };

  function resize() {
    const parent = canvas.parentElement;
    const width = Math.max(1, parent?.clientWidth || canvas.clientWidth || 1);
    const height = Math.max(1, parent?.clientHeight || canvas.clientHeight || 1);
    renderer.setSize(width, height, false);
    anchor = window.innerWidth >= 768 ? 4.5 : 0;
    debug.anchorX = anchor;
    const worldWidth = 10;
    const worldHeight = worldWidth / (width / height);
    camera.left = anchor - worldWidth / 2;
    camera.right = anchor + worldWidth / 2;
    camera.top = worldHeight / 2;
    camera.bottom = -worldHeight / 2;
    camera.position.x = anchor;
    camera.updateProjectionMatrix();
  }

  function renderFrame(progress, seconds, shouldFloat) {
    mesh.position.x = anchor;
    mesh.position.y = -1.86 + (shouldFloat ? Math.sin(seconds * 1.2) * 0.3 : 0);
    mesh.rotation.x = seconds * 0.55;
    mesh.rotation.y = seconds * 0.8;
    renderer.render(scene, camera);
    frameCount += 1;
    debug.frameCount = frameCount;
    debug.positionX = mesh.position.x;
    debug.positionY = mesh.position.y;
  }

  function stop() {
    if (frameId) cancelAnimationFrame(frameId);
    frameId = 0;
    debug.rafActive = false;
  }

  function tick(now) {
    if (!inView || document.hidden) {
      stop();
      pausedAt = now;
      return;
    }
    const elapsed = Math.max(0, now - startedAt - pausedDuration);
    const progress = Math.min(1, elapsed / DURATION_MS);
    renderFrame(progress, elapsed / 1000, progress < 1);
    if (progress < 1) {
      debug.rafActive = true;
      frameId = requestAnimationFrame(tick);
    } else {
      finished = true;
      stop();
      onStateChange?.('complete', debug);
    }
  }

  function replay() {
    stop();
    finished = false;
    pausedDuration = 0;
    pausedAt = 0;
    startedAt = performance.now();
    if (reducedMotion) {
      renderFrame(1, DURATION_MS / 1000, false);
      finished = true;
      onStateChange?.('static', debug);
      return;
    }
    debug.rafActive = true;
    frameId = requestAnimationFrame(tick);
  }

  function seek(phase) {
    stop();
    const positions = [0.29, 0.61, 1];
    const progress = positions[Math.max(0, Math.min(2, phase))];
    renderFrame(progress, progress * DURATION_MS / 1000, false);
    finished = true;
    onStateChange?.('seek', debug);
  }

  const resizeObserver = new ResizeObserver(() => {
    resize();
    if (finished || reducedMotion) renderFrame(1, DURATION_MS / 1000, false);
  });
  resizeObserver.observe(canvas.parentElement || canvas);

  const intersectionObserver = new IntersectionObserver(([entry]) => {
    inView = entry.isIntersecting;
    if (inView && !finished && !reducedMotion && !frameId) {
      const now = performance.now();
      if (pausedAt) pausedDuration += now - pausedAt;
      pausedAt = 0;
      debug.rafActive = true;
      frameId = requestAnimationFrame(tick);
    }
  }, {threshold: 0.05});
  intersectionObserver.observe(canvas);

  function handleVisibility() {
    if (document.hidden) {
      if (!finished) pausedAt = performance.now();
      stop();
    } else if (!finished && inView && !reducedMotion) {
      const now = performance.now();
      if (pausedAt) pausedDuration += now - pausedAt;
      pausedAt = 0;
      debug.rafActive = true;
      frameId = requestAnimationFrame(tick);
    }
  }
  document.addEventListener('visibilitychange', handleVisibility);

  resize();
  replay();
  onStateChange?.('ready', debug);

  return {
    debug,
    replay,
    seek,
    destroy() {
      stop();
      resizeObserver.disconnect();
      intersectionObserver.disconnect();
      document.removeEventListener('visibilitychange', handleVisibility);
      geometry.dispose();
      material.dispose();
      renderer.dispose();
    },
  };
}

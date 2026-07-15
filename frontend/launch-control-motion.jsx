import React, {useEffect, useRef, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {Badge} from '@astryxdesign/core/Badge';
import {Button} from '@astryxdesign/core/Button';
import {Card} from '@astryxdesign/core/Card';
import {ProgressBar} from '@astryxdesign/core/ProgressBar';
import {StatusDot} from '@astryxdesign/core/StatusDot';
import {Theme} from '@astryxdesign/core/theme';
import {launchControlTheme} from './generated/launch-control.js';
import '@astryxdesign/core/reset.css';
import '@astryxdesign/core/astryx.css';
import './generated/launch-control-theme.css';
import './launch-control-motion.css';

const PHASES = [
  {label: 'Detect', detail: 'Exception found'},
  {label: 'Route', detail: 'Owner assigned'},
  {label: 'Prove', detail: 'Receipt saved'},
];

let meshController = null;

function useReducedMotion() {
  const [reduced, setReduced] = useState(() => window.matchMedia('(prefers-reduced-motion: reduce)').matches);
  useEffect(() => {
    const query = window.matchMedia('(prefers-reduced-motion: reduce)');
    const update = () => setReduced(query.matches);
    query.addEventListener('change', update);
    return () => query.removeEventListener('change', update);
  }, []);
  return reduced;
}

function DetectPanel() {
  return <div className="trace-panel trace-detect" data-panel="detect">
    <div className="trace-panel-head"><div><small>Validator pass</small><strong>100 creative rows checked</strong></div><span>0.8 s</span></div>
    <div className="trace-rows" role="presentation">
      <div className="trace-row"><code>cr_004</code><span>Summer feed 04</span><em>Ready</em></div>
      <div className="trace-row is-exception"><code>cr_007</code><span>Launch offer 07</span><Badge label="Needs decision" variant="warning" /></div>
      <div className="trace-row"><code>cr_010</code><span>Stories cut 10</span><em>Ready</em></div>
    </div>
    <p className="trace-reason"><span aria-hidden="true">↳</span> Possible duplicate found before launch.</p>
  </div>;
}

function RoutePanel() {
  return <div className="trace-panel trace-route" data-panel="route">
    <div className="trace-panel-head"><div><small>Exception route</small><strong>cr_007 needs a named owner</strong></div><Badge label="Review" variant="warning" /></div>
    <div className="trace-route-grid">
      <div><small>Why it stopped</small><strong>Possible duplicate</strong><span>Same destination and offer, different asset.</span></div>
      <div className="trace-arrow" aria-hidden="true">→</div>
      <div><small>Decision owner</small><strong>Creative Ops Manager</strong><span>Ambiguous intent stays human.</span></div>
    </div>
  </div>;
}

function ProvePanel() {
  return <div className="trace-panel trace-prove" data-panel="prove">
    <div className="trace-receipt-mark" aria-hidden="true">✓</div>
    <div className="trace-receipt-copy"><small>Recorded decision</small><strong>Human confirmed · Keep both</strong><span>Saved locally with an inspectable receipt.</span></div>
    <dl className="trace-receipt-data"><div><dt>creative</dt><dd>cr_007</dd></div><div><dt>remaining</dt><dd>9</dd></div><div><dt>batch</dt><dd>78f20843aea8a367</dd></div></dl>
  </div>;
}

function PhasePanel({phase}) {
  if (phase === 0) return <DetectPanel />;
  if (phase === 1) return <RoutePanel />;
  return <ProvePanel />;
}

function MeshCanvas({active, reducedMotion, runId, onWebGL}) {
  const canvasRef = useRef(null);
  useEffect(() => {
    if (!active || !canvasRef.current) return undefined;
    if (navigator.connection?.saveData) {
      window.__launchControlMotion.fallback = 'save-data';
      return undefined;
    }
    let cancelled = false;
    let localController = null;
    import('./hero-mesh.js').then(({mountDecisionMesh}) => {
      if (cancelled || !canvasRef.current) return;
      try {
        localController = mountDecisionMesh(canvasRef.current, {
          reducedMotion,
          onStateChange(state, debug) {
            window.__launchControlMotion.mesh = debug;
            window.__launchControlMotion.state = state;
          },
        });
        meshController = localController;
        window.__launchControlMotion.mesh = localController.debug;
        window.__launchControlMotion.ready = true;
        window.dispatchEvent(new CustomEvent('launch-control-motion-ready'));
        onWebGL(true);
      } catch (error) {
        window.__launchControlMotion.fallback = 'webgl-unavailable';
        window.__launchControlMotion.error = String(error);
        window.__launchControlMotion.ready = true;
      }
    }).catch((error) => {
      window.__launchControlMotion.fallback = 'chunk-unavailable';
      window.__launchControlMotion.error = String(error);
      window.__launchControlMotion.ready = true;
    });
    return () => {
      cancelled = true;
      localController?.destroy();
      if (meshController === localController) meshController = null;
    };
  }, [active, reducedMotion, runId, onWebGL]);
  return <canvas ref={canvasRef} className="trace-mesh" id="meshGL" aria-hidden="true" />;
}

function RecordedTrace() {
  const rootRef = useRef(null);
  const reducedMotion = useReducedMotion();
  const [hasEntered, setHasEntered] = useState(reducedMotion);
  const [phase, setPhase] = useState(reducedMotion ? 2 : 0);
  const [runId, setRunId] = useState(0);
  const [isManual, setIsManual] = useState(false);
  const [webgl, setWebgl] = useState(false);
  const [liveMessage, setLiveMessage] = useState('');

  useEffect(() => {
    if (reducedMotion) {
      setHasEntered(true);
      setPhase(2);
      return undefined;
    }
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.intersectionRatio >= 0.6) {
        setHasEntered(true);
        observer.disconnect();
      }
    }, {threshold: [0.6]});
    observer.observe(rootRef.current);
    return () => observer.disconnect();
  }, [reducedMotion]);

  useEffect(() => {
    if (!hasEntered || reducedMotion || isManual) return undefined;
    setPhase(0);
    const routeTimer = window.setTimeout(() => setPhase(1), 2350);
    const proveTimer = window.setTimeout(() => setPhase(2), 4750);
    return () => {
      clearTimeout(routeTimer);
      clearTimeout(proveTimer);
    };
  }, [hasEntered, isManual, reducedMotion, runId]);

  function selectPhase(index) {
    setIsManual(true);
    setPhase(index);
    meshController?.seek(index);
    setLiveMessage(`${PHASES[index].label}: ${PHASES[index].detail}`);
  }

  function replay() {
    setIsManual(false);
    setPhase(0);
    setRunId((value) => value + 1);
    setLiveMessage('Recorded trace replayed from Detect.');
  }

  const progress = [34, 68, 100][phase];
  return <div ref={rootRef} className="lc-motion" data-phase={PHASES[phase].label.toLowerCase()} data-webgl={webgl ? 'ready' : 'fallback'}>
    <Theme theme={launchControlTheme} mode="light">
      <Card className="trace-card" padding={0} minHeight={430}>
        <div className="trace-topbar">
          <div className="trace-run-state"><StatusDot variant="accent" label="Recorded synthetic run" /><span>Recorded synthetic run</span></div>
          <span className="trace-boundary">Read-only replay · local data</span>
        </div>
        <div className="trace-progress"><ProgressBar value={progress} label="Recorded decision trace progress" isLabelHidden /></div>
        <ol className="trace-steps" aria-label="Recorded decision trace">
          {PHASES.map((item, index) => <li key={item.label} data-complete={index < phase ? 'true' : 'false'}>
            <button type="button" aria-current={index === phase ? 'step' : undefined} onClick={() => selectPhase(index)}>
              <b>{index < phase ? '✓' : `0${index + 1}`}</b><span><strong>{item.label}</strong><small>{item.detail}</small></span>
            </button>
          </li>)}
        </ol>
        <div className="trace-workspace">
          <PhasePanel phase={phase} key={`${phase}-${runId}`} />
          <div className="trace-rail" aria-hidden="true"><span></span><span></span><span></span></div>
          <div className="trace-token-fallback" aria-hidden="true"></div>
          <MeshCanvas active={hasEntered} reducedMotion={reducedMotion} runId={runId} onWebGL={setWebgl} />
        </div>
        <div className="trace-footer">
          <span>One exception. One owner. One receipt.</span>
          <Button className="trace-replay" label="Replay trace" variant="secondary" size="lg" onClick={replay} />
        </div>
        <p className="trace-static-summary">Recorded replay: cr_007 is detected as a possible duplicate, routed to the Creative Ops Manager, then saved locally after a human confirms “Keep both”.</p>
        <span className="trace-live" aria-live="polite">{liveMessage}</span>
      </Card>
    </Theme>
  </div>;
}

window.__launchControlMotion = {
  ready: false,
  version: '4.0.0',
  astryx: '0.1.6',
  three: '0.128.0',
  sequence: ['Detect', 'Route', 'Prove'],
};

const host = document.getElementById('hero-motion-root');
if (host) {
  let mounted = false;
  const mount = () => {
    if (mounted) return;
    mounted = true;
    createRoot(host).render(<RecordedTrace />);
  };
  const stylesheet = document.createElement('link');
  stylesheet.rel = 'stylesheet';
  stylesheet.href = 'assets/launch-control-motion.css';
  stylesheet.dataset.launchControlMotion = 'true';
  stylesheet.addEventListener('load', mount, {once: true});
  stylesheet.addEventListener('error', () => {
    window.__launchControlMotion.ready = true;
    window.__launchControlMotion.fallback = 'stylesheet-unavailable';
    window.dispatchEvent(new CustomEvent('launch-control-motion-ready'));
  }, {once: true});
  document.head.append(stylesheet);
}

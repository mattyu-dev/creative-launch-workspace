import React, {useEffect, useRef, useState} from 'react';
import {createRoot} from 'react-dom/client';
import {Badge} from '@astryxdesign/core/Badge';
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
const ROUTE_AT_MS = 2350;
const PROVE_AT_MS = 4750;
const TRACE_MOTION_MS = 6600;
const CALM_PAUSE_MS = 3200;
const LOOP_DURATION_MS = TRACE_MOTION_MS + CALM_PAUSE_MS;
const MANUAL_HOLD_MS = 5200;

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

function RecordedTrace() {
  const rootRef = useRef(null);
  const reducedMotion = useReducedMotion();
  const [hasEntered, setHasEntered] = useState(reducedMotion);
  const [isInView, setIsInView] = useState(false);
  const [pageVisible, setPageVisible] = useState(() => !document.hidden);
  const [phase, setPhase] = useState(reducedMotion ? 2 : 0);
  const [runId, setRunId] = useState(0);
  const [isManual, setIsManual] = useState(false);
  const [liveMessage, setLiveMessage] = useState('');

  useEffect(() => {
    window.__launchControlMotion.ready = true;
    window.dispatchEvent(new CustomEvent('launch-control-motion-ready'));
  }, []);

  useEffect(() => {
    if (reducedMotion) {
      setHasEntered(true);
      setPhase(2);
      return undefined;
    }
    const enterRatio = window.innerWidth < 768 ? 0.5 : 0.72;
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.intersectionRatio >= enterRatio) setHasEntered(true);
      setIsInView(entry.isIntersecting && entry.intersectionRatio >= 0.15);
    }, {threshold: [0, 0.15, 0.5, 0.72]});
    observer.observe(rootRef.current);
    return () => observer.disconnect();
  }, [reducedMotion]);

  useEffect(() => {
    const update = () => setPageVisible(!document.hidden);
    document.addEventListener('visibilitychange', update);
    return () => document.removeEventListener('visibilitychange', update);
  }, []);

  useEffect(() => {
    if (reducedMotion) {
      setPhase(2);
      window.__launchControlMotion.state = 'static';
      return undefined;
    }
    if (!hasEntered || !isInView || !pageVisible || isManual) return undefined;

    let cancelled = false;
    const timers = new Set();
    const later = (callback, delay) => {
      const timer = window.setTimeout(() => {
        timers.delete(timer);
        if (!cancelled) callback();
      }, delay);
      timers.add(timer);
    };
    const startCycle = () => {
      if (cancelled) return;
      setPhase(0);
      setRunId((value) => value + 1);
      window.__launchControlMotion.cycleCount += 1;
      window.__launchControlMotion.state = 'playing';
      later(() => setPhase(1), ROUTE_AT_MS);
      later(() => setPhase(2), PROVE_AT_MS);
      later(() => {
        window.__launchControlMotion.state = 'complete';
      }, TRACE_MOTION_MS);
      later(startCycle, LOOP_DURATION_MS);
    };

    startCycle();
    return () => {
      cancelled = true;
      timers.forEach((timer) => clearTimeout(timer));
      timers.clear();
    };
  }, [hasEntered, isInView, isManual, pageVisible, reducedMotion]);

  useEffect(() => {
    if (!isManual || reducedMotion || !isInView || !pageVisible) return undefined;
    const resumeTimer = window.setTimeout(() => setIsManual(false), MANUAL_HOLD_MS);
    return () => clearTimeout(resumeTimer);
  }, [isInView, isManual, pageVisible, reducedMotion]);

  function selectPhase(index) {
    setIsManual(true);
    setPhase(index);
    window.__launchControlMotion.state = 'seek';
    setLiveMessage(`${PHASES[index].label}: ${PHASES[index].detail}`);
  }

  const progress = [34, 68, 100][phase];
  return <div ref={rootRef} className="lc-motion" data-phase={PHASES[phase].label.toLowerCase()}>
    <Theme theme={launchControlTheme} mode="light">
      <Card className="trace-card" padding={0} minHeight={430}>
        <div className="trace-topbar">
          <div className="trace-run-state"><StatusDot variant="accent" label="Live product walkthrough" /><span>Live product walkthrough</span></div>
          <span className="trace-boundary">Automatic loop · local data</span>
        </div>
        <div className="trace-progress"><ProgressBar value={progress} label="Product walkthrough progress" isLabelHidden /></div>
        <ol className="trace-steps" aria-label="Product walkthrough">
          {PHASES.map((item, index) => <li key={item.label} data-complete={index < phase ? 'true' : 'false'}>
            <button type="button" aria-current={index === phase ? 'step' : undefined} onClick={() => selectPhase(index)}>
              <b>{index < phase ? '✓' : `0${index + 1}`}</b><span><strong>{item.label}</strong><small>{item.detail}</small></span>
            </button>
          </li>)}
        </ol>
        <div className="trace-workspace">
          <PhasePanel phase={phase} key={`${phase}-${runId}`} />
          <div className="trace-rail" aria-hidden="true"><span></span><span></span><span></span></div>
          <div className="trace-token" aria-hidden="true"></div>
        </div>
        <div className="trace-footer">
          <small className="trace-loop-note">One exception. One owner. One receipt. The walkthrough loops automatically.</small>
        </div>
        <p className="trace-static-summary">Looping walkthrough: cr_007 is detected as a possible duplicate, routed to the Creative Ops Manager, then saved locally after a human confirms “Keep both”.</p>
        <span className="trace-live" aria-live="polite">{liveMessage}</span>
      </Card>
    </Theme>
  </div>;
}

window.__launchControlMotion = {
  ready: false,
  version: '4.0.0',
  astryx: '0.1.6',
  renderer: 'css-token',
  sequence: ['Detect', 'Route', 'Prove'],
  loop: true,
  routeAtMs: ROUTE_AT_MS,
  proveAtMs: PROVE_AT_MS,
  motionDurationMs: TRACE_MOTION_MS,
  calmPauseMs: CALM_PAUSE_MS,
  loopDurationMs: LOOP_DURATION_MS,
  cycleCount: 0,
  state: 'idle',
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

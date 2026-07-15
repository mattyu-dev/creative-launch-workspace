import {execFileSync} from 'node:child_process';
import {gzipSync} from 'node:zlib';
import {mkdir, readFile, readdir, rm, writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import {build} from 'esbuild';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const generated = path.join(root, 'frontend', 'generated');
const outdir = path.join(root, 'docs', 'assets');
const chunkdir = path.join(outdir, 'launch-control-chunks');

await rm(generated, {recursive: true, force: true});
await rm(chunkdir, {recursive: true, force: true});
await rm(path.join(outdir, 'launch-control-motion.js'), {force: true});
await rm(path.join(outdir, 'launch-control-motion.css'), {force: true});
await mkdir(generated, {recursive: true});

execFileSync(process.execPath, [
  path.join(root, 'node_modules', '@astryxdesign', 'cli', 'bin', 'astryx.mjs'),
  'theme', 'build',
  path.join(root, 'frontend', 'launch-control-theme.mjs'),
  '--out', path.join(generated, 'launch-control-theme.css'),
], {cwd: root, stdio: 'inherit'});

for (const name of ['launch-control-theme.css', 'launch-control.js', 'launch-control.d.ts']) {
  const generatedPath = path.join(generated, name);
  const content = (await readFile(generatedPath, 'utf8'))
    .replace(/^ \* Command:.*\n/m, ' * Command: astryx theme build frontend/launch-control-theme.mjs\n')
    .replace(/^ \* Generated:.*\n/m, '');
  await writeFile(generatedPath, content);
}

await build({
  absWorkingDir: root,
  entryPoints: {'launch-control-motion': 'frontend/launch-control-motion.jsx'},
  outdir,
  bundle: true,
  splitting: true,
  format: 'esm',
  platform: 'browser',
  target: ['es2020'],
  minify: true,
  sourcemap: false,
  legalComments: 'inline',
  entryNames: '[name]',
  chunkNames: 'launch-control-chunks/[name]-[hash]',
  logLevel: 'info',
});

const bundleFiles = [
  path.join(outdir, 'launch-control-motion.js'),
  path.join(outdir, 'launch-control-motion.css'),
  ...(await readdir(chunkdir)).map((name) => path.join(chunkdir, name)),
];
for (const bundlePath of bundleFiles) {
  const content = await readFile(bundlePath, 'utf8');
  await writeFile(bundlePath, content.replace(/[ \t]+$/gm, ''));
}

const budgets = new Map([
  ['launch-control-motion.js', 115 * 1024],
  ['launch-control-motion.css', 36 * 1024],
]);
for (const [name, maxGzip] of budgets) {
  const bytes = await readFile(path.join(outdir, name));
  const gzip = gzipSync(bytes).byteLength;
  if (gzip > maxGzip) throw new Error(`${name} exceeds gzip budget: ${gzip} > ${maxGzip}`);
  console.log(`${name}: ${gzip} bytes gzip`);
}

const chunks = await readdir(chunkdir);
for (const name of chunks) {
  const bytes = await readFile(path.join(chunkdir, name));
  const gzip = gzipSync(bytes).byteLength;
  if (name.endsWith('.js') && gzip > 145 * 1024) {
    throw new Error(`${name} exceeds Three.js chunk budget: ${gzip} > ${145 * 1024}`);
  }
  console.log(`${name}: ${gzip} bytes gzip`);
}

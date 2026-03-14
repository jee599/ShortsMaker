import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';

import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';

import type {RenderProps} from '../src/types';

const readFlag = (name: string): string | undefined => {
  const index = process.argv.indexOf(name);
  if (index === -1) {
    return undefined;
  }

  return process.argv[index + 1];
};

const propsArg = readFlag('--props');
const outArg = readFlag('--out');

if (!propsArg || !outArg) {
  throw new Error('Usage: npm run render -- --props <props.json> --out <output.mp4>');
}

const projectRoot = path.resolve(import.meta.dirname, '..');
const entryPoint = path.join(projectRoot, 'src', 'index.ts');
const props = JSON.parse(fs.readFileSync(propsArg, 'utf-8')) as RenderProps;

const serveUrl = await bundle({
  entryPoint,
  publicDir: path.join(projectRoot, 'public'),
});

const composition = await selectComposition({
  serveUrl,
  id: props.compositionId,
  inputProps: props,
});

await renderMedia({
  composition,
  serveUrl,
  codec: 'h264',
  outputLocation: outArg,
  inputProps: props,
  chromiumOptions: {
    gl: 'angle',
  },
});

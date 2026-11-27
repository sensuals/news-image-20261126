// news-image-20261126 entry program (Node 22, standard library only).
//
// The entry image is the entry.png beside this file, drawn by
// generate_image.py from 40 verified stories of Thursday 26 November 2026.
// This program copies it to the output directory as entry.png, byte for
// byte, creating the directory first so the copy never fails on a missing
// folder. The judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));

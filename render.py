#!/usr/bin/env python3
"""Render a cartoon reel: frames from reel.html (Playwright) -> mp4 (ffmpeg) with the voice.
usage: python render.py WORK_FOLDER [--voice voice.mp3] [--still 1.5,4.2,...] [--fps 30]
WORK_FOLDER must contain reel.html, characters.js, scenes.json, words.json."""
import argparse, json, os, subprocess, sys, http.server, threading, functools, shutil

def need(pkg, imp=None):
    try: __import__(imp or pkg)
    except ImportError: subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', pkg], check=True)

ap = argparse.ArgumentParser(); ap.add_argument('work'); ap.add_argument('--voice'); ap.add_argument('--still'); ap.add_argument('--fps', type=int, default=30)
a = ap.parse_args(); W = os.path.abspath(a.work)
need('playwright'); need('imageio-ffmpeg', 'imageio_ffmpeg')
subprocess.run([sys.executable, '-m', 'playwright', 'install', 'chromium'], check=False)
import imageio_ffmpeg; FF = shutil.which('ffmpeg') or imageio_ffmpeg.get_ffmpeg_exe()
from playwright.sync_api import sync_playwright
srv = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=W))
threading.Thread(target=srv.serve_forever, daemon=True).start(); url = f'http://127.0.0.1:{srv.server_port}/reel.html'
sc = json.load(open(os.path.join(W, 'scenes.json'))); dur = max(s['t1'] for s in sc['scenes'])
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={'width': 1080, 'height': 1920}); pg.goto(url); pg.evaluate('LOAD()')
    if a.still:
        os.makedirs(os.path.join(W, 'stills'), exist_ok=True)
        for t in [float(x) for x in a.still.split(',')]:
            pg.evaluate(f'R({t})'); pg.screenshot(path=os.path.join(W, 'stills', f'still_{t:.2f}.png'))
        print('stills saved in', os.path.join(W, 'stills')); sys.exit()
    fr = os.path.join(W, 'frames'); os.makedirs(fr, exist_ok=True)
    n = int(dur * a.fps)
    for i in range(n):
        pg.evaluate(f'R({i / a.fps})'); pg.screenshot(path=os.path.join(fr, f'f{i:05d}.jpg'), quality=92)
        if i % 60 == 0: print(f'frame {i}/{n}', flush=True)
    b.close()
out = os.path.join(W, 'reel.mp4'); cmd = [FF, '-y', '-loglevel', 'error', '-framerate', str(a.fps), '-i', os.path.join(fr, 'f%05d.jpg')]
if a.voice: cmd += ['-i', a.voice, '-c:a', 'aac', '-b:a', '192k', '-shortest']
cmd += ['-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '20', '-movflags', '+faststart', out]
subprocess.run(cmd, check=True); shutil.rmtree(fr); print('saved', out)

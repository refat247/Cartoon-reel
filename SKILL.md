---
name: cartoon-reel-maker
description: Make a 9:16 flat cartoon reel (white-head characters, thick outlines, lit colorful world, slow camera, big karaoke subtitles) from a true story and a voice mp3. Use when the user asks for a cartoon reel, animated short, faceless history/science short, or "make a reel with this voice".
---

# Cartoon Reel Maker

Makes a 1080x1920, 30 fps cartoon reel the way viral history/science shorts look: flat 2D characters with white round heads, thick dark outlines and dot eyes, in a colorful world with real light and shadow, a slow gliding camera and big word-by-word subtitles. Everything is drawn with code (SVG in an HTML page), rendered to PNG frames with Playwright and joined with ffmpeg, so any single part can be fixed without redoing the whole video.

## Work in this order, and wait for the user's ok where it says so

1. **Style sheet** (optional). If the user gives screenshots of reels they like, measure them (do not give opinions): color brightness, highlight and shadow color, outline thickness, head shape, body height in heads, light direction, background blur, how often the shot changes, camera speed. Write the numbers in `style_sheet.md` in the work folder. Otherwise use `references/style_sheet.md`.
2. **Story.** Offer 10 true, surprising ideas for the topic, each as a one-line puzzle. Skip stories big channels already made viral.
3. **Facts.** Before writing, check every fact on the web and list them with sources (year, numbers, names). Never skip this.
4. **Script.** 35 to 45 seconds, about 4 spoken words per second. Shape: HOOK (puzzle in line one, no intro) → BUILD → YOU SEE (the real reason) → TWIST. Short sentences, numbers as words. Mark each part. See `references/script_rules.md`.
5. **Voice.** The user records it or uses ElevenLabs / Cartesia / Google AI Studio and gives you the mp3 (and a word timestamps JSON if they have one).
6. **Storyboard.** A numbered list: scene, start and end time, what is on screen, camera move. **Wait for ok.**
7. **Stills.** Render one still per shot (`scripts/render.py --still`). Check every still yourself (list below), fix, then show 4 stills. **Wait for ok.**
8. **Render** the MP4 with the voice, save it in the user's folder, and show it.
9. **Fixes.** Apply one-line fixes the user asks for (`references/fixes.md`), re-render only what changed.
10. **Thumbnail + cover** (1280x720 and 1080x1920): the puzzle in 3 or 4 huge words, the main character surprised next to it, readable on a small phone. 3 versions.
11. **Titles and captions**: 5 titles under 60 characters, description, Facebook caption ending in a question, 10 hashtags, one pinned comment.

## How to build the video

- Copy `assets/characters.js` and `assets/reel.html` to the work folder. `characters.js` has ready functions: `TOON(x,y,size,{out,mood,mouth,al,ar,wk,gun,flip})` for people (out: soldier, police, sailor, farmer, officer, plain; mood: smug, angry, shock), `EMU(...)` as an example animal, `MGUN(...)` a prop, `WFIELD(w,h,{light})` a lit field world where light 0 is bright day and 1 is deep blue night. Add new characters, animals and worlds in the same style (same outline color `OL`, same eye style).
- Write the storyboard as `scenes.json` (see `assets/scenes.example.json`): each scene has `t0`, `t1`, `world`, `light`, `chars`, `cam` (zoom and focus). Every value on screen must be a function of time `t`, so a frame at any time can be drawn again exactly.
- Subtitles: put the script words with their start times in `words.json` (from the user's JSON, or spread the words by syllables between pauses if no JSON). The spoken word turns yellow.
- Run `python scripts/render.py work_folder --voice voice.mp3` to render. It installs Playwright and ffmpeg (through `imageio-ffmpeg`) if missing.

## Rules (from the style sheet)

- Characters: flat, white round head, outline about 6 px at 1080 wide, dot eyes that blink every few seconds, eyebrows show feeling, clothes show who they are, body about 3.5 heads tall, thin arms and legs. Same character looks the same in every shot.
- World: colorful, warm highlights, cool blue or purple shadows, **no pure black anywhere**, background slightly blurred, dark ink lines on the world too.
- Light follows the story: bright and warm at the start, deeper blue when the real reason comes.
- Camera: new shot every 3 to 5 seconds, glide with ease in and out, never a hard jump.
- Subtitles: big, bottom third, thick dark stroke, current word yellow. Keep all text inside a 90% safe area.

## Self check before showing anything

For every still: is the camera inside a wall or object? Is anything in front of a face? Are colors right and is there pure black? Is any text outside the screen or covering a face? Does the character look the same as in other shots? Fix what you find before showing.

## Free plan

Split the story into half-minute parts. For the next part say: keep the same characters and style as before.

## Last step

When the user is happy, save every rule and every fix from this chat into this skill (update this file), so the next reel needs only the story.

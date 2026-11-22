# One-line fixes
- Subtitles come late: move every subtitle 0.2 s earlier.
- Text goes off screen: keep all text inside a 90% safe area.
- Video looks cheap or dull: compare with the style screenshot frame by frame, measure the difference (color, outline, light, blur, camera speed), then fix to match.
- Outline lost under blur: draw outlines after the blur, never blur the characters.
- Dark areas look black: lift shadows to deep blue, no pure black.
- Camera jumps: glide with ease in and out over at least 0.8 s.
- Character changes between shots: reuse the same TOON settings in every scene.

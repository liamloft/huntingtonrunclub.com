# 360° shirt mockups

`render.html` builds the black men's tee and women's racerback tank in three.js, puts the HRC logo on the chest, and renders a full turn. `grab.py` captures the frames.

```
cd tools/mockups
npm i three@0.170.0
python3 -m http.server 8765 &
SIZE=1200 python3 grab.py tee 120 all    # -> frames_tee/
SIZE=1200 python3 grab.py tank 120 all   # -> frames_tank/
ffmpeg -framerate 30 -i frames_tee/f%03d.png -vf "scale=720:720:flags=lanczos,format=yuva420p" \
  -c:v libwebp_anim -quality 78 -loop 0 ../../assets/drop02-mens.webp
```

To swap the logo, replace `logo.png` (white on transparent). To move or resize it, edit `logo: { y, width }` for each garment in `render.html` (metres from the hem / across the chest).

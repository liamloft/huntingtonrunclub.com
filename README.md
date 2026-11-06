# huntingtonrunclub.com

Huntington Run Club's site. First up: the Drop 02 merch pre-order page (made with lululemon, pre-orders open all of November 2026).

## What's here

- `index.html`: the whole site. One self-contained file with inline CSS and JS, no build step needed to host it.
- `tools/template.html` + `tools/pier.py`: source for `index.html`. The pier sketch is generated with a little hand-drawn wobble, so edit the template and rebuild:

  ```
  python3 tools/pier.py tools/template.html index.html
  ```

## Before going live

Edit the `CONFIG` block near the bottom of the page:

- `venmoHandle`: the club's Venmo username
- `styles`: the two pieces (men's EasySet sleeveless, women's Align tank): name, sizes, `price` (null leaves the amount blank in Venmo), lululemon link, and `image` (mockup in `assets/`, see `assets/README.md`)
- `email`, `phone`
- `heroGoesStraightToVenmo`: true makes the hero button skip the order form

## Hosting

Any static host works: Netlify, Vercel, Cloudflare Pages or GitHub Pages. Point the domain at it once it's bought.

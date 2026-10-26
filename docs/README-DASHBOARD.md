# Engineering dashboard

The public README uses self-contained SVGs. It runs no JavaScript and depends on no external image service. Existing artwork and earlier generators are preserved for recovery, but the current README embeds only assets/banner.svg, portrait.svg, neofetch.svg, tech-stack.svg, contributions.svg, impact.svg and individual project cards.

## Source and regeneration

- `data/dashboard.json`: profile facts and project descriptions, checked against the supplied resume and existing project sources. Update these facts before regenerating panels.
- `data/tech-icons.json`: authentic Simple Icons paths (CC0-1.0); semantic API, network, authentication and engineering icons are original line art.
- `scripts/generate_dashboard.py`: generates the hero, engineering information, stack, project and impact cards. The original ASCII character strings are copied intact from subhajit-ascii.svg with only the green accent adjusted.
- `scripts/fetch_contributions.py`: retrieves and validates public contribution dates/counts without a personal token.
- `scripts/generate_skyline.py`: exports the README animation and a static fallback from data/contributions.json. It ports the supplied component's camera, easing, week/day positioning, tower-height and staggered-wave formulas. Every cell remains the same polygon during the 2D-to-3D morph. An unsupported animation engine shows the base 3D geometry; reduced-motion users receive a separate static SVG through picture/source.

Run with Python's standard library:

```sh
python3 scripts/fetch_contributions.py
python3 scripts/generate_dashboard.py
python3 scripts/generate_skyline.py
```

The daily workflow runs these commands, preserves the earlier heatmap for compatibility, and commits only the generated data and SVGs. It uses the repository's built-in token for checkout and pushing, with contents-write as its only permission. No custom secrets are needed.

## React preview

The supplied component is preserved verbatim at `src/components/ui/contribution-skyline.tsx`. This repository was a Markdown profile, so a small isolated React/TypeScript/Vite preview and Tailwind configuration were added. No shadcn package is needed: the component imports only React and uses Tailwind utility classes. The `@/` alias resolves to `src/` for the conventional components/ui structure.

```sh
npm ci
npm run dev
npm run build
npm run preview
```

The entry point is preview/main.tsx. It always passes the real `data` and `endDate`; the supplied component's demo-data function is never used by the preview or export. The browser preview supports view switching, day details, keyboard navigation, and orbit dragging. The GitHub SVG has an automatic camera/tower cycle; README images cannot expose the component's interactive controls.

The React bundle is local preview source, not a deployed site, and is not loaded by the GitHub README. Production builds copy all referenced asset files into dist/assets. TypeScript checking and Vite bundling are part of `npm run build`.

## Data scope and links

The skyline covers the dates returned by GitHub's public calendar. It can differ from the account owner's private-activity total. Streaks use consecutive dates; the longest streak is limited to this calendar. The busiest day includes its actual date.

Nexio links to its verified public application and Cogniview to its public repository. Cointervues and Miles remain without public source links. The prior removal of Cointervues' public deployment link is preserved. Project visibility, code, and deployment configuration are unchanged.

Professional skills and impact figures are supported by the user's resume; the source resume and phone number are not copied into this repository. No account security or repository permissions were changed.

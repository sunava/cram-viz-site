# cram-viz-site

A static GitHub Pages deployment of [cram_viz](https://github.com/sunava/cognitive_robot_abstract_machine/tree/main/cram_viz)'s
**Recorded mode** — a browser-based 3D visualizer for the CRAM cognitive architecture,
replaying pre-recorded demo scenes with no server or ROS installation required.

This repository holds no application code of its own. Its one workflow
(`.github/workflows/deploy.yml`) checks out:

- the `cram_viz` frontend from
  [`sunava/cognitive_robot_abstract_machine`](https://github.com/sunava/cognitive_robot_abstract_machine),
- every demo scene bundle from
  [`sunava/cram-scenes`](https://github.com/sunava/cram-scenes),

assembles them into one static site, repairs the scenes index if it points at a
bundle that no longer exists, and publishes the result to GitHub Pages.

The Live mode (which needs a running Python backend for its EQL/knowledge-base
queries) is intentionally out of scope for this static deployment; only the
self-contained 3D scene playback works here.

## Rebuilding the site

The deploy workflow only runs on demand - trigger it from the
[Actions tab](../../actions/workflows/deploy.yml) ("Run workflow") whenever
`cram_viz`'s frontend or the scene bundles change.

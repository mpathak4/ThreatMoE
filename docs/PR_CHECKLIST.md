# PR Checklist for CI and Security Scans

Before requesting merge to main:
- CI (ci.yml) must pass: lint, unit tests, run_with_ckpt smoke test.
- CodeQL results should be reviewed on the PR; tune queries or suppress false positives.
- OSV and Trivy are scheduled; review their findings on the repository security tab.

Staged enforcement plan:
1. Require CI on PRs (immediate).
2. Run CodeQL on PRs but keep optional for merges.
3. After 2 successful PR cycles with manageable CodeQL noise, mark CodeQL as required for main.
4. Keep OSV/Trivy scheduled; promote to required only if you publish images or want dependency check gating.

How to promote a check to required:
- Merge PR that adds workflows.
- Validate action run names in Actions UI.
- Go to Settings → Branches → Protect main → Require status checks and add the job names you want to require.


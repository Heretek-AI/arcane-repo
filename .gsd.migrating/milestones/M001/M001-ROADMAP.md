# M001: Fix All Failing Docker Builds

**Vision:** All 37 Docker image build workflows in the arcane-repo GitHub Actions CI pass reliably. Every workflow builds its upstream project, installs dependencies via uv/npm, and pushes a working image to the container registry.

## Success Criteria

- All 37 Docker build workflows pass on GitHub Actions
- Final CI run shows 37/37 green (or 32/32 if Sunshine is deferred with documented reason)
- All workflow run IDs recorded in run log

## Slices

- [ ] **S01: Fix and verify all failing Docker builds** `risk:high` `depends:[]`
  > After this: All Docker image build workflows show green/pass status on GitHub Actions — including the previously broken builds and the runner-starved batch.

## Boundary Map

"### S01 → done\nProduces:\n- scripts/dockerfiles/*/Dockerfile — fixed build definitions\n- .github/workflows/*.yml — verified working CI\n\nConsumes: nothing"

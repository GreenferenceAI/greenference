# Greenference SDK Remaining Work Checklist

This checklist covers only `/workspace/Greenference/greenference`.

It does not track broader platform work in:
- `greenference-api`
- `greenference-miner`

## Critical
- [ ] Add a real installed-package validation path.
  - Verify `greenference` works when installed as a package, not only through workspace `PYTHONPATH`.
- [ ] Add CLI commands for image/build lifecycle depth.
  - `images history`
  - `builds list`
  - `builds get`
  - `builds logs`
  - `builds wait`
- [ ] Add workload lifecycle CLI depth.
  - `workloads create` from code ref without deploy
  - `workloads update` coverage for tags, readme, logo, pricing, alias clearing
  - `workloads utilization`
- [ ] Add deployment lifecycle CLI depth.
  - `deployments list`
  - `deployments get`
  - `deployments update`
  - `deployments wait`
- [ ] Add stronger error handling and exit behavior.
  - clearer CLI output for HTTP 4xx/5xx
  - non-zero exits for failed build, deploy, and wait flows
- [ ] Add packaging size safeguards.
  - warn or fail on oversized local contexts
  - surface included files more clearly before upload

## High
- [ ] Expand `Image` DSL parity.
  - maintainer
  - user
  - apt remove
  - richer add/copy semantics
  - better entrypoint/cmd/env ergonomics
- [ ] Expand workload DSL structure.
  - explicit concurrency and max instances as first-class SDK fields
  - clearer runtime config object instead of only flat runtime fields
  - support more metadata fields consistently
- [ ] Add richer Python client lifecycle helpers.
  - deployment wait helpers with better terminal-state classification
  - workload readiness helpers where meaningful
- [ ] Add Python client helpers for shares and warmup that are stable and documented.
- [ ] Improve build log streaming UX.
  - consistent SSE parsing
  - explicit end-of-stream and failure states
- [ ] Add a real examples directory.
  - minimal inference workload
  - vLLM-style workload
  - diffusion-style workload
  - build-only image example

## Medium
- [ ] Normalize template surface.
  - `greenference.templates` should be the canonical API
  - `workloads.py` should remain only as compatibility shim or be removed
- [ ] Add typed request/response wrappers in the client.
  - reduce raw dict/list API surface
- [ ] Improve config UX.
  - `config unset`
  - `config init`
  - mask secrets in display output
- [ ] Add alias-oriented invocation ergonomics.
  - make invoking deployed workloads by alias or derived identifier easier
- [ ] Improve packaging controls.
  - ignore patterns
  - explicit include/exclude overrides
  - clearer validation for paths outside project root

## Low
- [ ] Expand README and user docs.
  - full code-defined workflow
  - config setup
  - build/deploy/run examples
- [ ] Clean up deprecated helper wording and naming.
  - standardize around `Workload`
- [ ] Improve CLI tables and summaries.
  - better status views for builds and deployments

## Tests Required Before Calling The SDK Production-Ready
- [ ] Installed-package CLI tests, not only source-tree tests
- [ ] Module-ref build/deploy/run flow against a real local API stack
- [ ] Failure-path CLI tests:
  - build failure
  - deploy fee rejection
  - deployment timeout
  - permission denied on share or update
- [ ] Packaging tests for nested dirs, ignored files, and large contexts
- [ ] Config precedence tests across persisted config, env vars, and CLI flags
- [ ] Client retry and timeout tests for build/deploy polling flows

## Production-Ready Definition For This Repo
- [ ] A developer can install `greenference`, define an image/workload in Python, build it, deploy it, inspect it, and invoke it without raw payload assembly.
- [ ] The CLI and Python client handle normal failure modes cleanly.
- [ ] The packaging flow is safe enough for real project contexts.
- [ ] The SDK surface is stable, documented, and tested as an installed package.

# greenference

Shared Greenference developer-facing code:

- `protocol`: cross-service enums, request/response models, and signing helpers
- `sdk`: Python client and CLI
- `tests`: protocol and SDK tests

## SDK Workflow

The Greenference SDK supports a code-defined workflow:

1. Define an `Image` and `Workload` in Python.
2. Build from a module ref such as `examples/minimal_inference.py:workload`.
3. Create or deploy that workload through the CLI.
4. Inspect builds, deployments, warmup, and utilization from the same CLI.

Example commands:

```bash
greenference config init --base-url http://127.0.0.1:8000 --api-key <api-key>
greenference build examples/minimal_inference.py:workload --wait
greenference workloads create examples/minimal_inference.py:workload
greenference deploy examples/minimal_inference.py:workload --accept-fee --wait
greenference builds logs <build-id> --follow
greenference deployments wait <deployment-id>
```

## Examples

The repo includes example SDK definitions in [`examples/`](/workspace/Greenference/greenference/examples):

- `minimal_inference.py`
- `vllm_workload.py`
- `diffusion_workload.py`
- `build_only_image.py`

These examples are aligned with the current Greenference platform workflow rather than aspirational future runtime types.

## Config

The CLI resolves configuration in this order:

1. CLI flags
2. `GREENFERENCE_API_URL` / `GREENFERENCE_API_KEY`
3. persisted config under `~/.greenference/config.ini`

Useful commands:

```bash
greenference config init --base-url http://127.0.0.1:8000 --api-key <api-key>
greenference config show
greenference config unset --api-key
```

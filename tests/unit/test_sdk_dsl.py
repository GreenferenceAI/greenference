from __future__ import annotations

import io
import zipfile
from pathlib import Path

import pytest

from greenference import Image, NodeSelector, Workload
from greenference.config import get_config, save_config
from greenference.loader import load_workload
from greenference.packaging import package_workload
from greenference.templates import build_vllm_workload


def test_image_workload_loader_and_packaging(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    project = tmp_path / "project"
    project.mkdir()
    (project / "data.txt").write_text("payload", encoding="utf-8")
    (project / "app.py").write_text(
        """
from greenference import Image, NodeSelector, Workload

image = (
    Image(username="alice", name="demo", tag="latest")
    .from_base("python:3.12-slim")
    .add("data.txt", "/app/data.txt")
    .run_command("echo ready")
)

workload = Workload(
    name="demo-workload",
    image=image,
    node_selector=NodeSelector(gpu_count=1, min_vram_gb_per_gpu=24, concurrency=4),
    model_identifier="alice/demo-model",
)
""",
        encoding="utf-8",
    )
    monkeypatch.chdir(project)

    loaded = load_workload(f"{project / 'app.py'}:workload")
    packaged = package_workload(loaded.module_path, loaded.workload)

    assert loaded.workload.image_ref == "alice/demo:latest"
    assert loaded.workload.node_selector.to_requirements_payload()["concurrency"] == 4
    assert "RUN echo ready" in packaged.dockerfile_text
    assert packaged.included_paths == ["app.py", "data.txt"]

    with zipfile.ZipFile(io.BytesIO(packaged.archive_bytes)) as archive:
        assert sorted(archive.namelist()) == ["Dockerfile", "app.py", "data.txt"]


def test_config_file_and_env_precedence(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    config_path = tmp_path / "config.ini"
    monkeypatch.setenv("GREENFERENCE_CONFIG_PATH", str(config_path))

    saved = save_config(api_base_url="http://saved.example", api_key="saved-key")
    assert saved.api_base_url == "http://saved.example"
    assert saved.api_key == "saved-key"

    monkeypatch.setenv("GREENFERENCE_API_URL", "http://env.example")
    monkeypatch.setenv("GREENFERENCE_API_KEY", "env-key")
    resolved = get_config()

    assert resolved.api_base_url == "http://env.example"
    assert resolved.api_key == "env-key"


def test_template_builder_populates_rich_workload_defaults() -> None:
    workload_pack = build_vllm_workload(
        username="alice",
        name="llm-demo",
        model_identifier="meta-llama/Llama-3.2-1B-Instruct",
        display_name="LLM Demo",
        workload_alias="llm-demo-alias",
        tags=["llm", "chat"],
        context_paths=["README.md"],
    )

    payload = workload_pack.workload.to_workload_payload()

    assert workload_pack.template == "inference"
    assert payload["display_name"] == "LLM Demo"
    assert payload["workload_alias"] == "llm-demo-alias"
    assert payload["runtime"]["runtime_kind"] == "vllm"
    assert payload["lifecycle"]["warmup_enabled"] is True
    assert workload_pack.workload.context_paths == ["README.md"]

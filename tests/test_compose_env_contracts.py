from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def _compose_environment_lines(relative_path: str, service_name: str) -> list[str]:
    compose_data = yaml.safe_load((ROOT / relative_path).read_text(encoding="utf-8"))
    return [str(item) for item in compose_data["services"][service_name].get("environment", [])]


def test_compose_files_forward_vision_stream_default_env():
    expected_services = {
        "compose.yml": ["browser-pool"],
        "compose.local.yml": ["browser-pool"],
        "compose.test.yml": ["browser-pool", "test-runner"],
    }

    for relative_path, service_names in expected_services.items():
        for service_name in service_names:
            environment_lines = _compose_environment_lines(relative_path, service_name)
            assert "VISION_STREAM_DEFAULT=${VISION_STREAM_DEFAULT:-}" in environment_lines


def test_env_variables_doc_mentions_stream_default_compose_forwarding_and_sample():
    doc = (ROOT / "docs/ENV_VARIABLES.md").read_text(encoding="utf-8")

    assert "All shipped compose files forward `VISION_STREAM_DEFAULT`" in doc
    assert "| `VISION_STREAM_DEFAULT` | forwarded when set (app default false) |" in doc
    assert "VISION_STREAM_DEFAULT=true" in doc.split("## Example .env File", 1)[1]

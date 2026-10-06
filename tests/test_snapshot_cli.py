import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture(params=["single", "sharded"])
def snapshot_helper(tmp_path, request):
    skill = Path(__file__).resolve().parents[1] / "claude/podpitch/skills/podcast-discovery"
    (tmp_path / "scripts").mkdir()
    (tmp_path / "references").mkdir()
    script = tmp_path / "scripts/discover.py"
    shutil.copyfile(skill / "scripts/discover.py", script)
    catalog = {
        "source": "PodPitch public catalog snapshot",
        "captured_at": "2026-10-06T18:35:04+00:00",
        "podcasts": [
            {"id": "A2", "title": "Leadership Stories", "description": "Advice about software", "category": "Business"},
            {"id": "A1", "title": "Software", "description": "Interviews", "category": "Technology"},
            {"id": "A3", "title": "Making Things", "description": "Interviews", "category": "Crafts"},
        ],
    }
    if request.param == "single":
        (tmp_path / "references/catalog.json").write_text(json.dumps(catalog))
    else:
        index = {key: value for key, value in catalog.items() if key != "podcasts"}
        index["shards"] = [{"path": "catalog-001.json"}, {"path": "catalog-002.json"}]
        (tmp_path / "references/catalog.json").write_text(json.dumps(index))
        (tmp_path / "references/catalog-001.json").write_text(json.dumps({"podcasts": catalog["podcasts"][:1]}))
        (tmp_path / "references/catalog-002.json").write_text(json.dumps({"podcasts": catalog["podcasts"][1:]}))
    return script, catalog


def run_helper(script, *arguments):
    return subprocess.run([sys.executable, str(script), *arguments], capture_output=True, text=True)


def test_snapshot_cli_ranks_title_and_serializes_dated_results(snapshot_helper):
    script, catalog = snapshot_helper
    result = run_helper(script, "software", "--limit", "2")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert [show["id"] for show in payload["podcasts"]] == ["A1", "A2"]
    assert payload["source"] == catalog["source"]
    assert payload["captured_at"] == catalog["captured_at"]
    assert payload["is_live"] is False
    assert payload["is_complete_catalog"] is False


def test_snapshot_cli_matches_category_and_exact_id(snapshot_helper):
    script, catalog = snapshot_helper
    category = run_helper(script, "Crafts")
    assert json.loads(category.stdout)["podcasts"] == [catalog["podcasts"][2]]
    exact = run_helper(script, "--id", "A2")
    assert json.loads(exact.stdout)["podcasts"] == [catalog["podcasts"][0]]
    missing = run_helper(script, "--id", "missing")
    assert json.loads(missing.stdout)["podcasts"] == []


@pytest.mark.parametrize("query", ["podcasts", "the show", "unmatched-topic"])
def test_snapshot_cli_no_matches_is_successful_json(snapshot_helper, query):
    script, _ = snapshot_helper
    result = run_helper(script, query)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["podcasts"] == []


@pytest.mark.parametrize("arguments", [[], [" "], ["software", "--limit", "0"], ["software", "--limit", "11"]])
def test_snapshot_cli_rejects_missing_query_and_invalid_limit(snapshot_helper, arguments):
    script, _ = snapshot_helper
    result = run_helper(script, *arguments)
    assert result.returncode == 2
    assert "error:" in result.stderr
    assert result.stdout == ""

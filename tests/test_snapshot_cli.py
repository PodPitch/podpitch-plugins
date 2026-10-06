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
        index["record_count"] = len(catalog["podcasts"])
        index["shards"] = [{"path": "catalog-001.json", "record_count": 1},
                           {"path": "catalog-002.json", "record_count": 2}]
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


def test_shipped_catalog_is_complete_and_searchable():
    skill = Path(__file__).resolve().parents[1] / "claude/podpitch/skills/podcast-discovery"
    index = json.loads((skill / "references/catalog.json").read_text())
    records = []
    for shard in index["shards"]:
        shard_path = skill / "references" / shard["path"]
        payload = json.loads(shard_path.read_text())
        assert shard_path.stat().st_size < 128_000
        assert len(payload["podcasts"]) == shard["record_count"]
        records.extend(payload["podcasts"])
    assert len(records) == index["record_count"] == 5848
    assert len({record["id"] for record in records}) == 5848
    result = run_helper(skill / "scripts/discover.py", "B2B SaaS founders", "--limit", "3")
    assert result.returncode == 0, result.stderr
    assert [record["id"] for record in json.loads(result.stdout)["podcasts"]] == [
        "A1338265938", "A1495008122", "A1538169815",
    ]


@pytest.mark.parametrize("failure", ["missing", "invalid_json", "wrong_shard_count", "wrong_total_count"])
def test_shard_failure_returns_clear_error(snapshot_helper, failure):
    script, _ = snapshot_helper
    index_path = script.parent.parent / "references/catalog.json"
    index = json.loads(index_path.read_text())
    if "shards" not in index:
        pytest.skip("Shard failure applies to sharded catalogs")
    shard_path = index_path.parent / index["shards"][0]["path"]
    if failure == "missing":
        shard_path.unlink()
    elif failure == "invalid_json":
        shard_path.write_text("{")
    elif failure == "wrong_shard_count":
        index["shards"][0]["record_count"] = 3
    else:
        index["record_count"] = 4
    index_path.write_text(json.dumps(index))
    result = run_helper(script, "software")
    assert result.returncode == 2
    assert "Bundled PodPitch catalog is unavailable or incomplete" in result.stderr
    assert "Traceback" not in result.stderr
    assert result.stdout == ""

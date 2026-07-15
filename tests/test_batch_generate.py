import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from batch_generate import parse_script, generate_from_script


SCRIPT_PATH = os.path.join(os.path.dirname(__file__), "..", "scripts", "example.txt")


def test_parse_script_returns_expected_number_of_scenes():
    lines = parse_script(SCRIPT_PATH)
    assert len(lines) == 3


def test_parse_script_preserves_scene_ids_in_order():
    lines = parse_script(SCRIPT_PATH)
    ids = [scene_id for scene_id, _ in lines]
    assert ids == ["scene_01", "scene_02", "scene_03"]


def test_parse_script_skips_blank_lines(tmp_path):
    script = tmp_path / "script.txt"
    script.write_text("scene_01: Hello there.\n\n\nscene_02: Goodbye.\n")
    lines = parse_script(str(script))
    assert len(lines) == 2


def test_parse_script_handles_colons_inside_text(tmp_path):
    script = tmp_path / "script.txt"
    script.write_text("scene_01: He said: this is it.\n")
    lines = parse_script(str(script))
    assert lines[0] == ("scene_01", "He said: this is it.")


class FakeClient:
    def generate_speech(self, text, voice_id, stability=0.5, similarity_boost=0.75):
        return f"AUDIO({text})".encode("utf-8")


def test_generate_from_script_writes_manifest_and_clips(tmp_path):
    output_dir = str(tmp_path / "output")
    manifest = generate_from_script(FakeClient(), SCRIPT_PATH, voice_id="v1", output_dir=output_dir)

    assert manifest["voice_id"] == "v1"
    assert len(manifest["clips"]) == 3

    for clip in manifest["clips"]:
        assert os.path.exists(clip["output_path"])

    assert os.path.exists(os.path.join(output_dir, "manifest.json"))

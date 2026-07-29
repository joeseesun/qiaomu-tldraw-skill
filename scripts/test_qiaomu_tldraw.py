#!/usr/bin/env python3
"""Standard-library unit tests for qiaomu_tldraw.py."""

SCRIPT_INTERFACE = "internal-module"

import json
import http.client
import tempfile
import unittest
from unittest import mock
from pathlib import Path

import qiaomu_tldraw as tool


class OfficialToolTests(unittest.TestCase):
    def test_rejects_non_official_url(self):
        with self.assertRaises(ValueError):
            tool.ensure_official_url("https://example.com/llms.txt")

    def test_offline_app_info_is_best_effort(self):
        result = tool.offline_app_info()
        self.assertIn("installed", result)
        if result["installed"]:
            self.assertTrue(result.get("version"))

    def test_retries_incomplete_official_download(self):
        class Response:
            def __init__(self, content=None, error=None, status=200, content_range=None):
                self.content = content
                self.error = error
                self.status = status
                self.headers = {"content-length": str(len(content))} if content is not None else {}
                if content_range:
                    self.headers["content-range"] = content_range

            def __enter__(self):
                return self

            def __exit__(self, *_):
                return False

            def read(self):
                if self.error:
                    raise self.error
                return self.content

        incomplete = http.client.IncompleteRead(b"part", 4)
        with mock.patch.object(
            tool.urllib.request,
            "urlopen",
            side_effect=[
                Response(error=incomplete, status=200),
                Response(content=b"done", status=206, content_range="bytes 4-7/8"),
            ],
        ) as mocked:
            self.assertEqual(tool.fetch_bytes("https://tldraw.dev/llms.txt"), b"partdone")
            self.assertEqual(mocked.call_count, 2)

    def test_parses_current_cli_help_shape(self):
        help_text = """Available starter kits:
 • basic                A minimal template.
 • branching-chat       A branching chat interface.

"""
        self.assertEqual(
            tool.parse_templates(help_text),
            [
                {"id": "basic", "description": "A minimal template."},
                {"id": "branching-chat", "description": "A branching chat interface."},
            ],
        )

    def test_searches_cached_official_docs(self):
        with tempfile.TemporaryDirectory() as temporary:
            cache = Path(temporary)
            (cache / "llms-docs.txt").write_text(
                "# Shapes\nNative shapes.\n\n## Custom shapes\nUse ShapeUtil for custom shapes.\n",
                encoding="utf-8",
            )
            result = tool.docs_search("custom ShapeUtil", "docs", cache, 5)
            self.assertEqual(result["results"][0]["heading"], "Custom shapes")

    def test_project_info_finds_tldraw_dependencies(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "package-lock.json").write_text("{}\n", encoding="utf-8")
            (root / "package.json").write_text(
                json.dumps(
                    {
                        "name": "demo",
                        "dependencies": {"tldraw": "^5.2.5"},
                        "devDependencies": {"@tldraw/validate": "^5.2.5"},
                        "scripts": {"build": "vite build"},
                    }
                ),
                encoding="utf-8",
            )
            result = tool.project_info(root)
            self.assertEqual(result["package_manager"], "npm")
            self.assertEqual(sorted(result["tldraw_dependencies"]), ["@tldraw/validate", "tldraw"])


if __name__ == "__main__":
    unittest.main()

import urllib.parse

import pytest
from airbrowser_client.models import CreateBrowserRequest, ExecuteScriptRequest, NavigateBrowserRequest


@pytest.mark.browser
def test_cjk_glyphs_do_not_collapse_to_missing_glyph_hash(browser_client):
    html = """<!doctype html><html><meta charset=\"utf-8\"><body style=\"font:64px sans-serif\">中文测试 日本語テスト 한국어 테스트</body></html>"""
    url = "data:text/html;charset=utf-8," + urllib.parse.quote(html)
    browser_id = None

    create_result = browser_client.create_browser(payload=CreateBrowserRequest(window_size=[1200, 800]))
    assert create_result.success
    browser_id = create_result.data["browser_id"]

    try:
        navigate_result = browser_client.navigate_browser(browser_id, payload=NavigateBrowserRequest(url=url))
        assert navigate_result.success

        probe_result = browser_client.execute_script(
            browser_id,
            payload=ExecuteScriptRequest(
                script="""
                const glyphs = {
                  chinese: '中',
                  japanese: 'テ',
                  korean: '한',
                  missing: String.fromCodePoint(0xF0000),
                };
                const canvas = document.createElement('canvas');
                canvas.width = 120;
                canvas.height = 120;
                const ctx = canvas.getContext('2d');
                ctx.textBaseline = 'top';
                ctx.font = '64px sans-serif';

                function hashFor(ch) {
                  ctx.clearRect(0, 0, canvas.width, canvas.height);
                  ctx.fillStyle = '#fff';
                  ctx.fillRect(0, 0, canvas.width, canvas.height);
                  ctx.fillStyle = '#000';
                  ctx.fillText(ch, 10, 10);

                  const data = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
                  let hash = 0;
                  for (let i = 0; i < data.length; i += 1) {
                    hash = (hash * 131 + data[i]) % 1000000007;
                  }
                  return hash;
                }

                return Object.fromEntries(
                  Object.entries(glyphs).map(([label, ch]) => [label, hashFor(ch)])
                );
                """
            ),
        )
        assert probe_result.success

        hashes = probe_result.data["result"]["value"]
        assert len({hashes["chinese"], hashes["japanese"], hashes["korean"]}) == 3
        assert hashes["chinese"] != hashes["missing"]
        assert hashes["japanese"] != hashes["missing"]
        assert hashes["korean"] != hashes["missing"]
    finally:
        if browser_id:
            try:
                browser_client.close_browser(browser_id)
            except Exception:
                pass

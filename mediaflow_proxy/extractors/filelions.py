from typing import Dict, Any

from mediaflow_proxy.extractors.base import BaseExtractor
from mediaflow_proxy.utils.packed import eval_solver


class FileLionsExtractor(BaseExtractor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mediaflow_endpoint = "hls_manifest_proxy"

    async def extract(self, url: str, **kwargs) -> Dict[str, Any]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.92 Mobile Safari/537.36",
            "Accept": "*/*",
            "Referer": url,
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
        }

        patterns = [
            r"""["'](?:hls\d*|source|file)["']\s*:\s*["']([^"']*(?:\.m3u8|\.hls)[^"']*)["']""",
            r"""sources:\s*\[{file:\s*["']([^"']+)["']""",
            r"""["']file["']\s*:\s*["']([^"']*(?:\.m3u8|\.hls)[^"']*)["']""",
            r"""(?:hls|source)_url\s*:\s*["']([^"']*(?:\.m3u8|\.hls)[^"']*)["']""",
        ]

        final_url = await eval_solver(self, url, headers, patterns)

        self.base_headers["referer"] = url

        return {
            "destination_url": final_url,
            "request_headers": self.base_headers,
            "mediaflow_endpoint": self.mediaflow_endpoint,
            "stream_transformer": "ts_stream",
        }

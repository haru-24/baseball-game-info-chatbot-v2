from abc import ABC, abstractmethod

import requests


class AbstractScraper(ABC):
    """スクレイピング抽象クラス"""

    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_page_content(self, url):
        """指定されたURLからページコンテンツを取得する"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            raise Exception(f"エラー: {url}の取得中に問題が発生しました - {e}")

    @abstractmethod
    def parse_content(self, html):
        """ページコンテンツを解析する抽象メソッド"""
        pass

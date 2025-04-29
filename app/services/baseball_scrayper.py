from bs4 import BeautifulSoup

from app.services.abstract_scrayper import AbstractScraper


class BaseballScraper(AbstractScraper):
    """野球情報をスクレイピングするクラス"""

    def __init__(self):
        super().__init__(base_url="https://baseball.yahoo.co.jp/npb/")

    def get_today_games(self):
        """本日の試合一覧を取得する"""
        schedule_url = f"{self.base_url}schedule/"
        html = self.get_page_content(schedule_url)
        return self.parse_content(html)

    def parse_content(self, html):
        """ページコンテンツを解析する実装メソッド"""
        if not html:
            return "試合結果を取得できませんでした。"

        soup = BeautifulSoup(html, "html.parser")
        output = []

        try:
            game_results = soup.find("div", id="gm_card")
            if not game_results:
                return "試合情報が見つかりませんでした。"

            sections = game_results.find_all("section")
            for section in sections:
                league_heading = section.find("h1")
                if not league_heading:
                    continue

                league = league_heading.text.strip()
                game_list = section.find_all("li")

                output.append(f"{league}")
                output.append("-------------------")

                for game in game_list:
                    stadium = game.find("span", class_="bb-score__venue")
                    inning = game.find("p", class_="bb-score__link")
                    home_team = game.find("p", class_="bb-score__homeLogo")
                    away_team = game.find("p", class_="bb-score__awayLogo")
                    score_left = game.find("span", class_="bb-score__score--left")
                    score_right = game.find("span", class_="bb-score__score--right")

                    if stadium and inning and home_team and away_team and score_left and score_right:
                        output.append(f"{stadium.text.strip()}  {inning.text.strip()}")
                        output.append(
                            f"{home_team.text.strip()}  | {score_left.text.strip()} - {score_right.text.strip()} | {away_team.text.strip()}\n"
                        )

            output.append(f"{self.base_url}schedule/")
            return "\n".join(output)
        except Exception as e:
            raise Exception(f"エラーが発生しました: {str(e)}")

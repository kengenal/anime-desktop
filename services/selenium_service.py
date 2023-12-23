from dataclasses import dataclass
from sqlite3 import Cursor

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

from database.episode_database import EpisodeDatabase
from models.episodes_model import EpisodeElement, Player


class SeleniumService:
    def __init__(self, episode_database: EpisodeDatabase) -> None:
        self.episode_database = episode_database
        self.options = Options()
        self.options.add_argument("--headless")

    def get_sources(self, episode: EpisodeElement, mal_id: int):
        driver = webdriver.ChromiumEdge(options=self.options)
        for player in episode.players:
            public_id = f"{mal_id}-{episode.episode}-{player.url}-{player.player_source}"

            player_object = Player(
                url=player.url,
                source=player.source,
                type=player.type,
                player_source=player.player_source,
            )

            if res := self.episode_database.get_casched_episode(public_id):
                c_id, url = res
                player_object.url = url
                yield player_object
            else:
                driver.get(player.url)
                yield player_object
                element = driver.find_element(By.TAG_NAME, "video")
                video_source = element.get_attribute("src")
                if video_source:
                    player_object.url = video_source
                    self.episode_database.set_casched_episode(
                        url=video_source, public_id=public_id
                    )
                    yield player_object
        print("close driver")
        return driver.quit()

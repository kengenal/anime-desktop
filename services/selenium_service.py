import sys
import threading
from typing import Generator, Tuple

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from database.episode_database import EpisodeDatabase
from models.episodes_model import EpisodeElement, Player


class SeleniumService:
    def __init__(self, episode_database: EpisodeDatabase) -> None:
        self.episode_database = episode_database
        if sys.platform == "win32":
            self.options = EdgeOptions()
            self.options.add_experimental_option(
                "prefs",
                {
                    "profile.managed_default_content_settings.images": 2,
                },
            )
        else:
            self.options = ChromeOptions()
        self.options.add_argument("--headless")
        self.options.add_argument("--no-sandbox")
        self.driver = None
        self.wait = None
        self.event = threading.Event()
        threading.Thread(target=self.inital_driver, daemon=True).start()

    def inital_driver(self):
        if sys.platform == "win32":
            self.driver = webdriver.ChromiumEdge(options=self.options)
        else:
            self.driver = webdriver.Chrome(options=self.options)
        self.wait = WebDriverWait(self.driver, 4)
        self.event.set()

    def get_sources(
        self, episode: EpisodeElement, mal_id: int
    ) -> Generator[None, None, Tuple[int, Player]]:
        to_fetch = []
        for player in episode.players[:3]:
            if res := self.episode_database.get_casched_episode(
                self._create_id(
                    mal_id=mal_id, player=player, episode=episode.episode
                )
            ):
                c_id, url = res
                yield episode.episode, Player(
                    url=url,
                    source=player.source,
                    type=player.type,
                    player_source=player.player_source,
                )
            else:
                to_fetch.append(player)
        if to_fetch:
            self.event.wait()
            for player in to_fetch:
                self.driver.get(player.url)
                element = self.wait.until(
                    EC.presence_of_element_located((By.TAG_NAME, "video"))
                )
                video_source = element.get_attribute("src")
                if video_source:
                    self.episode_database.set_casched_episode(
                        url=video_source,
                        public_id=self._create_id(
                            mal_id=mal_id,
                            player=player,
                            episode=episode.episode,
                        ),
                    )
                    yield episode.episode, Player(
                        url=video_source,
                        source=player.source,
                        type=player.type,
                        player_source=player.player_source,
                    )

    def quit(self):
        def close():
            print("close driver")
            self.driver.quit()

        threading.Thread(target=close, daemon=True).start()

    def _create_id(self, mal_id: str, player: Player, episode: int) -> str:
        return f"{mal_id}-{episode}-{player.url}-{player.player_source}"

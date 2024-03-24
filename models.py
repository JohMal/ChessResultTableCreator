from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class GameResult(Enum):
    UNKNOWN = "0 - 0"
    HOME_TEAM_WIN = "1 - 0"
    HOME_TEAM_DEFAULT_WIN = "+ - -"
    GUEST_TEAM_WIN = "0 - 1"
    GUEST_TEAM_DEFAULT_WIN = "- - +"
    DRAW = "½ - ½"

@dataclass(frozen=True)
class MatchResult:
    home_team_points: float
    guest_team_points: float
    result: GameResult
    parsed_result: str

@dataclass(frozen=True)
class Team:
    name: str
    avarage_rating: int

@dataclass(frozen=True)
class Player: 
    name: str
    rating: int

@dataclass(frozen=True)
class Game:
    home_player: Player
    guest_player: Player
    result: GameResult

@dataclass(frozen=True)
class Match:
    home_team: Team
    guest_team: Team
    games: list[Game]
    result: MatchResult

@dataclass(frozen=True)
class TeamConfig:
    name: str
    base_url: str
    key: str

@dataclass(frozen=True)
class Config:
    teams: list[TeamConfig]
    zps_region_code: int
    result_file_name: str







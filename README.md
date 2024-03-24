# Chess Result Table Creator

The chess result table creator is a small python script to create html based result tables for league games of your local german chess club. 

## Functionality
When starting the main.py, the user can select one or all of the configured teams and one or all rounds. 

The script then parses the selected matches, updates the ratings with the current dwz database of the german chess federation (Schachbund) and writes the created html tables in the configured result file. 

In cases, the player's current rating cannot be found, the parsed rating is used instead and a warning is displayed.  

## Configuration
To use the script, a valid config.py has to be added. 
An example config is given below:

```python
from models import Config, TeamConfig

_team_1 = TeamConfig(
    name="Club name 1",
    base_url="<result-data-base-url>",
    key="Club name"
)

_team_2 = TeamConfig(
    name="Club name 2",
    base_url="<result-data-base-url>",
    key="Club name"
)


config = Config(
    teams=[_team_1, _team_2],
    zps_region_code=600, # 600 = NRW
    result_file_name="result.txt",
)
```

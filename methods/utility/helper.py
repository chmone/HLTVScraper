import datetime
from pytz import zoneinfo
import tzlocal
import zoneinfo
from helper import _get_all_teams
from HLTVScraper.methods.utility.parse import get_parsed_page
from python_utils import converters

HLTV_COOKIE_TIMEZONE = "Europe/Copenhagen"
HLTV_ZONEINFO=zoneinfo.ZoneInfo(HLTV_COOKIE_TIMEZONE)
LOCAL_TIMEZONE_NAME = tzlocal.get_localzone_name()
LOCAL_ZONEINFO = zoneinfo.ZoneInfo(LOCAL_TIMEZONE_NAME)

TEAM_MAP_FOR_RESULTS = []


class helper:
    
    def _get_all_teams():
        if not TEAM_MAP_FOR_RESULTS:
            teams = get_parsed_page("https://www.hltv.org/stats/teams?minMapCount=0")
            for team in teams.find_all("td", {"class": ["teamCol-teams-overview"], }):
                team = {'id': converters.to_int(team.find("a")["href"].split("/")[-2]), 'name': team.find("a").text, 'url': "https://hltv.org" + team.find("a")["href"]}
                TEAM_MAP_FOR_RESULTS.append(team)

    def _findTeamId(teamName: str):
        _get_all_teams()
        for team in TEAM_MAP_FOR_RESULTS:
            if team['name'] == teamName:
                return team['id']
        return None

    def _padIfNeeded(numberStr: str):
        if int(numberStr) < 10:
            return str(numberStr).zfill(2)
        else:
            return str(numberStr)

    def _monthNameToNumber(monthName: str):
        # Check for the input "Augu" and convert it to "August"
        # This is necessary because the input string may have been sanitized
        # by removing the "st" from the day numbers, such as "21st" -> "21"
        if monthName == "Augu":
            monthName = "August"
        return datetime.datetime.strptime(monthName, '%B').month

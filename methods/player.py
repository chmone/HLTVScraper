import requests
from HLTVScraper.methods.utility.parse import get_parsed_page
from HLTVScraper.methods.utility.helper import scrape_urls_concurrently
from collections import OrderedDict
from HLTVScraper import methods


# class Player:
    
#     def get_player_url(player_id, nickname, match_type=None, startDate=None, endDate=None, ranking=None, map_name=None):
#         # Base URL
#         url = f"https://www.hltv.org/stats/players/{player_id}/{nickname}"
        
#         # Initialize a list to hold query parameters
#         query_params = []
        
#         # Add optional parameters if they are provided
#         if match_type:
#             query_params.append(f"matchType={match_type}")
        
#         if startDate and endDate:
#             query_params.append(f"startDate={startDate}&endDate={endDate}")
        
#         if ranking:
#             query_params.append(f"rankingFilter={ranking}")
        
#         if map_name:
#             query_params.append(f"maps={map_name}")
        
#         # If there are any query parameters, append them to the URL
#         if query_params:
#             url += "?" + "&".join(query_params)

#         return url
    
#     def get_player_stats_sup(soup):
        
#         # Initialize an OrderedDict to hold player stats in the desired order
#         player_stats = OrderedDict()

#         # Player Summary Stats (from "playerSummaryStatBox")
#         summary_stats = OrderedDict()  # Also using OrderedDict for consistent order in summary stats
#         summary_stat_box = soup.find('div', class_='playerSummaryStatBox')
#         if not summary_stat_box:
#             print ("No player summary stats found")
#             return
#         info = summary_stat_box.find('div', class_='summaryShortInfo')
        

#         # Populate player details first
#         player_stats['name'] = info.find('div', class_='summaryRealname text-ellipsis').text.strip()
#         player_stats['nickname'] = info.find('h1', class_='summaryNickname text-ellipsis').text.strip()

#         team_element = info.find('div', class_='SummaryTeamname text-ellipsis').find('a', class_='a-reset text-ellipsis')
#         if team_element is not None:
#             player_stats['team'] = team_element.text.strip()
#         else:
#             player_stats['team'] = 'No Team'
#         player_stats['age'] = info.find('div', class_='summaryPlayerAge').text.strip().split(" ")[0]
#         player_stats['country'] = info.find('img', class_='flag').get('title')
        
#         teammates = []
#         teammate_elements = soup.find_all('div', class_='teammate standard-box')

#         for teammate_element in teammate_elements:
#             teammate_info = OrderedDict()

#             name_and_nickname = teammate_element.find('img').get('title').split("'")
#             teammate_info['full_name'] = name_and_nickname[0].strip()
#             teammate_info['nickname'] = name_and_nickname[1].strip()

#             rating_element = teammate_element.find('div', class_='teammate-info')  # Update based on HTML structure
#             text = rating_element.text.strip().split("\n")
#             teammate_info['rating'] = text[len(text) - 1]
            
#             teammates.append(teammate_info)

#         player_stats['teammates'] = teammates

#         # Player summary stats
#         summary_row = summary_stat_box.find_all('div', class_='summaryStatBreakdownRow')
#         for row in summary_row:
#             stats = row.find_all('div', class_='summaryStatBreakdown aboveAverage')
#             for stat in stats:
#                 stat_name = stat.find('div', class_='summaryStatBreakdownSubHeader').contents[0].strip()
#                 stat_value = stat.find('div', class_='summaryStatBreakdownDataValue').text.strip()
#                 summary_stats[stat_name] = stat_value
                
#         player_stats['summary_stats'] = summary_stats

        
#         # Player Total Stats (from "statistics")
#         total_stats = soup.find('div', class_='statistics')
#         total_result = OrderedDict()

#         for stat in total_stats.find_all('div', class_='stats-row'):
#             inside = stat.find_all('span')
#             stat_name = inside[0].text.strip()
#             stat_value = inside[1].text.strip()
#             total_result[stat_name] = stat_value

#         player_stats["total_stats"] = total_result


#         # player role deep level stats    
#         role_stats = OrderedDict()
#         role_stats_section = soup.find_all('div', class_='role-stats-section')
#         sides = ['Combined', 'CT', 'T']

#         for section in role_stats_section:
#             subheader = section.find('div', class_='role-stats-section-title').text.strip().split('\n')[0]
#             role_stats[subheader] = OrderedDict()

#             stat_rows = section.find_all('div', class_='role-stats-row')

#             for index, stat_row in enumerate(stat_rows):
#                 side = sides[index % len(sides)]  # Cycle through Combined, CT, T

#                 if side not in role_stats[subheader]:
#                     role_stats[subheader][side] = OrderedDict()

#                 stat_name = stat_row.find('div', class_='role-stats-title').text.strip()
#                 stat_value = stat_row.find('div', class_='role-stats-data').text.strip()

#                 role_stats[subheader][side][stat_name] = stat_value

#         player_stats['role_stats'] = role_stats

#         return player_stats

#     def get_player_stats(player_id, nickname, match_type=None, startDate=None, endDate=None, ranking=None, map_name=None):
#         return get_player_stats_sup(get_player_url(player_id, nickname, match_type, startDate, endDate, ranking, map_name))
                        
#     def get_top_player_stats():
#         players = top_players()
#         urls = []

#         for player in players:
#             urls.append(get_player_url(player['id'], player['nickname']))
        
#         soups = scrape_urls_concurrently(urls)

#         #try:
#         results = []
#         for soup in soups:
#             results.append(get_player_stats_sup(soup[0]))
#         #except:
#         #   print("Failed on link: " + soup[1])

#         return results

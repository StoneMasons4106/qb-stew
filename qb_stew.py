from bs4 import BeautifulSoup as bs
import requests
import pymongo
import pandas as pd


def show_menu():
    
    """Displays basic menu that allows for user input,
    to enter player data or break the loop"""
    
    print("")
    print("1. Search for player data")
    print("2. Exit")
    
    option = input("Enter option: ")
    return option


def input_player_data():
    
    """Asks for QB names and appends them to a list"""
    
    players = []
    
    while True:
        
        first_name = input("Please supply the first name of the player you are searching: " )
        last_name = input("Please supply the last name of the player you are searching: " )
        pos = 'QB'
        
        player_data = [first_name, last_name, pos]
        players.append(player_data)
        
        while True:
            
            confirmation = input("Do you wish to add another player? Y or N: ")
            print("")
            
            if confirmation == 'n' or confirmation == 'N':
                return players
            elif confirmation == 'y' or confirmation == 'Y':
                break
            else:
                print("Invalid input, please input Y or N.")


def search_player(first_name, last_name, pos):
    
    """Searches for the relevant player data on Pro Football Reference"""
    
    req = requests.get("https://www.pro-football-reference.com/search/search.fcgi?hint="+first_name+"+"+last_name+"&search="+first_name+"+"+last_name)
    soup = bs(req.text, 'html.parser')
    search_data = soup.find_all('div', class_='search-item')
    
    try:
        for item in search_data:
            pos_split_one = str(item).split("</a>  ")
            pos_split_two = pos_split_one[1].split(" (")
            if pos_split_two[0] == pos:
                url_split_one = pos_split_two[1].split('search-item-url">')
                url_split_two = url_split_one[1].split('</div>\n<div class="search-item-league">')
                break
        url = "https://www.pro-football-reference.com"+url_split_two[0]
        req2 = requests.get(url)
        soup2 = bs(req2.text, 'html.parser')
        return soup2
    except:
        l_last_name = list(last_name)
        l_first_name = list(first_name)
        url = "https://www.pro-football-reference.com/players/"+l_last_name[0]+"/"+''.join(l_last_name[0:4])+''.join(l_first_name[0:2])+'00.htm'
        req2 = requests.get(url)
        soup2 = bs(req2.text, 'html.parser')
        return soup2


def get_player_data(year, players):
    
    """Extracts the data from HTML, 
    connects to MongoDB to collect other relevant information."""
    
    print('Getting data for ' + players[0] + ' ' + players[1] + '...')
    
    player_page = search_player(players[0], players[1], players[2])
    last_year_passing = player_page.findAll('tr', id='passing.' + str(year))
    
    try:
        rating_split_one = str(last_year_passing[0]).split('"pass_rating">')
        rating_split_two = rating_split_one[1].split('</td>')
        try:
            rating_split_three = rating_split_two[0].split('<strong>')
            rating_split_four = rating_split_three[1].split('</strong>')
            rating = rating_split_four[0]
        except:
            rating = rating_split_two[0]
        
        qbr_split_one = str(last_year_passing[0]).split('"qbr">')
        qbr_split_two = qbr_split_one[1].split('</td>')
        try:
            qbr_split_three = qbr_split_two[0].split('<strong>')
            qbr_split_four = qbr_split_three[1].split('</strong>')
            qbr = qbr_split_four[0]
        except:
            qbr = qbr_split_two[0]
            
        anya_split_one = str(last_year_passing[0]).split('"pass_adj_net_yds_per_att">')
        anya_split_two = anya_split_one[1].split('</td>')
        try:
            anya_split_three = anya_split_two[0].split('<strong>')
            anya_split_four = anya_split_three[1].split('</strong>')
            anya = anya_split_four[0]
        except:
            anya = anya_split_two[0]
            
        try:
            conn = mongo_connect(MONGO_URI)
        except:
            print("Could not connect to MongoDB")
            return 'Database connection error'
        
        try:
            coll = conn[DATABASE][COLLECTION]
            doc = coll.find_one({"first": players[0], "last": players[1]})
            pff = doc['pff_grade']
            dvoa = doc['dvoa']
            cpoe = doc['cpoe']
            epa = doc['epa']

            return float(rating), float(qbr), float(anya), float(pff), float(dvoa), float(cpoe), float(epa)

        except:
            print("No matching record for " + players[0] + " " + players[1] + " in our database.")

    except:
        print('No data found for ' + players[0] + ' ' + players[1])


def mongo_connect(url):
    
    """Connect to MongoDB QBStew Cluster"""
    
    print("Connecting to MongoDB...")
    conn = pymongo.MongoClient(url)
    return conn
        

def analyze_player_data(player_data):
    
    """Use pandas to rank players based on results of pulled statistics"""
    
    print("Analyzing the data...")
    
    ranks = []
    
    for i in enumerate(player_data):
        ranks.append(int(i[0]) + 1)
    
    df = pd.DataFrame(player_data, columns=['first', 'last', 'pos', 'rating', 'qbr', 'anya', 'pff', 'dvoa', 'cpoe', 'epa'])
    df_rating_sort = df.sort_values(by=['rating'], ascending=False)
    df_rating_sort['rating rank'] = ranks
    df_qbr_sort = df_rating_sort.sort_values(by=['qbr'], ascending=False)
    df_qbr_sort['qbr rank'] = ranks
    df_anya_sort = df_qbr_sort.sort_values(by=['anya'], ascending=False)
    df_anya_sort['anya rank'] = ranks
    df_pff_sort = df_anya_sort.sort_values(by=['pff'], ascending=False)
    df_pff_sort['pff rank'] = ranks
    df_dvoa_sort = df_pff_sort.sort_values(by=['dvoa'], ascending=False)
    df_dvoa_sort['dvoa rank'] = ranks
    df_cpoe_sort = df_dvoa_sort.sort_values(by=['cpoe'], ascending=False)
    df_cpoe_sort['cpoe rank'] = ranks
    df_epa_sort = df_cpoe_sort.sort_values(by=['epa'], ascending=False)
    df_epa_sort['epa rank'] = ranks
    df_last_sort = df_epa_sort.sort_values(by=['last'], ascending=True)
    df_last_sort['qb stew'] = (df_last_sort['rating rank'] + df_last_sort['qbr rank'] + df_last_sort['anya rank'] + df_last_sort['pff rank'] + df_last_sort['dvoa rank'] + df_last_sort['cpoe rank'] + df_last_sort['epa rank']) / 7
    
    df_final = df_last_sort.sort_values(by=['qb stew'], ascending=True)
    return df_final


def export_to_excel(dataframe):
    
    print("")
    
    dataframe.to_excel("QB_Stew.xlsx", index=False)
    
    print("Exported to Excel!")


def main_loop():
    
    """Main loop of actions"""
    
    while True:
        option = show_menu()
        if option == "1":
            while True:
                year = input("Please supply the year of the data you are researching: " )
                if year != '2020':
                    print("Data isn't available for that year. Please try again.")
                else:
                    break
            global COLLECTION
            COLLECTION = str(year)
            players_list = input_player_data()
            player_data_list = []
            for players in players_list:
                player_data = get_player_data(year, players)
                if player_data == 'Database connection error':
                    break
                elif player_data is None:
                    pass
                else:
                    for i in player_data:
                        players.append(i)
                    player_data_list.append(players)
            if player_data == 'Database connection error':
                print('Unable to complete analysis due to being unable to access the database')
            else:
                df = analyze_player_data(player_data_list)
                print("")
                print(df)
                export_to_excel(df)
        elif option == "2":
            break
        else:
            print("That is not a valid option. Please choose either 1 or 2.")
        

MONGO_URI = "mongodb+srv://user:pa55w0r6@qbdata.2dvh9.mongodb.net/Stew?retryWrites=true&w=majority"
DATABASE = "Stew"        


main_loop()
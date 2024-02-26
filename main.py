import requests
import re
from bs4 import BeautifulSoup

def scrape_clash_decks():
    url = 'https://www.deckshop.pro/deck/new-meta'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        decks = soup.find_all('div', class_='deck-container-wide')
        bestDecks = []
        for deck in decks:
            title = deck.find('h5').text.strip()
            cards = deck.find_all('a', class_='grid')
            cards = [img['alt'] for img in cards[0].find_all('img')]
            bestDecks.append({"title": title, "cards": cards})
            # print("Title:", title)
            # print("Cards:")
            # for card in cards:
            #     print("         " + card)
            # print("-" * 50)
        return bestDecks
    else:
        print("Failed to retrieve data from Clash Decks.")

def getMyClashLevels(playerTag):
    url = f'https://royaleapi.com/player/{playerTag}/cards/levels'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        cards = soup.find_all('div', class_='ui basic segment player_cards__container')
        myCards = [card for card in cards[0].find_all('a')]
        userCards = []
        for card in myCards:
            userCards.append({"card": card.find('img')['alt'],
                              "level": card.find('div', class_="ui center aligned player_cards__card_level").text.strip("\n")[4:]})
            # userCards.append({"name": card.find('img')})
        return userCards
    else:
        print("Failed to retrieve data from Clash Decks.")

def checkBestDecks(bestDecks, myCards):
    bestDeck = []
    for deck in bestDecks:
        totalLevel = 0
        for card in deck['cards']:
            temp = [data for data in myCards if data['card'] == card][0]['level']
            if temp.strip(' ') == 'e':
                temp = 15
            totalLevel += int(temp)
        bestDeck.append({"name": deck['title'], "totalLevel": totalLevel, "cards": deck['cards']})
        bestDeck = sorted(bestDeck, key=lambda x: x['totalLevel'], reverse=True)
    return bestDeck



if __name__ == "__main__":
    bestDecks = scrape_clash_decks()
    print("Welcome to the clash royale meta deck picker made by Dylan Hall")
    print("This program scrapes the best current clash royale decks from ")
    print("deckshop.com and then sorts them according to your cards current level")
    playerTag = input("\nEnter your player tag to continue: ")
    #90PLCCG82
    myCards = getMyClashLevels(playerTag)
    bestDeck = checkBestDecks(bestDecks, myCards)
    print("\nThese are the best decks for you based on your current card level in ascending order: ")
    index = 0
    for deck in bestDeck:
        print(str(index) + ": " +deck['name'])
        index += 1
    userIndex = input("if you want to see a decks card simply input the decks number here: ")
    print("\nTitle:", bestDeck[int(userIndex)]['name'])
    print("Cards:")
    for card in bestDeck[int(userIndex)]['cards']:
        print("         " + card)



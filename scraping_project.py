from bs4 import BeautifulSoup as bs
import requests
from random import randint

# web scraping quote data

quote_list = []
page_number = ""
page_counter = 1

html = requests.get(f"http://quotes.toscrape.com{page_number}")
soup = bs(html.text,"html.parser")
quotes = soup.find_all("div", class_ = "quote")
for quote in quotes:
    quote_text = quote.find(class_ = "text").get_text()
    author = quote.find(class_ = "author").get_text()
    href = quote.find("a")["href"]
    quote_list.append(quote_text)
    quote_list.append(author)
    quote_list.append(href)
    next = soup.find_all(class_ = "next")
    for page in next:
        page_number = page.find("a")["href"]

while(page_counter < 11):
        html = requests.get(f"http://quotes.toscrape.com{page_number}")
        soup = bs(html.text,"html.parser")
        quotes = soup.find_all("div", class_ = "quote")
        for quote in quotes:
            quote_text = quote.find(class_ = "text").get_text()
            author = quote.find(class_ = "author").get_text()
            href = quote.find("a")["href"]
            quote_list.append(quote_text)
            quote_list.append(author)
            quote_list.append(href)
        next = soup.find_all(class_ = "next")
        for page in next:
            page_number = page.find("a")["href"]
        page_counter += 1

# game element

continue_game = "y"

while continue_game == "y": #loop while user is selecting yes to continue

    # generate question and hints
    number_of_quotes = int(len(quote_list)/3)
    random_quote_number = randint(1,number_of_quotes)
    random_quote = quote_list[random_quote_number*3]
    random_author = quote_list[random_quote_number*3+1]
    random_author_lower = random_author.lower()
    random_href = quote_list[random_quote_number*3+2]
    quote_hint_html = requests.get(f"http://quotes.toscrape.com{random_href}")
    hint_soup = bs(quote_hint_html.text,"html.parser")
    author_dob= hint_soup.find(class_ = "author-born-date").get_text()
    author_born_location = hint_soup.find(class_ = "author-born-location").get_text()
    first_name_letter = random_author[0]
    split_name = random_author.split()
    last_name_letter = split_name[1][0]

    #reset the number of guesses from any previous games
    guesses_remaining = 4

    # guess 1
    print(f"You have {guesses_remaining} guesses remaining.")
    print(f"Guess who said this quote: {random_quote}")
    guess = input()

    if guess.lower() == random_author_lower:
        print("Congratulations! You guessed correctly!")
    
    else:
        guesses_remaining -= 1
        print(f"You have {guesses_remaining} guesses remaining.")
        print(f"Here's a clue. The author was born on {author_dob} {author_born_location}")
        guess = input()

        if guess.lower() == random_author_lower:
            print("Congratulations! You guessed correctly!")

        else:
            guesses_remaining -= 1
            print(f"You have {guesses_remaining} guesses remaining.")
            print(f"Here's a clue. The author's first name begins with {first_name_letter}.")
            guess = input()

            if guess.lower() == random_author_lower:
                print("Congratulations! You guessed correctly!")

            else:
                print(f"This is your last guess!")
                print(f"Here's a clue. The author's last name begins with {last_name_letter}.")
                guess = input()

                if guess.lower() == random_author_lower:
                    print("Congratulations! You guessed correctly!")

                else:
                    print(f"You ran out of guesses! The correct answer was {random_author}.")

    continue_game = input("Do you want to play again? (y/n)")
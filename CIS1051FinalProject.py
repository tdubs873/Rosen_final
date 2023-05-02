import pandas as pd
import random


# Selects a random book from list of 2,000 most beloved books on gr
def select_random_book():
    df = pd.read_csv('books_data.csv')
    selected_book = df.sample(1).iloc[0]  # Select a random row and convert it to a Series
    return selected_book['title'], selected_book['author'], selected_book['date_published'], selected_book['average_rating']


def directions():
    while True:
        print("Hey there! Welcome to LitGuesser")
        print("The goal of the game is to guess the average star rating of a given book from the website 'GoodReads' ")
        print("The game uses data from the top 2,000 books on the 'best books of all time' list on GR")
        print("There are five total rounds, and you may skip the current question 5 times")
        print("A perfect guess is worth 200 points (1,000 max score)")
        print("Good luck!")
        start_game = input("Enter any key to start: ")
        if start_game != "":
            break


# Prompts user with info + gather a response
# The way I interact with the same variables in play_game() and main() is a bit ugly, but I couldn't figure out any other
# way that I could solve the issue. Making the variables global wasn't working
def play_game(book_info, round_number, total_score, num_skips):
    title, author, date_published, average_rating = book_info
    print("Title: ", title)
    print("Author: ", author)
    print("Date Published: ", date_published)
    print("Skips remaining: ", num_skips)
    user_guess = input("Guess the average rating (1-5) of the book, or type 'skip' to try another book: ")

    if user_guess == "skip":
        if num_skips > 0:
            print()
            print()
            num_skips -= 1
            return round_number, total_score, num_skips  # Pass the information back to the main() function
        else:
            print("You have no skips left. Please guess the average rating (1-5) of the book.")
            print()
            print()
            return play_game(book_info, round_number, total_score, num_skips)  # Call function again with the same input
    else:
        try:
            user_guess = float(user_guess)
            round_number += 1
            print("Correct Answer: ", average_rating)
            print("Points Earned: ", calculate_reward(average_rating, user_guess))
            print("Total Score: ", total_score)
            print()
            print()
            return round_number, total_score + calculate_reward(average_rating, user_guess), num_skips  # Pass information back to main()
        except ValueError:
            print("Invalid input. Please enter a number 1-5, or 'skip'")
            print()
            print()
            return play_game(book_info, round_number, total_score, num_skips)  # Call function again, same concept as line 44


# Calculates the score for each correct guess, inverse exponential
# Goal is to reward players who are extremely skilled, while not punishing players who are not experts
def calculate_reward(correct, guessed):
    difference = abs(correct - guessed)
    score = (1.5 ** (-1.5 * difference)) * 200

    return score


# Main loop of game
def main():
    num_rounds = 5  # A couple variables used in both main() and play_game()
    round_number = 1
    total_score = 0
    num_skips = 5


    # print directions - this is the first thing the user sees when running the code
    directions()
    print()
    print()
    print()
    print()


    # Loop runs while user is playing
    while round_number <= num_rounds:
        current_book = select_random_book()  # pulls the random  book from csv
        print("Round: ", round_number, ": ")
        round_number, total_score, num_skips = play_game(current_book, round_number, total_score, num_skips)  # run the game and update associated variables


    print("Game over!")
    print("Final Score: ", total_score)


main()
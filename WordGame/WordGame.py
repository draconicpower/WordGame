import os
import random
# Program Chosen is Word Builder
# Program Chosen is Word Builder
def displayTitle(titleFilePath):
    """
    Displays the content of a text file given its path.

    Parameters:
    - titleFilePath (string): The path of the file to display.

    Returns:
    None
    """
    try:
        with open(titleFilePath, 'r') as file:
            # Read all lines from the file and store them in 'title_content'
            title_content = file.readlines()
            # iterate trough each line in "title content" and print it after removing trailing whitespaces
            for line in title_content:
                print(line.rstrip())
    # Handle the specific case when the file is not found
    except FileNotFoundError:
        print(f"An error occurred while trying to access file '{titleFilePath}'. Exiting application.")
        exit()
    except IOError as e:
        print(f"An I/O error occurred: {e}. Exiting application.")
        exit()


def updateui(selectindex):
    """
    Update the user interface based on the selected index.

    Parameters:
    - selectindex (int): The index corresponding to a specific user interface image.

    Returns:
    None
    """
    
    # Check if the selected index is within the valid range of UI images
    if 0 <= selectindex < len(ui_images):
        # Print the selected UI image along with its index and a separator line
        print(f"Selected Image {selectindex + 1}:\n{ui_images[selectindex]}\n{'='*40}\n")
    else:
        # Print an error message if the selected index is invalid
        print(f"Invalid index. Please choose a valid index between 1 and {len(ui_images)}.")

def displayMenu():
    """
    Display the Word Game Menu and prompt the user for a choice.

    Parameters:
    None

    Returns:
    string: The menu choice as a string.
    """
    print("=== Word Game Menu ===")
    print("a. Enter Personal Details")
    print("b. Start Playing the Game")
    print("c. Add Letters to Text File")
    print("d. Quit Game")

    while True:
        choice = input("Enter your choice ").strip().lower() #takes user input and removes spaces

        if choice.isalpha() and len(choice) == 1: #checks if its a letter then sees if its lenght is 1
            return choice
        else:
            print("Invalid choice. Please enter a valid letter (a, b, c, or d).")

# Rest of your code...


def enterpersonal():
    """
    Takes user input for name.

    Parameters:
    None

    Returns:
    None
    """
    global name
    name = input("Enter Name Here ").lower() # name input for leaderboard
    #age was removed due to lack of compatibility with the letter rule
def GameFinished():
    """
    Display the game completion screen with the player's name and score.

    Parameters:
    None

    Returns:
    None
    """
    updateui(2) # output Last ASCII art 
    print(name, "Got", wordsCorr, "Words Correct!") # print name followed by how much words you got
    updateHighScores(name, wordsCorr) # updates highscore (sees if you surpassed anyone)
    displayHighScores() # afterhighscore is either updated or it remaining the same it is outputted

def loadWordList(wordListFilePath):
    """
    Load the word list from the specified file.

    Parameters:
    - wordListFilePath (string): The file path of the word list.

    Returns:
    set: A set containing words from the file.
    """
    try:
        with open(wordListFilePath, 'r') as file:
            # Read the content of the file, split it into a list of words, and convert it to a set
            word_list = set(file.read().split())
            return word_list
    except FileNotFoundError:
        # Handle the case when the file is not found
        print(f"Word list file not found: '{wordListFilePath}'. Exiting application.")
        exit()
    except IOError as e:
        # Handle other I/O errors
        print(f"An I/O error occurred: {e}. Exiting application.")
        exit()

def startPlayingGame():
    """
    Start the Word Builder game.

    Parameters:
    None

    Returns:
    None
    """
        
    updateui(0) # output first ASCII art
    print("Write Every Word Possible! \n You can only Write the Word Once!") # print rules
    startWordBuilderGame(word_list)

def startWordBuilderGame(wordList):
    """
    Start the Word Builder game loop.

    Parameters:
    - wordList (set): A set containing valid words.

    Returns:
    None
    """
    updateui(1)
    global wordsCorr
    wordsCorr = 0
    # Generate a random word from the specified file or use a default if file not found
    random_word = generateRandomWord(wordsFilePath)
    # Print the message indicating the start of the game with the selected letters
    print(f"Letters for the game: {random_word}")

    guessedwords = set()

    while True:
        word = input("Enter a word (type 'exit' to end game): ").strip().lower() # takes word strips it and lowercases it

        if word == 'exit':
            GameFinished() 
            break

        if word in guessedwords:
            # Ignore duplicate entries
            os.system('cls' if os.name == 'nt' else 'clear')
            print("You already guessed that word. Try again.")
            print(f"Current Score: {wordsCorr}")
            print(f"Letters for the game: {random_word}")
            continue

        if isValidWord(word, random_word, wordList):
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Valid word! Keep going.")
            wordsCorr += 1
            print(f"Current Score: {wordsCorr}")
            print(f"Letters for the game: {random_word}")
            guessedwords.add(word.lower())  # Add the word to the set of guessed words and lower cases it
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Invalid word. Try again.")
            print(f"Letters for the game: {random_word}")

def isValidWord(word, available_letters, word_list):
    """
    Check if the entered word is valid.

    Parameters:
    - word (string): The entered word.
    - available_letters (string): The letters available for the game.
    - word_list (set): A set containing valid words.

    Returns:
    bool: True if the word is valid, False otherwise.
    """
    if word not in word_list:
        return False

    for letter in word:
        if letter not in available_letters:
            return False
    return True


def addWordsToFile(wordsFilePath, newWords):
    """
    Append new words to a text file.

    Parameters:
    - wordsFilePath (string): The path of the file to append to.
    - newWords (list): List of words to add to the file.

    Returns:
    None
    """
    try:
        with open(wordsFilePath, 'a') as file:
            for word in newWords:
                if word.strip():  # Check if the word is not empty
                    file.write(word.strip().lower() + '\n') # adds the letters to the files
            print("Words successfully added to the file.")
    except IOError as e:
        print(f"An I/O error occurred: {e}. Exiting application.")
        exit()


def generateRandomWord(wordsFilePath):
    """
    Generate a random word from the specified file or use a default if the file is not found.

    Parameters:
    - wordsFilePath (str): The file path containing the words.

    Returns:
    str: The randomly selected word.
    """
    try:
        # Try to open the specified file
        with open(wordsFilePath, 'r') as file:
            words = file.readlines()
            random_word = random.choice(words).strip()   # Choose a random word from the list and striping it
            return random_word # Return the randomly selected word
    except FileNotFoundError: # Handle the case when the specified file is not found
        print("Words file not found. Backup words will be used instead.")
        default_words = ["boailer", "crolsgnsl", "lponsmiu", "oiunmplj", "crownbasf"] # Default words to be used if the file is not found
        return random.choice(default_words)  # Choose a random word from the default list
    except IOError as e:
        print(f"An error occurred while trying to fetch the word: {e}. Exiting application.")
        exit()

def loadGameUIImages(filePath):
    """
    Load user interface images from a specified file.

    Parameters:
    - filePath (str): The file path of the user interface images.

    Returns:
    list: A list containing user interface images as strings.
    """
    try:
        with open(filePath, 'r') as file:
            images = file.read().split('\n\n')  # Split content based on double newline
            return images
    except FileNotFoundError:
        print(f"An error occurred while trying to access the user interface file '{filePath}'. Exiting application.")
        exit()
    except IOError as e:
        print(f"An I/O error occurred: {e}. Exiting application.")
        exit()

def updateHighScores(player_name, score):
    """
    Update the high scores file with a new player's name and score.

    Parameters:
    - player_name (str): The player's name.
    - score (int): The player's score.

    Returns:
    None
    """
    # Read existing high scores from the file
    try:
        with open(HSF, 'r') as file:
            high_scores = [line.strip().split(',') for line in file.readlines()]
    except FileNotFoundError:
        high_scores = []

   
    high_scores.append([player_name, str(score)])  # Add the new score to the list
    high_scores.sort(key=lambda x: int(x[1]), reverse=True) # Sort the scores by the score value (in descending order)

    # Keep only the top 10 scores
    high_scores = high_scores[:10]

    # Write the updated high scores back to the file
    with open(HSF, 'w') as file:
        for entry in high_scores:
            file.write(','.join(entry) + '\n')

def isHighScore(score):
    """
    Check if the provided score is a high score.

    Parameters:
    - score (int): The score to check.

    Returns:
    bool: True if the score is a high score, False otherwise.
    """
    # Check if the provided score is a high score
    try:
        with open(HSF, 'r') as file:
            high_scores = [int(line.strip().split(',')[1]) for line in file.readlines()]  # Read all lines from the file, extract and convert scores to integers
            if len(high_scores) < 10 or score > min(high_scores):  # Check if there are less than 10 high scores or if the new score is higher than the lowest high score
                return True # Return True if the score qualifies as a high score
    except FileNotFoundError:
        return True

    return False

def displayHighScores():
    """
    Display the high scores stored in the high scores file.

    Parameters:
    None

    Returns:
    None
    """
    try:
        with open(HSF, 'r') as file:
            high_scores = [line.strip().split(',') for line in file.readlines()] # Read all lines from the file, extract player names and scores
            if not high_scores: # Check if there are no high scores available
                print("No high scores available.") 
            else:
                print("=== High Scores ===")
                for i, (player, score) in enumerate(high_scores, start=1):
                    print(f"{i}. {player}: {score}")
                print(" ")
    except FileNotFoundError:
        print("No high scores available.")

name = "Name Not Given" # assigns name just in case the user doesnt input it
Age = 0 # assigns age as 0, just in case the user doesnt input it
Titlepath = 'ASCII.txt' # sets path
wordsFilePath = "wordstouse.txt" # sets path
ui_file_path = 'UIImages.txt'  # sets path
Allwords = 'AllWords.txt' # sets path, this file contains a lot of english words 
HSF = "highscores.txt" # sets path for the highscore file
ui_images = loadGameUIImages(ui_file_path)  # list that stores all ASCII art
word_list = loadWordList(Allwords) #loads all the words that are valid in the variable
displayTitle(Titlepath) #display the title screen
while True:
    user_choice = displayMenu() # displays the menu and stores return in variable

    if user_choice == 'a':
        enterpersonal() # calls enteterpersonal function
    elif user_choice == 'b':
        startPlayingGame() #calls startplaying game function
    elif user_choice == 'c':
        new_words_to_add = [] # defines a list
        while True:
            word = input("Enter a word (type 'exit' to finish): ") #aks for user input
            if word.lower() == 'exit': # checks if lowercase word is exit, if its exit break
                break
            new_words_to_add.append(word.lower()) # appens new word and lower cases it
        addWordsToFile(wordsFilePath, new_words_to_add) # adds the list to the file
    elif user_choice == 'd':
        print("Exiting the game. Goodbye!")
        break

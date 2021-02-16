#! /usr/local/bin/python3
# 2048.py plays the popular game automatically by moving the arrow keys up, right, down and left
# We can modify this code later to keep playing until a max score is achieved or it reaches a max retry limit
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

URL = 'https://play2048.co/'
TARGET_SCORE = 2000
RETRY_LIMIT = 3

num_of_retries = 0

driver = webdriver.Chrome()
driver.get(URL)

def play_2048():
    moves = [Keys.UP, Keys.RIGHT, Keys.DOWN, Keys.LEFT]
    while True:
        driver.find_element_by_tag_name('html').send_keys(moves)
        if is_game_over() :
            if is_replay(): continue
            else:  break
        else: continue

def is_replay():
    # score comes in as '1024\n+4'
    score = int(driver.find_element_by_class_name("score-container").text.split('\n')[0])
    if score < TARGET_SCORE:
        if num_of_retries < RETRY_LIMIT:
            print(f"Retrying the game, number of retries: {num_of_retries + 1}")
            replay_game()
            return True
        else:
            print(f"Quitting the browser as the max retry limit {RETRY_LIMIT} is reached")
            quit_game()
            return False
    else:
        print(f"Quitting the browser as the target score {TARGET_SCORE} has been achieved with game score {score}")
        quit_game()
        return False

def replay_game():
    global num_of_retries
    num_of_retries += 1
    time.sleep(1) #lets actually wait for the game over text to display
    driver.find_element_by_class_name("retry-button").click()

def quit_game():
    time.sleep(1) #lets actually wait for the game over text to display
    driver.quit()

def is_game_over():
    try:
        driver.find_element_by_class_name("game-over")
        return True 
    except NoSuchElementException:
        return False
    

if __name__ == "__main__":
    play_2048()


  
        

    

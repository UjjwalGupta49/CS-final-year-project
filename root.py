import mysql.connector as sql
import uuid
import sys
from game_main import game

gamedb = sql.connect(
  host="localhost",
  user="Ujjwal",
  password="pandaOnMar$",
  database= "game"
)

gamecursor = gamedb.cursor()



def create_user(gamedb= gamedb, gamecursor = gamecursor):
  print("To beign create an account\n")
  name = input("\nEnter your name:\n")
  password = input("Create a password:\n")
  user_id = str(uuid.uuid4())
  query_create_user = "INSERT INTO users (user_id, user, password) VALUES (%s, %s, %s)"
  user_details = (user_id, name, password)
  gamecursor.execute(query_create_user, user_details)
  gamedb.commit()
  print("Account created successfully! Your unique user id is: ", user_id)

def login(gamedb= gamedb, gamecursor = gamecursor):
    global user, password
    user = input("Enter your user name: ")
    password = input("Enter your password: ")
    query_login = "SELECT * FROM users WHERE user = %s AND password = %s"
    login_details = (user, password)
    gamecursor.execute(query_login, login_details)
    data = gamecursor.fetchone()
    if data:
        print("Welcome", user)
        return True
    else:
        print("Invalid login details")
        return False

def start_game():
  gamecursor.execute("ALTER TABLE users DROP COLUMN score")
  gamecursor.execute("ALTER TABLE users ADD score INT DEFAULT 0")
  score = game()
  query_update_score = "UPDATE users SET score = %s WHERE user = %s AND password = %s"
  values = (score, user, password)
  gamecursor.execute(query_update_score, values)
  gamedb.commit()
  query_select_user = "SELECT * FROM users WHERE user = %s AND password = %s"
  values = (user, password)
  gamecursor.execute(query_select_user, values)
  user_data = gamecursor.fetchone()
  print("User details:")
  print("User name:", user_data[1])
  print("Score:", user_data[3])
  print("User ID:", user_data[0])

  gamecursor.execute("ALTER TABLE users DROP COLUMN score")
  gamedb.commit()
  print("Thanks for playing the game!")
  gamedb.close()
  gamedb.close()
  sys.exit()



def main():

    gamecursor.execute('''CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL UNIQUE,
        user VARCHAR(255) NOT NULL,
        password VARCHAR(255) NOT NULL
    )''')

    opt_1 = input("Welcome to the quizler game!\nTo play the game-\n(a) login to your account\n(b) create a new one.\n").lower()
    if (opt_1 == "a"):
      logged_in = login()
    elif (opt_1 == "b"):
      create_user()
      logged_in = login()
    if (logged_in):
      start = input("Do you wnat to start the quiz game?\n(a) Yes\n(b) No\n").lower()
      if (start == "a"):
        start_game()
      else:
        print("Bye!")
        sys.exit()
    else:
      ("Please login to continue")
    

main()




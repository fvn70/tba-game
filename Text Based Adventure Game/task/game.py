username = ''
hero = {'Name': "John", 'Species': "human", 'Gender': "male"}
inventory = {'Snack': "apple", 'Weapon': "sword", 'Tool': "rope"}
difficulty = {'1': "Easy", '2': "Medium", '3': "Hard"}
level = 'Easy'
lives = 5


def menu():
    print('\n***Welcome to the Journey to Mount Qaf***\n')
    print("1- Press key '1' or type 'start' to start a new game")
    print("2- Press key '2' or type 'load' to load your progress")
    print("3- Press key '3' or type 'quit' to quit the game")


def set_hero():
    print("Create your character:")
    hero['Name'] = input('1- Name ').capitalize()
    hero['Species'] = input('2- Species ').capitalize()
    hero['Gender'] = input('3- Gender ').capitalize()


def set_tools():
    print("Pack your bag for the journey:")
    inventory['Snack'] = input('1- Favourite Snack ').capitalize()
    inventory['Weapon'] = input('2- A weapon for the journey ').capitalize()
    inventory['Tool'] = input('3- A traversal tool ').capitalize()


def set_level():
    global level
    global lives
    print("""
Choose your difficulty:
1- Easy
2- Medium
3- Hard""")
    while True:
        lvl = input().lower()
        if lvl in ['1', 'easy']:
            level = 'Easy'
            lives = 5
        elif lvl in ['2', 'medium']:
            level = 'Medium'
            lives = 3
        elif lvl in ['3', 'hard']:
            level = 'Hard'
            lives = 1
        else:
            print("Unknown input! Please enter a valid one.")
            continue
        break


def info():
    print(f"Your character: {hero['Name']}, {hero['Species']}, {hero['Gender']}")
    print(f"Your inventory: {inventory['Snack']}, {inventory['Weapon']}, {inventory['Tool']}")
    print(f"Difficulty: {level}")
    print(f"Number of lives: {lives}")


def start():
    global username
    print("Starting a new game...")
    username = input("Enter a user name to save your progress or type '/b' to go back ")
    if username == '/b':
        print("Going back to menu...")
        return False
    set_hero()
    set_tools()
    set_level()
    print("Good luck on your journey!")
    info()


while True:
    menu()
    cmd = input().lower()
    # if cmd in ['/b']:
    #     print("Going back to menu...")
    #     continue
    if cmd in ['1', 'start']:
        if not start():
            continue
    elif cmd in ['2', 'load']:
        print("No save data found!")
    elif cmd in ['3', 'quit']:
        print("Goodbye!")
        break
    else:
        print("Unknown input! Please enter a valid one.")

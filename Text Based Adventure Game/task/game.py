import json
import re

username = ''
hero = {'Name': "John", 'Species': "human", 'Gender': "male"}
inventory = {'Snack': "apple", 'Weapon': "sword", 'Tool': "rope"}
difficulty = {'1': "Easy", '2': "Medium", '3': "Hard"}

data = {}
scene = 1
level = 1
lives = 5
loop = True


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
            level = 1
            lives = 5
        elif lvl in ['2', 'medium']:
            level = 2
            lives = 3
        elif lvl in ['3', 'hard']:
            level = 3
            lives = 1
        else:
            print("Unknown input! Please enter a valid one.")
            continue
        break


def info():
    print(f"Your character: {hero['Name']}, {hero['Species']}, {hero['Gender']}")
    print(f"Your inventory: {inventory['Snack']}, {inventory['Weapon']}, {inventory['Tool']}")
    print(f"Difficulty: {difficulty[str(level)]}")
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
    return True


def load_data():
    global data
    fn = 'story/story.json'
    try:
        with open(fn, 'r') as fl:
            data = json.load(fl)
    except Exception:
        print(f"File {fn} not found")


def help():
    print("""
Type the number of the option you want to choose.
Commands you can use:
/i => Shows inventory.
/q => Exits the game.
/c => Shows the character traits.
/h => Shows help.
""")


def do_effect(eff):
    global lives, loop, scene
    tasks = eff.split(' and ')
    # print('All tasks:')
    for task in tasks:
        # print(task)
        if 'inventory+' in task:
            key = task[11: -1].capitalize()
            inventory[key] = key
            print(f"A new item has been added to your inventory: {key}")
        elif 'inventory-' in task:
            key = task[11: -1].capitalize()
            inventory.pop(key)
            print(f"An item has been removed from your inventory: {key}")
        elif 'life+1' in task:
            lives += 1
            print(f"You gained an extra life! Lives remaining: {lives}")
        elif 'life-1' in task:
            lives -= 1
            print(f"You died! Lives remaining: {lives}")
        elif 'move' in task:
            if scene < 3:
                scene += 1
            # print(f"Scene - {scene}")
        elif 'save' in task:
            save_game()
        elif 'game_won' in task:
            won_game()


def save_game():
    print('Save game')


def won_game():
    print('You won game!')


def game_loop():
    global loop, level, scene, lives
    scene = 1
    level = 1
    lives = 5

    while True:
        lvl = 'lvl' + str(level)
        scn = 'scene' + str(scene)
        if not data['story'].get(lvl):
            loop = False
            print("Goodbye!")
            return
        print()
        print(data['story'][lvl]['title'])
        if not data['story'][lvl]['scenes']:
            loop = False
            print("Goodbye!")
            return
        print(data['story'][lvl]['scenes'][scn])
        print("\nWhat will you do? Type the number of the option or type '/h' to show help.")
        print(f"1-{data['choices'][lvl][scn]['choice1']}", end='')
        print(f"2-{data['choices'][lvl][scn]['choice2']}", end='')
        print(f"3-{data['choices'][lvl][scn]['choice3']}", end='')
        ch = input()
        if ch in ['1', '2', '3']:
            outcome = 'outcome' + ch
            # print(f"lvl={lvl}, scn={scn}, outcome={outcome}")
            out = data['outcomes'][lvl][scn][outcome]
            if isinstance(out, dict):
                if inventory.get('Key'):
                    opt = 'option1'
                else:
                    opt = 'option2'
                out = out[opt]
            out.strip()
            i = out.find('(')
            j = out.find(')')
            text = out
            to_do = ""
            if i > 0:
                text = out[:i].strip()
                to_do = out[i + 1: j]
            i = text.find('{')
            if i > 0:
                word = text[i + 1: -1].capitalize()
                text = text[: i] + inventory[word]
            # print(out)
            print(text)
            # print(to_do)
            do_effect(to_do)
            if lives == 0:
                print("You've run out of lives! Game over!")
                return  # to main loop
        elif ch == '/i':
            print(f"Inventory: {list(inventory.values())}")
        elif ch == '/c':
            print(f"Your character: {list(hero.values())}")
            print(f"Lives remaining: {lives}")
        elif ch == '/h':
            help()
        elif ch == '/q':
            ch = input("You sure you want to quit the game? Y/N ")
            if ch.lower() == 'y':
                loop = False
                print("Goodbye!")
                return
        else:
            print("Unknown input! Please enter a valid one.")


load_data()
while loop:
    menu()
    cmd = input().lower()
    if cmd in ['1', 'start']:
        if start():
            game_loop()
        else:
            continue
    elif cmd in ['2', 'load']:
        print("No save data found!")
    elif cmd in ['3', 'quit']:
        print("Goodbye!")
        break
    else:
        print("Unknown input! Please enter a valid one.")

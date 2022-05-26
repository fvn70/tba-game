import json
import os

username = ''
char_attrs = {'name': "John", 'species': "human", 'gender': "male"}
inventory = {'snack': "apple", 'weapon': "sword", 'tool': "rope"}

data = {}
difficulty = "Easy"
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
    char_attrs['name'] = input('1- Name ').capitalize()
    char_attrs['species'] = input('2- Species ').capitalize()
    char_attrs['gender'] = input('3- Gender ').capitalize()


def set_tools():
    print("Pack your bag for the journey:")
    inventory['snack'] = input('1- Favourite Snack ').capitalize()
    inventory['weapon'] = input('2- A weapon for the journey ').capitalize()
    inventory['tool'] = input('3- A traversal tool ').capitalize()


def set_level():
    global level, lives, difficulty
    print("""
Choose your difficulty:
1- Easy
2- Medium
3- Hard""")
    while True:
        lvl = input().lower()
        if lvl in ['1', 'easy']:
            difficulty = 'Easy'
            lives = 5
        elif lvl in ['2', 'medium']:
            difficulty = 'Medium'
            lives = 3
        elif lvl in ['3', 'hard']:
            difficulty = 'Hard'
            lives = 1
        else:
            print("Unknown input! Please enter a valid one.")
            continue
        break


def info():
    print(f"Your character: {char_attrs['name']}, {char_attrs['species']}, {char_attrs['gender']}")
    print(f"Your inventory: {inventory['snack']}, {inventory['weapon']}, {inventory['tool']}")
    print(f"Difficulty: {difficulty}")
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


def load_story():
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


def save_game():
    global char_attrs, inventory, level, lives, difficulty, username
    fn = f'game/saves/{username}.json'
    d = {
        "char_attrs": {
            "name": char_attrs['name'],
            "species": char_attrs['species'],
            "gender": char_attrs['gender']
        },
        "inventory": {
            "snack": inventory['snack'],
            "weapon": inventory['weapon'],
            "tool": inventory['tool']
        },
        "lives": lives,
        "difficulty": difficulty,
        "level": level
    }
    with open(fn, 'w') as fl:
        json.dump(d, fl)


def load_file():
    global char_attrs, inventory, level, lives, difficulty, username
    fdir = 'game/saves/'
    fns = os.listdir(fdir)
    fns = [f[: -5] for f in fns if f[-5:] == '.json']
    if fns:
        print("Choose your user name from the list: ")
        print('\n'.join(fns))
        username = input("Type your user name from the list: ")
        fn = fdir + username + '.json'
        try:
            with open(fn, 'r') as fl:
                d = json.load(fl)
                if d:
                    print("Loading your progress...")
                    char_attrs = d['char_attrs']
                    inventory = d['inventory']
                    lives = d['lives']
                    level = d['level']
                    difficulty = d['difficulty']
                    return True
        except Exception:
            found = False
    print("No save data found!")
    return False


def won_game():
    global lives
    print('Congratulations! You beat the game!')
    lives = -1


def do_effect(eff):
    global lives, loop, scene, level
    tasks = eff.split(' and ')
    for task in tasks:
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
            scene = 1
        elif 'move' in task:
            if scene < 3:
                scene += 1
        elif 'save' in task:
            level += 1
            scene = 1
            save_game()
        elif 'game_won' in task:
            won_game()


def game_loop():
    global loop, level, scene, lives

    while True:
        lvl = 'lvl' + str(level)
        scn = 'scene' + str(scene)
        if lives < 0 or not data['story'].get(lvl):
            loop = False
            print("Goodbye!")
            return
        print(data['story'][lvl]['title'])
        if not data['story'][lvl]['scenes'][scn]:
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
            j = text.find('}')
            if i > 0:
                word = text[i + 1: j]
                text = text[: i] + inventory[word]
            print(text)
            do_effect(to_do)
            if lives == 0:
                print("You've run out of lives! Game over!")
                return  # to main loop
        elif ch == '/i':
            print(f"Inventory: {list(inventory.values())}")
        elif ch == '/c':
            print(f"Your character: {list(char_attrs.values())}")
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


load_story()
while loop:
    menu()
    cmd = input().lower()
    if cmd in ['1', 'start']:
        if start():
            game_loop()
    elif cmd in ['2', 'load']:
        if load_file():
            game_loop()
    elif cmd in ['3', 'quit']:
        print("Goodbye!")
        break
    else:
        print("Unknown input! Please enter a valid one.")

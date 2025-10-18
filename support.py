import json
from datetime import datetime, timedelta
import re
import requests

intro = '''Welcome to your personal assistant app!
Choose what you wish to be helped with.
1. Task manager
2. Weather forecast
3. Project manager
4. Schedules
5. News headlines'''

def main():
    print(intro)
    while True:
        user_choice = input('Number: ').strip()
        if user_choice not in ['1', '2', '3', '4', '5']:
            print('Invalid user choice.')
            return
        elif user_choice == '1':
            task_manager()
        elif user_choice == '2':
            weather_app()
        elif user_choice == '3':
            project_manager()
        elif user_choice == '4':
            schedules_handler()
        elif user_choice == '5':
           news_headline()

        again = input('Go again?(y/n): ').lower().strip()
        if again != 'y':
            break

tasks = []

try:
    with open('C:\\Users\\User\\Desktop\\website\\tasks.json', 'r') as file:
        content = file.read().strip()
        if content:
            tasks = json.loads(content)
        else:
            tasks = []
except FileNotFoundError:
    tasks = []

def save_file():
    with open('C:\\Users\\User\\Desktop\\website\\tasks.json', 'w') as file:
        json.dump(tasks, file, indent=4)

def task_manager():
    options = '''Welcome to the task management app. Please choose what you wish to do(insert only the number)
1. Add task
2. View task
3. Remove task
4. Add due date
5. Edit task
6. Filter tasks based on a category
7. Query'''

    while True:
        print(options)
        print()
        choice = input('Insert your choice: ').lower().strip()
        if choice not in ['1', '2', '3', '4', '5', '6', '7']:
            print('Please insert one of the numbers.')
            return
        else:
            break

    if choice == '1':
        print('Lets begin by writing some data about each task.')
        task_name = input('Task name: ').lower().strip()

        while True:
            task_priority = input('Task priority(high/medium/low): ').lower().strip()
            if task_priority not in ['medium', 'high', 'low']:
                print('Please enter a valid input')
                return
            else:
                break
       
        while True:
            task_status = input('Task status(finished/unfinished): ').lower().strip()
            if task_status not in ['finished', 'unfinished']:
                print('Please enter a valid option.')
                return
            else:
                break

        tasks.append({
            'task_name': task_name,
            'task_status': task_status,
            'task_priority': task_priority,
            'due_date': None
            })
        
        save_file()

        print(f'{task_name} was added successfully.')

    if choice == '2':
        if not tasks:
            print('Task list is empty.')
            return
        else:
            for i, task in enumerate(tasks):
                print(f"{i + 1}. {task['task_name']}, status: {task['task_status']}, priority: {task['task_priority']}, due date: {task['due_date']}")

    if choice == '3':
        try:
            num = int(input('Choose the task you wish to remove: '))
            if num not in range(1, len(tasks) + 1):
                print('Invalid number.')
                return
        except ValueError:
            print('You must enter a number.')

        tasks.remove(tasks[num - 1])

        save_file()
        print('Task removed successfully.')

    if choice == '4':
        if not tasks:
            print('No tasks yet.')
            return
        try:
            num = int(input('Choose the task you wish to edit: '))
            if num not in range(1, len(tasks) + 1):
                print('Invalid number.')
                return
        except ValueError:
            print('You must enter a number.')
   
        datestr = input('Insert the due date(DD-MM-YYYY): ')
        if not re.search(r'\d{2}-\d{2}-\d{4}', datestr):
            print('Invalid format.')
        else:
            try:
                date = datetime.strptime(datestr, '%d-%m-%Y')
            except ValueError:
                print('Invalid format.')
                return
            tasks[num - 1]['due_date'] = date.strftime('%d-%m-%Y')
            print('Due date added successfully!')

        save_file()          
   
    if choice == '5':
        if not tasks:
            print('No tasks yet.')
            return
        try:
            num = int(input('Choose the task you wish to edit: '))
            if num not in range(1, len(tasks) + 1):
                print('Invalid number.')
                return
        except ValueError:
            print('You must enter a number.')
        
        category_to_edit = input('Choose which category do you wish to change(name/status/priority/date): ').lower().strip()
        if category_to_edit not in ['name', 'status', 'priority', 'date']:
            print('Invalid input, category does not exist.')
        else:
            new = input('What you want to insert: ')
            if category_to_edit == 'name':
                tasks[num - 1]['task_name'] = new
            elif category_to_edit == 'status':
                if new not in ['finished', 'unfinished']:
                    print('Invalid choice.')
                else:
                    tasks[num - 1]['task_status'] = new
            elif category_to_edit == 'priority':
                if new not in ['low', 'medium', 'high']:
                    print('Invalid choice: ')
                else:
                    tasks[num - 1]['task_priority'] = new
            elif category_to_edit == 'date':
                if not re.search(r'\d{2}-\d{2}-\d{4}', new):
                    print('Invalid format.')
                else:
                    try:
                        new_date = datetime.strptime(new, '%d-%m-%Y')
                    except ValueError:
                        print('Invalid format.')
                    tasks[num - 1]['due_date'] = new_date.strftime('%d-%m-%Y')

            save_file()

        print('Task updated successfully.')
    if choice == '6':
        category = input('Choose the category you wish to filter your tasks based on(priority/status/due): ').lower().strip()
        subcat = input('What do you want to see?(mini categories or due date): ').lower().strip()

        if category not in ['priority', 'status', 'due']:
            print('Category not available.')
        elif category == 'priority':
            if subcat not in ['low', 'medium', 'high']:
                print('Type an existing category.')
                return
        elif category == 'status':
            if subcat not in ['finished', 'unfinished']:
                print('Type an existing category.')
                return
        else:
            if not re.search(r'\d{2}-\d{2}-\d{4}', subcat):
                print('Invalid date format.')
                return
        keys = {
            'priority': 'task_priority',
            'status': 'task_status',
            'due': 'due_date'
        }

        key = keys.get(category)

        for task in tasks:
            if task[key] == subcat:
                print(f"{task['task_name']}, status: {task['task_status']}, priority: {task['task_priority']}, due date: {task['due_date']}")

    if choice == '7':
        found = False
        query = input('Search bar - search through a keyword: ').lower().strip()
        for task in tasks:
            if query in task['task_name']:
                print(f"{task['task_name']}, status: {task['task_status']}, priority: {task['task_priority']}, due date: {task['due_date']}")
                found = True
        if not found:
            print('Nothing found.')

    print('--------')
    print('Important reminders!')
    today = datetime.today().date() 
    found = False
    for task in tasks:
        if not task['due_date']:
            continue

        due = datetime.strptime(task['due_date'], '%d-%m-%Y').date()
        left = (due - today).days
       
        if 0 <= left <= 1:
            print(f"Due date for {task['task_name'].capitalize()} is approaching soon.")
            found = True
    if not found:
        print('No deadlines soon.')

def weather_app():
    print('Welcome to the weather forecast.')
    city = input('Choose the city you want to be informed on: ').capitalize().strip()
    key = '59417eb0b2b2f497f5606a63dc4ac337'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric'

    response = requests.get(url)
    data = response.json()
    
    name = data['name']
    country = data['sys']['country']
    condition = data['weather'][0]['main']
    description = data['weather'][0]['description']
    temp = data['main']['temp']
    temp_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind = data['wind']['speed']
    max_temp = data['main']['temp_max']
    min_temp = data['main']['temp_min']
    clouds = data['clouds']['all']

    print(f'Weather forecast for {name} in {country}')
    print(f'Weather: {condition}, {description}')
    print(f'Temperature: {temp}°C, which feels like {temp_like}°C')  
    print(f'Maximum temperature: {max_temp}°C and minimum temperature: {min_temp}°C')
    print(f'Humidity: {humidity}')
    print(f'Wind speed: {wind}')
    print(f'Cloudiness: {clouds}')

projects = []

try: 
    with open('C:\\Users\\User\\Desktop\\website\\projects.json', 'r') as file:
        projects = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    projects = []

def save_projects():
    with open('C:\\Users\\User\\Desktop\\website\\projects.json', 'w') as file:
        json.dump(projects, file, indent=4)

class Project:
    def __init__(self, name, priority, deadline, details):
        self.name = name
        self.priority = priority
        self.deadline = deadline
        self.details = details   

    def add_project(self):
        projects.append({
            'name': self.name,
            'priority': self.priority,
            'deadline': self.deadline,
            'description': self.details
        })
        
def project_manager():
    menu = '''Welcome to your Project Manager app. Choose what you wish to do(only insert the number): 
1. Add project
2. View projects
3. Remove project
4. View projects for a specific month
5. Query'''
    while True:
        print(menu)
        print()
        num = input('Select the number: ').strip()
        if num not in ['1', '2', '3', '4', '5']:
            print('Invalid choice.')
            return 
        else:
            break
    
    if num == '1':
        name = input('Project name: ').lower().strip()

        while True:
            priority = input('Enter priority(low/medium/high): ').lower().strip()
            if priority not in ['low', 'medium', 'high']:
                print('Invalid choice')
                return
            else:
                break

        while True:
            deadline = input('Enter the project deadline(DD-MM-YYYY): ').strip()
            if not re.match(r'\d{2}-\d{2}-\d{4}', deadline):
                print('Invalid format.')
                return 
            else:
                break

        description = input('Description: ').lower().strip()

        new_project = Project(name, priority, deadline, description)

        new_project.add_project()
        save_projects()

    if num == '2':
        if not projects:
            print('No projects yet.')
            return
        for i, p in enumerate(projects):
            print(f"{i + 1}. {p['name']}, priority: {p['priority']}, deadline: {p['deadline']}")
            print(f"Additional description: {p['description']}")

    if num == '3':
        if not projects:
            print('No projects yet')
        
        try: 
            choice = int(input('Choose the project you wish to remove(its number): '))
            if choice not in range(1, len(projects) + 1):
                print('Invalid choice.')
                return
        except ValueError:
            print('Invalid choice!')
            return
        
        projects.pop(choice - 1)
        print('Project deleted successfully.')
        save_projects()

    if num == '4':
        mth = input('Insert the month(MM-YYYY): ').lower() 
        found = False
        for p in projects:
            if p['deadline'][3:10] == mth:
                print(f"{p['name']}, priority: {p['priority']}, deadline: {p['deadline']}")
                print(f'Additional description: {p['description']}')
                print()
                found = True
        if not found:
            print('No projects match.')

    if num == '5':
        found = False
        query = input('Search bar - search a keyword: ').lower().strip()
        for p in projects:
            if query in p['name']:
                print(f"{p['name']}, priority: {p['priority']}, deadline: {p['deadline']}")
                found = True
        if not found:
            print('No projects found.')

    print('----------')
    print('Reminders for tomorrow.')
    now = datetime.today().date()
    found = False
    for pr in projects:
        due = datetime.strptime(pr['deadline'], '%d-%m-%Y').date()
        left = (due - now).days

        if 0 <= left <= 1:
            print(f"Deadline is coming soon for {pr['name']}.")
            found = True
    if not found:
        print('No projects soon.') 

schedules = []
try: 
    with open('C:\\Users\\User\\Desktop\\website\\schedules.json', 'r') as file:
        schedules = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    schedules = []

def save_schedules():
    with open('C:\\Users\\User\\Desktop\\website\\schedules.json', 'w') as file:
        json.dump(schedules, file, indent=4)

class Schedule:
    def __init__(self, name, date, start_time, end_time, location):
        self.name = name
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.location = location

    def add_schedule(self):
        schedules.append({
            'name': self.name,
            'date': self.date,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'location': self.location
            })  
              
def schedules_handler():
    menu = '''Welcome to the schedule handler app. Here you can: 
1. Add schedules
2. View all schedules
3. Delete schedules
4. Specific date schedules
5. Query'''
    print(menu)
    choice = input('Choose what you wish to do(one number): ').strip()
    if choice not in ['1', '2', '3', '4', '5']:
        print('Invalid choice.')
        return
    elif choice == '1':
        name = input('Event name: ').lower().strip()
    
        while True:
            date = input('Event date(DD-MM-YYYY): ').strip()
            if not re.match(r'\d{2}-\d{2}-\d{4}', date):
                print('Wrong format.')
                return
            else:
                break
    
        while True:
            start_time = input('Time when event starts(24 hour system): ').strip()
            if not re.match(r'^(?:[0-1]\d|2[0-3]):[0-5][0-9]$', start_time): 
                print('Wrong format.')
                return
            else:
                break

        while True:
            end_time = input('Time when the event ends(24 hour system): ').strip()
            if not re.match(r'^(?:[0-1]\d|2[0-3]):[0-5][0-9]$', end_time):
                print('Invalid format.')
                return
            else:
                break

        location = input('Where is the event taking place: ').lower().strip() 

        new_schedule = Schedule(name, date, start_time, end_time, location)   
        new_schedule.add_schedule()
        save_schedules()

    elif choice == '2':
        if not schedules:
            print('No schedules yet.')
            return
            
        for i, s in enumerate(schedules):
            print(f"{i + 1}. {s['name'].title()}, on {s['date']}, {s['start_time']}-{s['end_time']} in {s['location'].title()}")

    elif choice == '3':
        if not schedules:
            print('No schedules yet.')
            return

        chc = int(input('Choose which schedule do you want to delete: ').strip())
        if chc < 1 or chc > len(schedules):
            print('Invalid number.')
            return
        schedules.pop(chc - 1)
        save_schedules()
        print('Schedule deleted successfully.')

    elif choice == '4':
        dt = input('Which dates schedules do you wish to see(DD-MM-YYYY): ').strip()
        if not re.match(r'\d{2}-\d{2}-\d{4}', dt):
            print('Invalid format.')
            return
        found = False
        for s in schedules:
            if s['date'] == dt:
                print(f"{s['name'].title()}, on {s['date']}, {s['start_time']}-{s['end_time']} in {s['location'].title()}")
                found = True
        if not found:
            print('No schedule found.')

    elif choice == '5':
        found = False
        query = input('Search bar - search a keyword: ').lower().strip()
        for s in schedules:
            if query in s['name']:
                print(f"{s['name'].title()}, on {s['date']}, {s['start_time']}-{s['end_time']} in {s['location'].title()}")
                found = True
        if not found:
            print('No schedules found.')

    print('--------')
    print('Reminders for tomorrow.')
    now = datetime.today().date()
    found = False
    for sch in schedules:
        date = datetime.strptime(sch['date'], '%d-%m-%Y').date()
        left = (date - now).days

        if 0 <= left <= 1:
            print(f"{sch['name']} is coming soon.")
            found =  True
    if not found:
        print('Nothing scheduled up to now.')

def news_headline():
    news_categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']

    print('Welcome to the news app. You can see here the main news headlines.')
    print('Valid country codes: us/gb/de/fr.')

    country = input('Choose one of the countries: ').lower().strip()
    key = '713dcd01d5ee47b3817e76d0aa21f149'
    if country not in ['us', 'gb', 'de', 'fr']:
        print('Choice not supported.')
        return
    
    for cat in news_categories:
        print(cat + ' |', end='')
    category = input('Choose a category from the ones listed below: ')
    
    if category not in news_categories:
        print('Category unavailable.')
        return
    url = f'https://newsapi.org/v2/top-headlines?country={country}&category={category}&apiKey={key}'
   
    response = requests.get(url)
    data = response.json()

    if data['status'] != 'ok' or not data['articles']:
        print('No articles available for the moment.')
        return

    for i, article in enumerate (data['articles']):
        title = article.get('title', 'Unknown')
        source = article['source'].get('name', 'Unknown')
        url = article.get('url', 'Not available.')
        
        print(f"{i + 1}. {title}")
        print(f"Source: {source}")
        print(f"Read more: {url}")
        print()

if __name__ == '__main__':
    main() 
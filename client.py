import requests
import json
import getpass

BASE_URL = "http://127.0.0.1:8000"  # change this URL when deploying
TOKEN = None
SESSION = requests.Session()

# command line interface for user input
def command_loop():
    print("\n===== Professor Rating (Command Line Interface) =====")
    print("Type a command or 'help' for a list of available commands.")

    while True:
        command = input("\n>>> ").strip().split()  # Read input and split into parts

        if not command:
            continue

        action = command[0].lower()

        if action == "register":
            register()
        elif action == "login":
            if len(command) < 2:
                print("Usage: login <url>")
            else:
                login(command[1])
        elif action == "logout":
            if TOKEN is None:
                print("You are not logged in.")
            else:
                logout()
        elif action == "list":
            list_modules()
        elif action == "view":
            view_ratings()
        elif action == "average":
            if len(command) < 3:
                print("Usage: average <professor_id> <module_code>")
            else:
                get_professor_average(command[1], command[2])
        elif action == "rate":
            if TOKEN is None:
                print("You must be logged in to rate a professor.")
            elif len(command) < 6:
                print("Usage: rate <professor_id> <module_code> <year> <semester> <rating>")
            else:
                rate_professor(command[1], command[2], command[3], command[4], command[5])
        elif action == "exit":
            print("Exiting...")
            break
        elif action == "help":
            print("\nAvailable Commands:")
            print("'register' - Register a new user")
            print("'login <url>' - Login to server URL")
            print("'logout' - Logout")
            print("'list' - View module instances & professors")
            print("'view' - View all professor ratings")
            print("'average <professor_id> <module_code>' - View average rating of a professor in a module")
            print("'rate <professor_id> <module_code> <year> <semester> <rating>' - Rate a professor")
            print("'exit' - Exit the application")
        else:
            print("Invalid command. Type 'help' for a list of commands.")


# register
def register():
    print("\n===== Register User =====")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    email = input("Enter email: ")

    data = {
        "username": username,
        "password": password,
        "email": email
    }

    response = requests.post(f"{BASE_URL}/register/", json=data)
    result = response.json()

    if response.status_code == 201:
        print("User registered successfully!")
    else:
        print("Registration failed:", result.get("error", "Unknown error"))


# login
def login(url):
    global TOKEN, BASE_URL
    BASE_URL = url  

    print(f"\n===== Logging in to {BASE_URL} =====")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    data = {"username": username, "password": password}
    response = requests.post(f"{BASE_URL}/login/", json=data)
    result = response.json()

    if response.status_code == 200:
        print("Login successful!")
        TOKEN = result.get("token")  
    else:
        print("Login failed:", result.get("error", "Unknown error"))


# logout
def logout():
    global TOKEN  

    if TOKEN is None:
        print("You are not logged in.")
        return

    headers = {"Authorization": f"Token {TOKEN}"}
    response = SESSION.post(f"{BASE_URL}/logout/", headers=headers)
    result = response.json()

    if response.status_code == 200:
        print("Logout successful!")
        TOKEN = None  # clear token
        SESSION.cookies.clear()  # clear session cookies
        SESSION.headers.pop("X-CSRFToken", None)  # remove CSRF token
    else:
        print("Logout failed:", result.get("error", "Unknown error"))


# list all module instances
def list_modules():
    print("\n===== List of Module Instances =====")

    headers = {"Authorization": f"Token {TOKEN}"} if TOKEN else {}
    response = requests.get(f"{BASE_URL}/list/", headers=headers)

    if response.status_code == 200:
        module_instances = response.json()
        
        if module_instances:
            for module in module_instances:
                print(f"\n- {module['module_code']}, {module['module_name']} | Year: {module['year']}, Semester: {module['semester']}")
                print("  Taught by:")
                
                if module["professors"]:
                    for professor in module["professors"]:
                        print(f"  - Professor {professor['name']} (ID: {professor['code']})")
                else:
                    print("  - No professors assigned.")
        else:
            print("No module instances found.")
    else:
        print("Error retrieving module instances:", response.json())


# view all professor ratings
def view_ratings():
    print("\n===== View List of Professor Ratings =====")
    response = requests.get(f"{BASE_URL}/view/")

    if response.status_code == 200:
        ratings = response.json()
        if ratings:
            for rating in ratings:
                print(f"\n- Professor {rating['professor__name']} (ID: {rating['professor__code']}) has an average rating of {rating['avg_rating']}")        
        else:
            print("No ratings found.")
    else:
        print("Error retrieving ratings:", response.json())


# average rating for professors
def get_professor_average(professor_code=None, module_code=None):

    print("\n===== Professor Module Average Rating =====")

    if professor_code is None:
        professor_code = input("Enter professor ID (eg. JE1): ")
    if module_code is None:
        module_code = input("Enter module code (eg. CD1): ")

    response = requests.get(f"{BASE_URL}/average/{professor_code}/{module_code}/")

    if response.status_code == 200:
        data = response.json()

        if "average_rating" in data and data["average_rating"] is not None:
            professor_name = f"Professor {data.get('professor_name', professor_code)} ({professor_code})"
            module_name = f"module {data.get('module_name', module_code)} ({module_code})"
            avg_rating = round(data["average_rating"]) 
            print(f"\n{professor_name} in {module_name} has an average rating of {avg_rating}.")
        else:
            print("No ratings found for this professor in this module.")
    else:
        print("Error retrieving average rating:", response.json())


# rate professor
def rate_professor(professor_code=None, module_code=None, year=None, semester=None, rating=None):
    global TOKEN
    print("\n===== Rate a Professor =====")

    if TOKEN is None:
        print("You must be logged in to rate a professor.")
        return

    headers = {"Authorization": f"Token {TOKEN}"}
    data = {
        "professor_id": professor_code,
        "module_code": module_code,
        "year": int(year),
        "semester": int(semester),
        "rating": int(rating)
    }

    response = requests.post(f"{BASE_URL}/rate/", json=data, headers=headers)
    result = response.json()

    if response.status_code == 201:
        print("Rating submitted successfully!")
    else:
        print("Error submitting rating:", result.get("error", "Unknown error"))


if __name__ == "__main__":
    command_loop()

I. Instructions on using the client application on the command line interface (CLI)
1. Upon running client.py, you are prompted with:

===== Professor Rating (Command Line Interface) =====
Type a command or 'help' for a list of available commands.

2. Input 'help' and press Enter to list available commands (the prompt will look like this):

Available Commands:
'register' - Register a new user
'login <url>' - Login to url (domain address) 
'logout' - Logout
'list' - View module instances & professors
'view' - View all professor ratings
'average <professor_id> <module_code>' - View average rating of a professor in a module
'rate <professor_id> <module_code> <year> <semester> <rating>' - Rate a professor
'exit' - Exit the application

3. Input the commands to run it.


II. The name of your pythonanywhere domain.
https://sc23ysl.pythonanywhere.com


III. The password instructors must use to login to the admin account on your service.
username: admin
password: adminpw123


IV. Any other information instructors need to know in order to use your client.
- Users can input 'login', 'average', 'rate' and the command line will prompt the proper usage, (eg. Usage: average <professor_id> <module_code>)
- Users must be logged in to rate a professor
- Users can only log out if they are logged in
- Guest users (not logged in) can use the following commands: 'register', 'login', 'list', 'view', 'average' and 'exit'

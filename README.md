# Background Context
## Welcome to the Tongify clone project!

First step: A command interpreter to manage the project's objects.
This is the first step towards building Tongify. This first step is very important because I will use what I build during this project with all other following projects: HTML/CSS templating, database storage, API, front-end integration…

After this phase I will accomplish:

1. put in place a parent class (called BaseModel) to take care of the initialization, serialization and deserialization of the future instances
2. create a simple flow of serialization/deserialization: Instance <-> Dictionary <-> JSON string <-> file
3. create all classes used for Tongify (User, vaccum, ..) that inherit from BaseModel
4. create the first abstracted storage engine of the project: File storage.
5. create all unittests to validate all our classes and storage engine

## What’s a command interpreter?
I want to be able to manage the objects of the project from my own CMD without the need to have any UI:

- Create a new object (ex: a new User or a new Vacuum)
- Retrieve an object from a file, a database etc…
- Do operations on objects (count, compute stats, etc…)
- Update attributes of an object
- Destroy an object


## General Use
First clone this repository.

Once the repository is cloned locate the "console.py" file and run it as follows:

````bash
/tongify$ ./console.py
````
When this command is run the following prompt should appear:
```bash
(tongify)
```
This prompt designates you are in the "tongify" console. There are a variety of commands available within the console program.

### Commands
* create - Creates an instance based on given class

* destroy - Destroys an object based on class and UUID

* show - Shows an object based on class and UUID

* all - Shows all objects the program has access to, or all objects of a given class

* update - Updates existing attributes an object based on class name and UUID

* quit - Exits the program (EOF will as well)

## Alternative Syntax
Users are able to issue a number of console command using an alternative syntax:

```bash
Usage: <class_name>.<command>([<id>[name_arg value_arg]|[kwargs]])
```
Advanced syntax is implemented for the following commands:

* all - Shows all objects the program has access to, or all objects of a given class

* count - Return number of object instances by class

* show - Shows an object based on class and UUID

* destroy - Destroys an object based on class and UUID

* update - Updates existing attributes an object based on class name and UUID

## Examples
### Primary Command Syntax
*Example 0: Create an object*
Usage: create <class_name>

```bash
(tongify) create BaseModel
3aa5babc-efb6-4041-bfe9-3cc9727588f8
(tongify)                   
```
*Example 1: Show an object*
Usage: show <class_name> <_id>

```bash
(tongify) show BaseModel 3aa5babc-efb6-4041-bfe9-3cc9727588f8
[BaseModel] (3aa5babc-efb6-4041-bfe9-3cc9727588f8) {'id': '3aa5babc-efb6-4041-bfe9-3cc9727588f8', 'created_at': datetime.datetime(2020, 2, 18, 14, 21, 12, 96959), 
'updated_at': datetime.datetime(2020, 2, 18, 14, 21, 12, 96971)}
(tongify)  
```
*Example 2: Destroy an object*
Usage: destroy <class_name> <_id>

```bash
(tongify) destroy BaseModel 3aa5babc-efb6-4041-bfe9-3cc9727588f8
(tongify) show BaseModel 3aa5babc-efb6-4041-bfe9-3cc9727588f8
** no instance found **
(tongify)   
```
*Example 3: Update an object*
Usage: update <class_name> <_id>

```bash
(tongify) update BaseModel b405fc64-9724-498f-b405-e4071c3d857f first_name "person"
(tongify) show BaseModel b405fc64-9724-498f-b405-e4071c3d857f
[BaseModel] (b405fc64-9724-498f-b405-e4071c3d857f) {'id': 'b405fc64-9724-498f-b405-e4071c3d857f', 'created_at': datetime.datetime(2020, 2, 18, 14, 33, 45, 729889), 
'updated_at': datetime.datetime(2020, 2, 18, 14, 33, 45, 729907), 'first_name': 'person'}
(tongify)
```

# Authors
Mokhtar M. Ramadan - [GitHub](https://github.com/mokhtarmramadan "GitHub") - [Email](mailto:mokhtarramdanformal@gmail.com "Email")
©All rights reserved

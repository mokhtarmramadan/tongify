#!/usr/bin/python3
''' contains the entry point of the command interpreter '''
import models
from models.base_model import BaseModel
from models.user import User
from models.post import Post
import cmd
import sys
import re
from shlex import split


def parse(input_string):
    "Parsing input"
    curly_braces = re.search(r"\{(.*?)\}", input_string)
    brackets = re.search(r"\[(.*?)\]", input_string)
    if curly_braces is None:
        if brackets is None:
            return [item.strip(",") for item in split(input_string)]
        else:
            lexer = split(input_string[:brackets.span()[0]])
            ret_list = [item.strip(",") for item in lexer]
            ret_list.append(brackets.group())
            return ret_list
    else:
        lexer = split(input_string[:curly_braces.span()[0]])
        ret_list = [item.strip(",") for item in lexer]
        ret_list.append(curly_braces.group())
        return ret_list
    

def split_check(input_str):
    if '=' in input_str:
        attribute, value = input_str.split("=")
        value = value.replace("_", " ")
        try:
            value = int(value)
        except ValueError:
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass
        return attribute, value

    else:
        return None, None


class tongfiyCommand(cmd.Cmd):
    ''' CMD class '''

    prompt = "(tongify) "
    __classes = ['BaseModel', 'User', 'Post']

    def do_quit(self, quit):
        ''' Exists the program'''
        sys.exit()

    def do_EOF(self, EOF):
        ''' Exists the program'''
        sys.exit()

    def do_help(self, arg: str) -> bool | None:
        ''' Comand manual '''
        return super().do_help(arg)

    def do_create(self, className):
        ''' Creates a new instance of BaseModel, saves it
          (to the JSON file) and prints the id'''
        input_list = parse(className)
        if len(input_list) == 0:
            print("** class name missing **")
        elif input_list[0] not in tongfiyCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj = eval(input_list[0])()
            if len(input_list) > 1:                
                for input in input_list:
                    attribute, value = split_check(input)
                    if attribute is not None and value is not None:
                        if hasattr(obj, attribute):
                            setattr(obj, attribute, value)
                print(obj.id)
                obj.save()
            else:
                print(obj.id)
                obj.save()

    def do_show(self, input_str):
        ''' Prints the string representation of an instance
        based on the class name and id'''
        input_list = parse(input_str)
        if len(input_list) == 0:
            print("** class name missing **")
        elif len(input_list) == 1:
            print("** instance id missing **")
        elif input_list[0] not in tongfiyCommand.__classes:
            print("** class doesn't exist **")
        else:
            key = f"{input_list[0]}.{input_list[1]}"
            obj_dict = models.storage.all().get(key, 0)
            if not obj_dict:
                print("** no instance found **")
            else:
                print(obj_dict)

    def do_destroy(self, input_str):
        ''' Deletes an instance based on the class name and id '''
        input_list = parse(input_str)
        if len(input_list) == 0:
            print("** class name missing **")
        elif len(input_list) == 1:
            print("** instance id missing **")
        elif input_list[0] not in tongfiyCommand.__classes:
            print("** class doesn't exist **")
        else:
            key = f"{input_list[0]}.{input_list[1]}"
            obj_dict = models.storage.all().get(key, 0)
            if not obj_dict:
                print("** no instance found **")
            else:
                del models.storage.all()[key]
                models.storage.save()

    def do_all(self, className=None):
        ''' Prints all string representation of all instances
        based or not on the class name'''
        instance_dict = models.storage.all()
        instance_list = []

        if className is not None:
            for k in instance_dict.keys():
                if className in k:
                    instance_list.append(instance_dict[k].__str__())
            print(instance_list)
        else:
            for k in instance_dict.keys():
                instance_list.append(instance_dict[k].__str__())
            print(instance_list)

    def do_update(self, input_str):
        '''  Updates an instance based on the class name and id by adding
          or updating attribute (save the change into the JSON file)'''
        input_list = parse(input_str)
        if len(input_list) == 0:
            print("** class name missing **")
        elif input_list[0] not in tongfiyCommand.__classes:
            print("** class doesn't exist **")
        elif len(input_list) == 1:
            print("** instance id missing **")
        elif len(input_list) == 2:
            print("** attribute name missing **")
        elif len(input_list) == 3:
            print("** value missing **")
        else:
            key = f"{input_list[0]}.{input_list[1]}"
            obj = models.storage.all().get(key, 0)
            if not obj:
                print("** no instance found **")
            else:
                if input_list[2] in obj.__class__.__dict__.keys():
                    val_type = type(obj.__class__.__dict__[input_list[2]])
                    obj.__dict__[input_list[2]] = val_type(input_list[3])
                else:
                    obj.__dict__[input_list[2]] = input_list[3]
                models.storage.save()


if __name__ == '__main__':
    tongfiyCommand().cmdloop()

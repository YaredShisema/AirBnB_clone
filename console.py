#!/usr/bin/env python3
"""
This module contains the console for the AirBnB project.
"""
import cmd
import json
import models
from models.base_model import BaseModel

class HBNBCommand(cmd.Cmd):
    """Command interpreter class."""

    prompt = '(hbnb) '

    def do_create(self, arg):
        """Create a new instance of BaseModel, save it to JSON file, and print the id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in models.classes:
            print("** class doesn't exist **")
            return
        instance = models.classes[class_name]()
        instance.save()
        print(instance.id)

    def do_show(self, arg):
        """Print the string representation of an instance based on the class name and id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in models.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        if key not in models.storage.all():
            print("** no instance found **")
            return
        print(models.storage.all()[key])

    def do_destroy(self, arg):
        """Delete an instance based on the class name and id."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in models.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        if key not in models.storage.all():
            print("** no instance found **")
            return
        del models.storage.all()[key]
        models.storage.save()

    def do_all(self, arg):
        """Print all string representations of all instances or of a specific class."""
        args = arg.split()
        instance_list = []
        if len(args) == 0:
            for obj in models.storage.all().values():
                instance_list.append(str(obj))
        else:
            class_name = args[0]
            if class_name not in models.classes:
                print("** class doesn't exist **")
                return
            for obj in models.storage.all().values():
                if obj.__class__.__name__ == class_name:
                    instance_list.append(str(obj))
        print(instance_list)

    def do_count(self, arg):
        """Count the number of instances of a specific class."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in models.classes:
            print("** class doesn't exist **")
            return
        count = 0
        for obj in models.storage.all().values():
            if obj.__class__.__name__ == class_name:
                count += 1
        print(count)

    def do_update(self, arg):
        """Update an instance based on the class name and id with a dictionary."""
        args = arg.split()
        if len(args) == 0:
            print("** class name missing **")
            return
        class_name = args[0]
        if class_name not in models.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        if key not in models.storage.all():
            print("** no instance found **")
            return
        if len(args) < 3:
            print("** dictionary missing **")
            return
        try:
            dictionary = eval(args[2])
        except (NameError, SyntaxError):
            print("** invalid dictionary **")
            return
        instance = models.storage.all()[key]
        instance_dict = instance.to_dict()
        for k, v in dictionary.items():
            if k in instance_dict:
                if isinstance(v, str):
                    v = v.strip("\"'")
                setattr(instance, k, v)
        instance.save()

    def emptyline(self):
        """Called when an empty line is entered in response to the prompt."""
        pass

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):

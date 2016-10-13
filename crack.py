#!/usr/bin/env python3

#Author: Martin Borek (mborekcz@gmail.com)
#Date: 11/Oct/2016

import sys
import argparse
import traceback
import hashlib
from string import ascii_lowercase
from string import ascii_uppercase
from string import punctuation

class Params:
    def __init__(self):
        self.users = [];
        self.dictionary = [];
        self.constant = "";

    def __del__(self):
        self.cleanup()

    def cleanup(self):
        pass

    def _set_constant(self, constant):
        self.constant = constant

    def _read_users(self, filename):
        '''Reads users file given by filename.'''

        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                values = line.split()
                self.users.append(User(values[0], values[1], values[2]))

    def _read_dictionary(self, filename):
        '''Reads dictionary file given by filename.'''

        with open(filename, "r", encoding="utf-8",errors='ignore') as file:
            for line in file:
                self.dictionary.append(line.strip())

    def _print_help(self):
        print('''Password Cracker
Usage:
    password_cracker.py --users users.txt --dictionary dictionary.txt --constant "constant"
    --users List of users; each line consisting of name, salt (hexa) and password hash (hexa, 32 characters)
    --dictionary File with words on separate lines
    --constant Constant; text prepended to a password before computing its hash''')

    def get_args(self):
        '''Parses given arguments.'''

        try:
            arg_parser = argparse.ArgumentParser()
            #arg_parser = argparse.ArgumentParser(add_help=False)
            arg_parser.add_argument("--users")
            arg_parser.add_argument("--dictionary")
            arg_parser.add_argument("--constant")
            args = arg_parser.parse_args()
        except:
            raise OtherError("Wrong argument(s) entered")

        if len(sys.argv) == 1:
            self._print_help()
            exit(1)
        elif len(sys.argv) > 7 or args.users is None or args.dictionary is None:
            raise OtherError("Incorrect arguments");
        else:
            self._read_users(args.users)
            self._read_dictionary(args.dictionary)
            if args.constant is not None:
                self._set_constant(args.constant)

class User:
    def __init__(self, name, salt, hashed):
        self.name = name
        self.salt = salt
        self.hashed = hashed
        self.password = None

'''Definition of Error classes:''' 
class OtherError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Cracker:
    def __init__(self, dictionary, constant):
        self.dictionary = dictionary
        self.constant = constant

    #def _get_hash(self, string):
    #    return (string.)).hexdigest()[:32]

    def crack_user(self, user):
        for word in self.dictionary:
            #print(word)
            if hashlib.sha256((self.constant + word + user.salt).encode('utf-8')).hexdigest()[:32] == user.hashed:
                return word
            #hashed = self._get_hash(self.constant + word + user.salt)
            #krint(word + ':' + hashed + ':' + user.hashed)
            #if hashed == user.hashed:
        return None

def lower(dictionary):
    return [x.lower() for x in dictionary]

def upper(dictionary):
    return [x.upper() for x in dictionary]

def append(dictionary, i):
    return [x + str(i) for x in dictionary]

def prepend(dictionary, i):
    return [str(i) + x for x in dictionary]

def reverse(dictionary):
    return [x[::-1] for x in dictionary]

def duplicate(dictionary):
    return [x+x for x in dictionary]

def reflect(dictionary):
    return [x+x[::-1] for x in dictionary]

def reflect_reverse(dictionary):
    return [x[::-1]+x for x in dictionary]

def title(dictionary):
    return [x.title() for x in dictionary]

def capitalize(dictionary):
    return [x.capitalize() for x in dictionary]

def n_capitalize(dictionary):
    return [x[0].lower()+x[1:].upper() for x in dictionary]

def delete_first(dictionary):
    return [x[1:] for x in dictionary]

def delete_last(dictionary):
    return [x[:-1] for x in dictionary]

def no_dash(dictionary):
    return [x.replace('-', ' ') for x in dictionary]

def replace_el(dictionary):
    d = [x.replace('e', '3') for x in dictionary]
    return  [x.replace('l', '1') for x in d]

def replace_as(dictionary):
    d = [x.replace('a', '@') for x in dictionary]
    return  [x.replace('s', '$') for x in d]

def toggle_case(dictionary):
    toggle = lambda s: "".join((str.upper,str.lower)[i%2](ch) for i,ch in enumerate(s))
    return [toggle(x) for x in dictionary]

def toggle_case2(dictionary):
    toggle = lambda s: "".join((str.lower,str.upper)[i%2](ch) for i,ch in enumerate(s))
    return [toggle(x) for x in dictionary]

def capitalize_x(dictionary, position):
    return [x[:position].lower() + x[position:].capitalize() for x in dictionary]


def main():
    '''MAIN PROGRAM'''

    err_code = 0
    try:
        params = Params()
        params.get_args()
        print("Constant: " + params.constant)


        print("starting")
        cracker = Cracker(params.dictionary, params.constant)
        for user in params.users:
            if user.password is not None:
                continue
            password = cracker.crack_user(user)

            if password is not None:
                print(user.name + ": " + password)
                user.password = password



        step = 0
        upperCase = False
        default_dictionary = lower(params.dictionary)
        while step < 18:

            print("Step:" + str(step))
            if step == 0:
                altered_dictionary = params.dictionary
            elif step == 1:
                altered_dictionary = upper(params.dictionary)
            elif step == 2:
                altered_dictionary = lower(params.dictionary)
            elif step == 3:
                altered_dictionary = toggle_case(params.dictionary)
            elif step == 4:
                altered_dictionary = toggle_case2(params.dictionary)
            elif step == 5:
                altered_dictionary = title(params.dictionary)
            elif step == 6:
                altered_dictionary = capitalize(params.dictionary)
            elif step == 7:
                altered_dictionary = n_capitalize(params.dictionary)


            elif step == 8:
                altered_dictionary = duplicate(default_dictionary)
            elif step == 9:
                altered_dictionary = reverse(default_dictionary)
            elif step == 10:
                altered_dictionary = reflect_reverse(default_dictionary)
            elif step == 11:
                altered_dictionary = reflect(default_dictionary)
            elif step == 12:
                altered_dictionary = delete_first(default_dictionary)
            elif step == 13:
                altered_dictionary = delete_last(default_dictionary)
            elif step == 14:
                altered_dictionary = no_dash(default_dictionary)
            elif step == 15:
                altered_dictionary = replace_el(default_dictionary)
            elif step == 16:
                altered_dictionary = replace_as(default_dictionary)
            elif step == 17:
                altered_dictionary = replace_as(default_dictionary)
                altered_dictionary = replace_el(altered_dictionary)
                if upperCase is not True:
                    upperCase = True
                    default_dictionary = upper(params.dictionary)
                    print("Now uppercase")
                    step = 7 # Go from step 8 again with upper case


            step += 1 
            cracker = Cracker(altered_dictionary, params.constant)
            for user in params.users:
                if user.password is not None:
                    continue
                password = cracker.crack_user(user)

                if password is not None:
                    print(user.name + ": " + password)
                    user.password = password

        print("Appending and prepending characters")
        big_step = 1
        while big_step < 3:
            if big_step == 1:
                print("lower")
                default_dictionary = lower(params.dictionary)
            elif big_step == 2:
                print("upper")
                default_dictionary = upper(params.dictionary)

            big_step += 1 
            for i in ascii_uppercase:
                print(i)
                step = 1
                while step < 3:
                    if step == 1:
                        altered_dictionary = append(default_dictionary, i)
                        step += 1
                    elif step == 2:
                        altered_dictionary = prepend(default_dictionary, i)
                        step += 2

                    cracker = Cracker(altered_dictionary, params.constant)
                    for user in params.users:
                        if user.password is not None:
                            continue
                        password = cracker.crack_user(user)

                        if password is not None:
                            print(user.name + ": " + password)
                            user.password = password

            for i in punctuation:
                print(i)
                step = 1
                while step < 3:
                    if step == 1:
                        altered_dictionary = append(default_dictionary, i)
                        step += 1
                    elif step == 2:
                        altered_dictionary = prepend(default_dictionary, i)
                        step += 2

                    cracker = Cracker(altered_dictionary, params.constant)
                    for user in params.users:
                        if user.password is not None:
                            continue
                        password = cracker.crack_user(user)

                        if password is not None:
                            print(user.name + ": " + password)
                            user.password = password


            for i in ascii_lowercase:
                print(i)
                step = 1
                while step < 3:
                    if step == 1:
                        altered_dictionary = append(default_dictionary, i)
                        step += 1
                    elif step == 2:
                        altered_dictionary = prepend(default_dictionary, i)
                        step += 2

                    cracker = Cracker(altered_dictionary, params.constant)
                    for user in params.users:
                        if user.password is not None:
                            continue
                        password = cracker.crack_user(user)

                        if password is not None:
                            print(user.name + ": " + password)
                            user.password = password

            for i in range(0,100):
                print(i)
                step = 1
                while step < 3:
                    if step == 1:
                        altered_dictionary = append(default_dictionary, i)
                        step += 1
                    elif step == 2:
                        altered_dictionary = prepend(default_dictionary, i)
                        step += 2

                    cracker = Cracker(altered_dictionary, params.constant)
                    for user in params.users:
                        if user.password is not None:
                            continue
                        password = cracker.crack_user(user)

                        if password is not None:
                            print(user.name + ": " + password)
                            user.password = password

        print("Capitalizing")
        for i in range(0,12):
            print(i)
            altered_dictionary = capitalize_x(params.dictionary, i)

            cracker = Cracker(altered_dictionary, params.constant)
            for user in params.users:
                if user.password is not None:
                    continue
                password = cracker.crack_user(user)

                if password is not None:
                    print(user.name + ": " + password)
                    user.password = password



        for user in params.users:
            if user.password is None:
                print(user.name + ": Password not cracked")
        
    except OtherError as e:
        sys.stderr.write(e.value + "\n")
        err_code = 1

    except Exception as e:
        sys.stderr.write(traceback.format_exc())
        err_code = 2
    finally:
        params.cleanup()
        exit(err_code)

main()

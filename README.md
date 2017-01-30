# Password cracker
Simple password cracker implemented in Python.

Author: Martin Borek

How to run:
```sh
python3 password_cracker.py --users users.txt --dictionary dictionary.txt --constant "constant"

    --users List of users; each line consisting of name, salt (hexa) and password hash (hexa, 32 characters)
    --dictionary File with words on separate lines
    --constant Constant; text prepended to a password before computing its hash


# information-security-assignments
Assignments for the course "Information Security", taken at Aalto University in 2016

Author: Martin Borek

#Password cracker
Simple password cracker implemented in Python.

How to run:
```sh
password_cracker.py --users users.txt --dictionary dictionary.txt --constant "constant"
    --users List of users; each line consisting of name, salt (hexa) and password hash (hexa, 32 characters)
    --dictionary File with words on separate lines
    --constant Constant; text prepended to a password before computing its hash


#!/usr/bin/env python3
"""Set or change the admin password:  python3 admin/set_password.py"""
import getpass, sys
import common

user = input("Admin username [admin]: ").strip() or "admin"
pw = getpass.getpass("New password (min 10 characters): ")
if len(pw) < 10 or pw != getpass.getpass("Repeat password: "):
    sys.exit("Passwords differ or are too short. Nothing changed.")
common.set_password(user, pw)
print("Password updated.")

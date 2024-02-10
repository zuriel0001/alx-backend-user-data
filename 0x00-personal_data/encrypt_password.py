#!/usr/bin/env python3
"""
Module for encrypting passwords
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Mrthod that returns a salted, hashed password,
    which is a byte string
    """
    encoded = password.encode()
    hashed = bcrypt.hashpw(encoded, bcrypt.gensalt())

    return (hashed)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Method to validate the provided password that matches
    the hashed password
    """
    valid = False
    encoded = password.encode()
    if bcrypt.checkpw(encoded, hashed_password):
        valid = True
    return (valid)

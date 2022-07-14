""" Module for database

    Classes:
        User
            tasks' table
        Task
            users' table
        Staging
            queue's table
        Game
            games' table

    Functions:
        get_session
            gets database session
"""
from core.store.db_model import UserTable, TaskTable

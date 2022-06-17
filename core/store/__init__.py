""" Module for database

    Classes:
        User
            users' table
        Task
            tasks' table
        Staging
            queue's table
        Game
            games' table

    Functions:
        get_session
            gets database session
"""
from core.store.db_model import UserTable, TaskTable, TaskModerationTable

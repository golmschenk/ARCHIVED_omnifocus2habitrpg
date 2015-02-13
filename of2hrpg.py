"""
Interactions between OmniFocus and HabitRPG
"""

import json
from secret import habitrpg_api_token, habitrpg_user_id
import urllib.request
from applescript import AppleScript
from getch import getch

class Of2Hrpg:
    """
    A class to allow interaction between OmniFocus and HabitRPG
    """
    def __init__(self):
        self.of_tasks_completed_today = []
        self.hrpg_dailies = []

    def obtain_completed_of_list_for_today(self):
        """
        Obtains the list of tasks which have been completed today. "of" is for OmniFocus.
        """
        #applescript = AppleScript(path="OmniFocus.scpt")
        applescript = AppleScript("""on getAllTasksCompletedToday()
                                         set dateToday to date (short date string of (current date))
                                         tell application "OmniFocus"
                                             tell front document
                                                 set completedTasks to (name of every flattened task whose completed is true and completion date ≥ dateToday)
                                             end tell
                                         end tell
                                         return completedTasks
                                     end getAllTasksCompletedToday""")
        self.of_tasks_completed_today = applescript.call("getAllTasksCompletedToday")

    def obtain_hrpg_dailies(self):
        """
        Gets the character's dailies and adds them to the object.
        """
        request = urllib.request.Request("https://habitrpg.com/api/v2/user/tasks",
                                   headers={"x-api-key": habitrpg_api_token, "x-api-user": habitrpg_user_id})
        response = urllib.request.urlopen(request)
        tasks = json.loads(response.read().decode('utf-8'))
        self.hrpg_dailies = [task for task in tasks if task["type"] == "daily"]

    def complete_task(self, task):
        request = urllib.request.Request("https://habitrpg.com/api/v2/user/tasks/%s/up" % task['id'],
                                         data=b'',
                                         headers={"x-api-key": habitrpg_api_token, "x-api-user": habitrpg_user_id})
        urllib.request.urlopen(request)

    def create_and_complete_todo_task(self, text, priority=1):
        """
        Creates a new todo task and marks it complete.
        :param text: Set the task text.
        :param priority: Set the difficulty (easy: 1, medium: 1.5, hard: 2).
        """
        # Create the task.
        task = {"text": text, "priority": priority, "type": "todo"}
        params = json.dumps(task).encode('utf8')
        request = urllib.request.Request("https://habitrpg.com/api/v2/user/tasks",
                                         data=params,
                                         headers={'content-type': 'application/json',
                                                  "x-api-key": habitrpg_api_token,
                                                  "x-api-user": habitrpg_user_id})
        response = urllib.request.urlopen(request)

        # Complete the task.
        task = json.loads(response.read().decode('utf-8'))
        self.complete_task(task)

    def process_task(self, name):
        """
        Handles what to do for a given task from OmniFocus
        """
        # Check if it's a daily.
        daily = next(daily for daily in self.hrpg_dailies if daily.text == name)
        if daily:
            # We don't want to use it if it's already completed.
            if not daily.completed:
                self.complete_task(daily)
        else:
            # Make a regular to-do.
            priority = self.request_priority(name)
            if priority != -1:
                self.create_and_complete_todo_task(name, priority)

    def interface(self):
        """
        Presents an interface for the user to select which items to be processed.
        """
        self.obtain_hrpg_dailies()
        self.obtain_completed_of_list_for_today()
        print("For each task, select the difficulty by key (1=easy, 2=medium, 3=hard).")
        print("To not submit the task, click any other key.")
        for name in self.of_tasks_completed_today:
            self.process_task(name)

    def request_priority(self, name):
        """
        Ask the user what difficulty the task should be.
        """
        print(name)
        character = getch()
        if character == '1':
            return 1
        elif character == '2':
            return 1.5
        elif character == '3':
            return 2
        else:
            return -1

if __name__ == "__main__":
    pass
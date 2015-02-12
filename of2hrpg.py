"""
Interactions between OmniFocus and HabitRPG
"""

import json
from secret import habitrpg_api_token, habitrpg_user_id
import urllib.request
from applescript import AppleScript

class Of2Hrpg:
    """
    A class to allow interaction between OmniFocus and HabitRPG
    """
    def __init__(self):
        self.of_tasks_completed_today = []
        self.hrpg_dailies = []

    def attain_completed_omnifocus_list_for_today(self):
        """
        Returns the list of tasks which have been completed today.
        """
        applescript = AppleScript(path="OmniFocus.scpt")
        return applescript.call("getAllTasksCompletedToday")

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
        pass
        #if name in self.hrpg_dailies:

if __name__ == "__main__":
    of2hrpg = Of2Hrpg()
    #of2hrpg.create_and_complete_todo_task("testapiscript")
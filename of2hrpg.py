"""
Interactions between OmniFocus and HabitRPG
"""

import json
from secret import habitrpg_api_token, habitrpg_user_id
import urllib.request
#from applescript import AppleScript

class Of2Hrpg:
    def __init__(self):
        self.of_tasks_completed_today = []
        self.hrpg_dailies = []

    #def attain_completed_omnifocus_list_for_today(self):
    #    applescript = AppleScript(path="OmniFocus.scpt")
    #    return applescript.run("getAllTasksCompletedToday")

    def obtain_hrpg_dailies(self):
        request = urllib.request.Request("https://habitrpg.com/api/v2/user/tasks",
                                   headers={"x-api-key": habitrpg_api_token, "x-api-user": habitrpg_user_id})
        response = urllib.request.urlopen(request)
        tasks = json.loads(response.read().decode('utf-8'))
        self.hrpg_dailies = [task for task in tasks if task["type"] == "daily"]

if __name__ == "__main__":
    of2hrpg = Of2Hrpg()
    of2hrpg.obtain_hrpg_dailies()
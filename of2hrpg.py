"""
Interactions between OmniFocus and HabitRPG
"""

from applescript import AppleScript

class Of2Hrpg:
    def attain_completed_omnifocus_list_for_today(self):
        applescript = AppleScript(path="OmniFocus.scpt")
        return applescript.run("getAllTasksCompletedToday")

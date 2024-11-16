from typing import List
import matplotlib.pyplot as plt
import pandas as pd

from data_loader import DataLoader
from model import Issue
import config

from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from model import Issue,Event
import config

from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_loader import DataLoader
from model import Issue,Event
import config

class UserAnalyzer:  
    def user_issue_count(self, user_name: str):
        issues = DataLoader().get_issues()
        
        # Filter issues to only those created by the specified user
        user_issues = [issue for issue in issues if issue.creator == user_name]
        
        # Output the count of issues created by the user
        issue_count = len(user_issues)
        print(f"{user_name} has created {issue_count} issue(s):")
        
        # Display each issue's label and creation date
        for issue in user_issues:
            created_date = issue.created_date.strftime("%Y-%m-%d") if issue.created_date else "Unknown date"
            labels = ', '.join(issue.labels) if issue.labels else "No labels"
            print(f" - Issue created on {created_date} with label(s): {labels}")

if __name__ == '__main__':
    UserAnalyzer().run()
import calendar
from datetime import datetime
import config
from typing import List
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import Counter
from data_loader import DataLoader
from model import Issue,Event



class MonthlyIssueAnalyser:
    def __init__(self, year=None):
        """
        Initializes the analyzer for the given year or all years if None.
        """
        self.USER: str = config.get_parameter('user')
        # Store the year to filter issues
        self.year = year  

    def analyse(self):
        #Analyzes issues from the input year and generates a issue frequency bar chart for given year.
    
        issues = DataLoader().get_issues()
        # Initialize list for each month
        monthly_issue_counts = [0] * 12  
        
        for issue in issues:
            # Ensure created_date is a string and handle None
            if issue.created_date is not None:
                issue_date_str = str(issue.created_date)  # Convert to string if needed
                issue_date = datetime.fromisoformat(issue_date_str)
                
                # Filter issues by specified year, or consider all years if not provided
                if self.year is None or issue_date.year == self.year:
                    monthly_issue_counts[issue_date.month - 1] += 1
            else:
                print("Skipping issue with no created_date")
        if self.year is not None:
            print(f'The total number of issues reported in year {self.year} is {sum(monthly_issue_counts)}.')
        else:
            print(f'Month-Wise breakdown of the total number of issues reported across all years is {sum(monthly_issue_counts)}.')
        # Plotting the issue frequency per month
        months = calendar.month_name[1:]
        plt.figure(figsize=(12, 6))
        plt.bar(months, monthly_issue_counts, color='lightgreen')
        plt.title(f'Frequency of Issues per Month in {self.year or "All Years"}',color = 'Blue', fontweight='bold')
        plt.xlabel('Month', color='Red', fontweight='bold')
        plt.ylabel('Number of Issues', color='Red',fontweight='bold')
        plt.xticks(rotation=45)

        # Annotate the bars with issue counts
        for i, count in enumerate(monthly_issue_counts):
            plt.text(i, count, str(count), ha='center', va='bottom')

        plt.show()

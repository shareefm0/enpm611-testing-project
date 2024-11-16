from typing import List
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

from data_loader import DataLoader
from model import Issue, Event
import config
from collections import Counter


class TopLabelsAnalyzer:
    
    def __init__(self, label: str = None):
        # Parameter is passed in via command line (--user)
        self.USER: str = config.get_parameter('user')
        self.label = label
    
    def analyse(self):
        
        # get all the issues from the data loader
        issues: List[Issue] = DataLoader().get_issues()
        
        # store all the lables from issues
        labels = []
        for issue in issues:
            labels.extend(issue.labels)
        
        # count the frequency of each label and store
        label_counts = Counter(labels)
        
        if self.label:
            count = label_counts.get(self.label, 0) # count the frequency of input label

            if count > 0:
                print(f"Count for label '{self.label}': {count}") # print the count of the labels
                df = pd.DataFrame([[self.label, count]], columns=['label', 'count'])
                self._plot_data(df)
            else:
                print(f"Label '{self.label}' not present in the data.")  # if label is not present
        else:
            print("Displaying top 50 labels.")
            df = pd.DataFrame(label_counts.most_common(50), columns=['label', 'count'])
            self._plot_data(df)

    # plot the bar graph for the labels
    def _plot_data(self, df):

        plt.figure(figsize=(12, 8))
        plt.barh(df['label'], df['count'], color='skyblue')
        plt.xlabel("Number of Issues", color='red', fontweight='bold')
        plt.ylabel("Label", color='red', fontweight='bold')
        plt.title(f"{'Top 50 Labels' if not self.label else f'Count for Label: {self.label}'}", color='blue', fontweight='bold')
        plt.gca().invert_yaxis()
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
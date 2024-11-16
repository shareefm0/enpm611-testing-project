from typing import List
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

from data_loader import DataLoader
from model import Issue, Event
import config
from collections import Counter
class EventAnalysis:

    
    def __init__(self):
        self.USER: str = config.get_parameter('user')
    
    def run(self):

        issues: List[Issue] = DataLoader().get_issues()
        dates = []
        
        for issue in issues:
            for event in issue.events:
                event_date = event.event_date 
                dates.append(event_date)

        df = pd.DataFrame(dates, columns=["date"])
        df['count'] = 1
        df = df.groupby('date').count().resample('D').sum().fillna(0) 

        #plotting
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['count'], marker='o', color='b')
        
        plt.title("Event Activity Over Time")
        plt.xlabel("Date")
        plt.ylabel("Event Count")
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
                        
if __name__ == '__main__':
    EventAnalysis().run()
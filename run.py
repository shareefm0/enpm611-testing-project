

"""
Starting point of the application. This module is invoked from
the command line to run the analyses.
"""

import argparse

import config
from example_analysis import ExampleAnalysis
from first_feature import MonthlyIssueAnalyser
from feature_2 import TopLabelsAnalyzer
from feature_3 import UserAnalyzer
from feature_4 import EventAnalysis

def parse_args():
    """
    Parses the command line arguments that were provided along
    with the python command. The --feature flag must be provided as
    that determines what analysis to run. Optionally, you can pass in
    a user and/or a label to run analysis focusing on specific issues.
    
    You can also add more command line arguments following the pattern
    below.
    """
    ap = argparse.ArgumentParser("run.py")
    
    # Required parameter specifying what analysis to run
    ap.add_argument('--feature', '-f', type=int, required=True,
                    help='Which of the three features to run')
    
    # Optional parameter for analyses focusing on a specific user (i.e., contributor)
    ap.add_argument('--user', '-u', type=str, required=False,
                    help='Optional parameter for analyses focusing on a specific user')
    
    # Optional parameter for analyses focusing on a specific label
    ap.add_argument('--label', '-l', type=str, required=False,
                    help='Optional parameter for analyses focusing on a specific label')
    
    return ap.parse_args()



# Parse feature to call from command line arguments
args = parse_args()
# Add arguments to config so that they can be accessed in other parts of the application
config.overwrite_from_args(args)
    
# Run the feature specified in the --feature flag
if args.feature == 0:
    ExampleAnalysis().run()
elif args.feature == 1:
    # Ask the user to input a four-digit year
    year_input = input("Please enter a four-digit year (e.g., 2023) to filter issues, or leave blank for all years: ")
    
    # Validate the input to ensure it's a four-digit number or blank
    # Check if input is a valid 4-digit number
    if year_input == "":
        year = None
    elif not year_input.isdigit() or len(year_input) != 4:
        raise ValueError("Invalid input. Please enter a 4-digit year.")
    else:
        year = int(year_input)

    MonthlyIssueAnalyser(year=year).analyse()
elif args.feature == 2:
    label_input = input("Enter a specific label to analyze or leave blank for the top 50 labels: ").strip()
    label = label_input if label_input else None
    TopLabelsAnalyzer(label=label).analyse()
elif args.feature == 3:
    user_name = args.user if args.user else input("Enter the user name to analyze their issues: ")
    if user_name:
        UserAnalyzer().user_issue_count(user_name)
    else:
        print("User name is required for this analysis")
elif args.feature == 4:
    EventAnalysis().run()
else:
    print('Need to specify which feature to run with --feature flag.')

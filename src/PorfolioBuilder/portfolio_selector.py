import pandas as pd
import numpy as np


def get_top_performers(df, n=10):
    """
    Get the top performers in the portfolio.
    """
    # Get the top performers
    industries = 1
    top_performers = df.sort_values(by='Return', ascending=False)[:n]
    # Get the top performers
    top_performers = top_performers.sort_values(by='Return', ascending=False)
    # Return the top performers
    return top_performers
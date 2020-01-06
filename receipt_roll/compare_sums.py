import settings
import pandas as pd

roll_df = pd.read_csv(settings.ROLL_CSV)
sums_df = pd.read_csv(settings.DAILY_SUMS_CSV)


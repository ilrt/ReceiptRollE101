# Notes

Notes of method calls for data used in the paper and blog posts

----

We need to import the libraries

```
import pandas as pd
from receipt_roll import roll_data as rd
from receipt_roll import roll_plot as rp
from receipt_roll import money as money
```

Note: we filter out 0, since 'Pence' will be 0 for days the Exhequer didn't sit.

```
df_po = df[df['Pence'] > 0]
```

Get the minimum payment.

```
money.pence_to_psd(df_po['Pence'].min())
```

Maximum payment:

```
money.pence_to_psd(df_po['Pence'].max())
```

Mean payment:

```
money.pence_to_psd(df_po['Pence'].mean())
```

Mode

```
money.pence_to_psd(df_po['Pence'].mode()[0])
```

Create a new data frame with half a mark (80 pence) values only:

```
df_hm = df_po[df_po['Pence'] == 80.0]
```

Figure 1: Total payments by term

```
rp.plt_total_by_terms(title='1. Total payments, per term', is_long_title=False, show=False)
```

Figure 2: Number of days per term
```
rp.plt_days_by_term(title="2. Number of days, per term", is_long_title=False, show=False)
```
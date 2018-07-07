import pandas as pd
import numpy as np

# df = pd.read_csv('us-500.csv')
def guess_match(df):
    df_low = df.apply(lambda x: x.astype(str).str.lower())

    cities = pd.read_table('../data/us_cities.txt', header=None).iloc[:,2].unique()
    cities = list(map(lambda x: x.lower(), cities))

    states_abs = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    states_long = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
      "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
      "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
      "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
      "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
      "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
      "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
      "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
    states = states_abs + states_long
    states = list(map(lambda x: x.lower(), states))

    given_names = pd.read_table('../data/popular-both-first.txt', delim_whitespace=True, header=None).iloc[:,0]
    # given_names = list(map(lambda x: x.lower(), given_names))
    given_names = list(given_names.astype(str).str.lower())

    family_names = pd.read_table('../data/last_names.txt', delim_whitespace=True, header=None).iloc[:,0]
    family_names = list(family_names.astype(str).str.lower())

    col_dict = {'given_names': given_names, 'family_names': family_names, 'states': states }
    col_lst = []
    col_names = []
    for col_name, col in col_dict.items():
        col_lst.append(df_low.isin(col).mean()*100)
        col_names.append(col_name)
    df_match = pd.concat(col_lst, axis=1)

    df_match.columns = col_names

    email_match_dict = {}
    for co in df_low.columns:
        email_match_dict[co] = df_low[co].str.contains("@").mean()*100

    estimated_names = {}
    for col in col_names:
        estimated_names[col] = df_match[col].idxmax()

    estimated_names['emails'] = max(email_match_dict, key=email_match_dict.get)

    db_fields_match_dict = {'db_first': 'given_names', 'db_last': 'family_names', 'db_state': 'states', 'db_email': 'emails'}

    final_match_dict = {}
    for k, v in db_fields_match_dict.items():
        final_match_dict[k] = estimated_names[v]

    return final_match_dict

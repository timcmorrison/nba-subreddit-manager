from datetime import datetime


def get_year():
    date = datetime.today()
    if date.month < 7:
        return str(date.year)
    else:
        return str(date.year + 1)


def to_ordinal(date):
    day = int(date[-2:])
    ones_place = int(date[-1:])

    if 10 < day < 20:
        return date + 'th'

    if ones_place == 1:
        return date + 'st'
    elif ones_place == 2:
        return date + 'nd'
    elif ones_place == 3:
        return date + 'rd'
    else:
        return date + 'th'


# Want to display previous 5 games + 5 next games
def get_game_index(df):
    nan_values = df[df['Tm'].isna()]
    index = nan_values.index[0] - 7
    if index < 0:
        return 0
    if index > 71:
        return 71
    return index
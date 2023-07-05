import pandas as pd
import random
from myLogger import my_logger
import logging

logger = my_logger()
logger.setLevel(logging.WARNING)
in_xlsx_file = './drop_test.xlsx'

pd.set_option('display.max_rows', 500) 
pd.set_option('display.max_columns', 500) 
pd.set_option('display.unicode.east_asian_width', True) 

def design_data(design_cols, design_header, design_sheet):
    return pd.read_excel(
        in_xlsx_file,
        sheet_name=design_sheet,
        usecols=design_cols,
        header=design_header,
    ).dropna(how='all')


drop_df = design_data('A:H', 0, 'drop')
packs_df = design_data('A:E', 0, 'packs')
cards_df = design_data('A:F', 0, 'cards')
logger.debug(drop_df)
logger.debug(packs_df)
logger.debug(cards_df)


def gen_drop_num(drop_nums):
    weights_df = pd.DataFrame(drop_nums.split(','), columns=['weights'])
    weights = weights_df['weights'].astype('int').to_list()
    return random.choices(list(range(len(weights))), weights=weights, k=1)[0]


def gen_drop_pack(mode, drop_times):
    drop_row = drop_df.loc[(drop_df['mode'] == mode) & (
        drop_df['start_times'] <= drop_times)].tail(1)
    drop_nums = drop_row['drop_nums'].astype('str').values[0]
    pack_id = drop_row['pack_id'].values[0]
    pack_num = gen_drop_num(drop_nums)
    return (pack_id, pack_num)


def gen_drop_stars(pack_id):
    drop_row = packs_df[packs_df['pack_id'] == pack_id]
    weights = drop_row['card_weights'].astype('int').to_list()
    card_star_list = drop_row['card_star'].astype('int').to_list()
    card_num = drop_row['card_num'].astype('int').to_list()[0]
    return (random.choices(card_star_list, weights=weights, k=card_num))


def gen_drop_card(drop_card_star, pack_times):
    card_id = 0
    drop_row = cards_df[(cards_df['star'] == drop_card_star)
                        & (cards_df['times_limits'] <= pack_times)]
    card_pool = drop_row['id'].astype('int').to_list()
    weights = [1 for _ in range(len(card_pool))]
    if len(card_pool) > 0:
        card_id =random.choices(card_pool, weights=weights, k=1)[0]
    return (card_id)


def update_card_set(card_list):
    cards_df.loc[cards_df['id'].isin(card_list), 'already'] = True
    return (cards_df)


def check_card_set(already_sets):
    check_df = cards_df[cards_df['set'].isin(already_sets)]
    return (check_df['already'].all())


def level_drop_card(mode, drop_times, pack_times):
    card_star_list = []
    card_list = []
    pack_id, pack_num = gen_drop_pack(mode, drop_times)
    drop_times += 1
    if pack_num > 0:
        for _ in range(pack_num):
            one_pack = gen_drop_stars(pack_id)
            card_star_list.append(one_pack)

        for one_pack in card_star_list:
            for star in one_pack:
                card_id = gen_drop_card(star, pack_times)
                card_list.append(card_id)
            pack_times += 1
    update_card_set(card_list)
    return (card_list, pack_times, drop_times)


mode = 3
drop_times = 0
pack_times = 0
target_sets = [1,2,3]

count = 200

# for _ in range(count):
#     card_list,drop_times,pack_times = level_drop_card(mode, drop_times, pack_times)
while check_card_set(target_sets) == False:
    card_list,drop_times,pack_times = level_drop_card(mode, drop_times, pack_times)


logging.warning(cards_df)
logging.warning(drop_times)
logging.warning(pack_times)
# cards_df.to_excel("cards_df.xlsx", index=False)


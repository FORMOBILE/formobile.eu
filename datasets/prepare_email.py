"""
Module with functions to prepare the email dataset.
"""
import json
import os
import pandas as pd

from datasets.reddit_email import get_email_conversation
from datasets.get_mods import get_mods, get_mods_from_file


def concat_sub_conv(sub: pd.DataFrame, convers: pd.DataFrame) -> pd.DataFrame:
    """
    Concatenates submission and replies to one dataframe.

    :param sub: DataFrame of the initial post.
    :param convers: DataFrame of the replies.
    :return: formatted DataFrame
    """
    sub = sub[['title', 'author', 'selftext']]
    sub.rename(columns={'title': 'previous message', 'selftext': 'body'}, inplace=True)
    for i, conv in enumerate(convers):
        convers[i] = pd.concat(
            [sub.iloc[i:i+1], conv], ignore_index=True)[['previous message', 'body']].to_dict(orient='records')
    return convers


# pylint: disable = invalid-name
def prepare() -> None:
    """
    Prepares the email dataset and stores it in the "SeriousConversation" sub folder.

    :return: Nothing
    """
    try:
        mods = get_mods('SeriousConversation')
    except KeyError:
        mods = get_mods_from_file(os.path.join(os.path.dirname(__file__), "SeriousConversation", "moderators_SC.json"))

    path = os.path.join(os.path.dirname(__file__), "SeriousConversation")

    init_mail, replies = get_email_conversation(path, mods)

    conversations = concat_sub_conv(init_mail, replies)

    dictionary = {}
    for index, _ in enumerate(conversations):
        dic = {'content': conversations[index]}
        dictionary[f"{index}"] = dic

    with open(os.path.join(path, 'email_dataset.json'), 'w+') as f:
        json.dump(dictionary, f)

"""
Module to prepare reddit-comments-dl data to be used as messages for group conversations
"""
import copy
import logging
import os
import json
import pandas as pd

from datasets.get_mods import get_mods, get_mods_from_file


def get_conversations(path: str, moderators: list = None) -> (list, list):
    """
    Formats the reddit-comments-dl data in the given path

    The function tries to find messages that have been posted by moderators and skips them since those are often
    "This post has been removed because... " messages

    Currently only the longest conversation of each initial reply is stored.

    :param path: path where the reddit-comments-dl data is stored
    :param moderators: list of moderator names
    :return: tuple of lists
    """
    logging.info('Started Reddit comments formatting')
    # most common automods I found
    if moderators is None:
        moderators = ['AutoModerator', 'IAmAModBot', 'Flair_Helper']
        logging.info('No Moderator list submitted - using default list')

    submissions = pd.read_csv(os.path.join(path, 'submissions', '0.csv'),
                              dtype={'id': 'str', 'submission_id': 'str',
                                     'body': 'str', 'created_utc': 'int',
                                     'parent_id': 'str', 'author': 'str',
                                     'permalink': 'str'}).fillna(moderators[0])
    # drop removed rows/posts
    removed = submissions[submissions['selftext'] == '[removed]'].id.values
    submissions = submissions[submissions['selftext'] != '[removed]']
    logging.info('Removed removed posts')

    comments = pd.read_csv(os.path.join(path, 'comments', '0.csv')).fillna(moderators[0])
    # remove removed comments
    comments = comments[comments['body'] != '[deleted]']

    # remove comments of removed posts
    for rem in removed:
        comments = comments[comments['submission_id'] != rem]
    logging.info('Removed comments of removed posts')

    cons = []
    authors = list(copy.deepcopy(submissions['author'].values))
    for i in range(len(submissions)):
        conv_id = submissions['id'].iloc[i]
        # all replies to post
        all_replies = comments.loc[comments['submission_id'] == conv_id]

        # direct replies to post
        initial_replies = all_replies[list(map(lambda x: x.startswith('t3_'), all_replies['parent_id']))]

        # comments to comments
        further_replies = all_replies[list(map(lambda x: x.startswith('t1_'), all_replies['parent_id']))]

        conversations = []

        for reply_number in range(len(initial_replies)):

            if initial_replies['author'].iloc[reply_number] in moderators:
                logging.info(
                    f'skipped comments of '
                    f'{initial_replies.iloc[reply_number]["submission_id"]} as it was removed by mod')
                break

            previous_message = submissions['title'].iloc[i]
            # initial replies
            reply_thread_id = initial_replies['id'].iloc[reply_number]

            if initial_replies['author'].iloc[reply_number] not in authors:
                authors.append(initial_replies['author'].iloc[reply_number])

            # check if username is used in message
            usernames = [ele for ele in authors if ele in initial_replies['body'].iloc[reply_number]]
            # if true remove username
            if usernames:
                try:
                    initial_replies['body'] = initial_replies['body'].replace(str(list(set(usernames))), "", regex=True)
                    logging.info(
                        f'Deleted username in comment of {initial_replies.iloc[reply_number]["submission_id"]}')
                except:
                    logging.info('failed to remove username')

            conversation_df = pd.DataFrame(columns=['author', 'body', 'previous message'])
            conversation_df = conversation_df.append({'author': initial_replies['author'].iloc[reply_number],
                                                      'body': initial_replies['body'].iloc[reply_number],
                                                      'previous message': previous_message}, ignore_index=True)

            previous_message = initial_replies['body'].iloc[reply_number]

            while True:
                reply = further_replies.loc[further_replies['parent_id'].str.endswith(reply_thread_id)]
                if reply.empty:
                    break
                reply_body = reply['body'].iloc[0]
                reply_author = reply['author'].iloc[0]

                # append username to list of usernames
                if reply_author not in authors:
                    authors.append(reply_author)

                # Check if username is used in message
                usernames = [ele for ele in authors if ele in reply_body]
                if usernames:
                    for name in usernames:
                        # remove username
                        reply_body = reply_body.replace(name, "")
                        logging.info(f'Removed username from {further_replies["submission_id"]}')

                conversation_df = conversation_df.append({'author': reply_author,
                                                          'body': reply_body,
                                                          'previous message': previous_message}, ignore_index=True)

                reply_thread_id = reply['id'].iloc[0]

                previous_message = reply_body
            if not reply.empty:
                reply_thread_id = reply['id']

            conversations.append(conversation_df)

        cons.append(conversations)
    return submissions, cons


def concat_sub_conv(sub: pd.DataFrame, convers: list) -> list:
    """
    Appends the submission (initial post) to the list of comments

    :param sub: submission data
    :param convers: conversations
    :return:
    """
    for i, conv in enumerate(convers):
        conv.insert(0, sub.iloc[i:i + 1])
    return convers


# pylint: disable = invalid-name
def prepare():
    """
    Prepares the email dataset and stores it in the "CasualConversation" sub folder.

    :return: Nothing
    """
    direc = os.path.join(os.path.dirname(__file__), 'CasualConversation')

    try:
        mods = get_mods('CasualConversation')
    except KeyError:
        mods = get_mods_from_file(os.path.join(os.path.dirname(__file__), 'CasualConversation', 'moderators_CC.json'))

    submissions, conversations = get_conversations(direc, mods)

    submissions['body'] = submissions['title'] + "\n" + submissions['selftext']
    submissions['previous message'] = ""
    submissions = submissions[['author', 'body', 'previous message']]

    list_for_json = concat_sub_conv(submissions, conversations)
    dictionary = {}
    for index, conversation in enumerate(list_for_json):
        dic = {}
        for j, msg in enumerate(conversation):
            list_for_json[index][j] = msg.to_dict(orient='records')
        dic['content'] = list_for_json[index]
        dictionary[f"{index}"] = dic

    with open(os.path.join(direc, 'group_chats.json'), 'w+') as f:
        json.dump(dictionary, f)


def prepare_subreddit(direc: str, mods: list):
    """
    Prepares the conversations dataset and stores it in the subreddit folder.

    :param subreddit: directory of the subreddit
    :param mods: the list of moderators of a subreddit
    :return: Nothing
    """
    # Removes all unwanted comments from moderators
    submissions, conversations = get_conversations(direc, mods)

    submissions['body'] = submissions['title'] + "\n" + submissions['selftext']
    submissions['previous message'] = ""
    submissions = submissions[['author', 'body', 'previous message']]

    # Concatenates the conversations into one
    list_for_json = concat_sub_conv(submissions, conversations)
    dictionary = {}
    for index, conversation in enumerate(list_for_json):
        dic = {}
        for j, msg in enumerate(conversation):
            list_for_json[index][j] = msg.to_dict(orient='records')
        dic['content'] = list_for_json[index]
        dictionary[f"{index}"] = dic

    with open(os.path.join(direc, 'group_chats.json'), 'w+') as f:
        json.dump(dictionary, f)

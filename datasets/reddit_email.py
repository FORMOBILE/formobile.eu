"""
Format subreddit-comment-dl data for email purposes
"""
import copy
import logging
import os

import pandas as pd


# pylint: disable = invalid-name
def get_email_conversation(path: str,  mods: list = None) -> (list, list):
    """
    Formats the given data to lists of dataframes

    :param path: path to downloaded data
    :param mods: list of mods of the subreddit, used to filter "this post has been removed because" messages
    :return: tuple of two lists
    """
    logging.info('Started Reddit comments formatting')
    # most common automods I found
    if mods is None:
        mods = ['AutoModerator', 'IAmAModBot', 'Flair_Helper']
        logging.info('No Moderator list submitted - using default list')

    submissions = pd.read_csv(os.path.join(path, 'submissions', '0.csv')).fillna(mods[0])
    # drop removed rows/posts
    removed = submissions[submissions['selftext'] == '[removed]'].id.values
    submissions = submissions[submissions['selftext'] != '[removed]']
    logging.info('Removed removed posts')
    comments = pd.read_csv(os.path.join(path, 'comments', '0.csv')).fillna(mods[0])
    # remove removed comments
    comments = comments[comments['body'] != '[deleted]']
    # remove comments of removed posts
    for rem in removed:
        comments = comments[comments['submission_id'] != rem]

    logging.info('Removed all comments of removed posts')
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

        if not initial_replies.empty:
            reply = initial_replies.iloc[0]
        else:
            df = pd.DataFrame(columns=['author', 'body', 'previous message'])
            cons.append(df)
            continue

        if reply['author'] in mods:
            logging.info(f'skipped comments of {reply["submission_id"]} as it was removed by mod')
            continue

        reply_thread_id = initial_replies['id'].iloc[0]

        previous_message = submissions['selftext'].iloc[i]

        if reply['author'] not in authors:
            authors.append(reply['author'])

        conversation_df = pd.DataFrame(columns=['author', 'body', 'previous message'])
        conversation_df = conversation_df.append({'author': reply['author'],
                                                  'body': reply['body'],
                                                  'previous message': previous_message}, ignore_index=True)
        # display(further_replies)
        previous_message = reply['body']
        while True:
            reply_ = further_replies.loc[further_replies['parent_id'].str.endswith(reply_thread_id)]
            # display(reply_)
            if reply_.empty:
                break
            reply_body = reply_['body'].iloc[0]
            reply_author = reply_['author'].iloc[0]

            # append username to list of usernames
            #if reply_author not in authors:
             #   authors.append(reply_author)

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

            reply_thread_id = reply_.iloc[0]['id']

            previous_message = reply_body

        if not reply_.empty:
            reply_thread_id = reply_['id']

        cons.append(conversation_df)

    return submissions, cons

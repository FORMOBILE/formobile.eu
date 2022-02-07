"""
Script to add emojis to the amazon dataset
"""
import os
import random

import pandas as pd


# pylint: disable=invalid-name
def amazon_add_emojis(path: str) -> None:
    """
    Adds emojis to the amazon dataset based on sentiment and stores it in the same directory.
    :param path: path to the amazon dataset
    :return: Nothing
    """

    df = pd.read_json(path)

    keys = df.keys()

    angry = ['\U0001F624', '\U0001F621', '\U0001F620', '\U0001F92C', '\U0001F47F', '\U0001F4A2']

    disgusted = ['\U0001F922', '\U0001F92E']

    fearful = ['\U0001F631', '\U0001F630', '\U0001F625']

    sad = ['\U0001F615', '\U0001F62D', '\U0001F61E', '\U0001F614', '\u2639', '\U0001F641', '\U0001F629']

    happy = ['\U0001F600', '\U0001F603', '\U0001F604', '\U0001F601', '\U0001F642', '\U0001F60A', '\u263A']

    surprised = ['\U0001F92F', '\U0001F62E', '\U0001F62F', '\U0001F632', '\U0001F631']

    curious = ['\U0001F9D0', '\U0001F914', '\U0001F928', '']

    for key in keys:
        dff = df[key]
        for i in range(len(dff['content'])):
            dff['content'][i]['message'] = dff['content'][i]['message'].replace('\"', '\'').strip('\n')
            # logging.info()
            dff['content'][i]['message'] = dff['content'][i]['message'].replace('\n', '<br />')
            if dff['content'][i]['sentiment'] == 'Angry':
                dff['content'][i]['message'] = dff['content'][i]['message'] + " " + random.choice(angry)

            elif dff['content'][i]['sentiment'] == 'Disgusted':
                dff['content'][i]['message'] = dff['content'][i]['message'] + " " + random.choice(disgusted)

            elif dff['content'][i]['sentiment'] == 'Fearful':
                dff['content'][i]['message'] = dff['content'][i]['message'] + " " + random.choice(fearful)

            elif dff['content'][i]['sentiment'] == 'Sad':
                dff['content'][i]['message'] = dff['content'][i]['message'] + " " + random.choice(sad)

            elif dff['content'][i]['sentiment'] == 'Happy':
                dff['content'][i]['message'] = dff['content'][i]['message'] + " " + random.choice(happy)

            elif dff['content'][i]['sentiment'] == 'Surprised':
                dff['content'][i]['message'] = dff['content'][i]['message'] + " " + random.choice(surprised)

            elif dff['content'][i]['sentiment'] == 'Curious to dive deeper':
                dff['content'][i]['message'] = dff['content'][i]['message'] + " " + \
                                               random.choices(population=curious, weights=[0.01, 0.05, 0.02, 0.92])[0]

            elif dff['content'][i]['sentiment'] == 'Neutral':
                dff['content'][i]['message'] = dff['content'][i]['message']

    data_with_emojis = os.path.join(os.path.dirname(path), 'messages_emoji.json')
    df.to_json(data_with_emojis)

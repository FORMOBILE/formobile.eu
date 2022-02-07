import random
import time
import pandas as pd

from datasets.reddit_email import get_email_conversation


def start(person1, person2, person3, person4, person5, person6, path1,
          person7, person8, person9, person10, person11, person12, path2,
          person13, person14, person15, person16, person17, person18, path3):

    members = [person1, person2]

    # Formatting the data
    init_mail, replies = get_email_conversation(path1, members)

    # Send initial messages
    for i, msg in init_mail.iterrows():
        body = f'Dear {person2.name}\n\n' + msg['selftext'].replace("\\n", "\n") + f"\n\n{person1.signature}"
        person1.send_mail(person2.email_address, msg['title'], body)

        body = f'Dear {person4.name}\n\n' + msg['selftext'].replace("\\n", "\n") + f"\n\n{person3.signature}"
        person3.send_mail(person4.email_address, msg['title'], body)

        body = f'Dear {person6.name}\n\n' + msg['selftext'].replace("\\n", "\n") + f"\n\n{person5.signature}"
        person5.send_mail(person6.email_address, msg['title'], body)

        duration = random.uniform(100, 150)
        time.sleep(duration)

    # Concat all reply data into one big DataFrame
    df = pd.DataFrame(columns=['author', 'body', 'previous message'])
    for data in replies:
        df = pd.concat([df, data], ignore_index=True)

    # Replies to all messages after some time
    time.sleep(30)
    person2.reply_unread_msgs(df, person1, max_results=5000)
    person4.reply_unread_msgs(df, person3, max_results=5000)
    person6.reply_unread_msgs(df, person5, max_results=5000)
    time.sleep(30)
    person1.reply_unread_msgs(df, person2, max_results=5000)
    person3.reply_unread_msgs(df, person4, max_results=5000)
    person5.reply_unread_msgs(df, person6, max_results=5000)
    time.sleep(30)
    person2.reply_unread_msgs(df, person1, max_results=5000)
    person4.reply_unread_msgs(df, person3, max_results=5000)
    person6.reply_unread_msgs(df, person5, max_results=5000)

    members = [person7, person8]

    # Formatting the data
    init_mail, replies = get_email_conversation(path2, members)

    # Send initial messages
    for i, msg in init_mail.iterrows():
        body = f'Dear {person8.name}\n\n' + msg['selftext'].replace("\\n", "\n") + f"\n\n{person7.signature}"
        person7.send_mail(person8.email_address, msg['title'], body)

        body = f'Dear {person10.name}\n\n' + msg['selftext'].replace("\\n", "\n") + f"\n\n{person9.signature}"
        person9.send_mail(person10.email_address, msg['title'], body)

        body = f'Dear {person12.name}\n\n' + msg['selftext'].replace("\\n", "\n") + f"\n\n{person11.signature}"
        person11.send_mail(person12.email_address, msg['title'], body)

        duration = random.uniform(100, 150)
        time.sleep(duration)

    # Concat all reply data into one big DataFrame
    df = pd.DataFrame(columns=['author', 'body', 'previous message'])
    for data in replies:
        df = pd.concat([df, data], ignore_index=True)

    # Replies to all messages after some time
    time.sleep(30)
    person8.reply_unread_msgs(df, person7, max_results=5000)
    person10.reply_unread_msgs(df, person9, max_results=5000)
    person12.reply_unread_msgs(df, person11, max_results=5000)
    time.sleep(30)
    person7.reply_unread_msgs(df, person8, max_results=5000)
    person9.reply_unread_msgs(df, person10, max_results=5000)
    person11.reply_unread_msgs(df, person12, max_results=5000)
    time.sleep(30)
    person8.reply_unread_msgs(df, person7, max_results=5000)
    person10.reply_unread_msgs(df, person9, max_results=5000)
    person12.reply_unread_msgs(df, person11, max_results=5000)

    members = [person13, person14]

    # Formatting the data
    init_mail, replies = get_email_conversation(path3, members)

    # Send initial messages
    for i, msg in init_mail.iterrows():
        body = f'Dear {person15.name}\n\n' + msg['selftext'].replace("\\n", "\n") + f"\n\n{person14.signature}"
        person14.send_mail(person15.email_address, msg['title'], body)

        body = f'Dear {person17.name}\n\n' + msg['selftext'].replace("\\n", "\n") + f"\n\n{person16.signature}"
        person16.send_mail(person17.email_address, msg['title'], body)

        body = f'Dear {person13.name}\n\n' + msg['selftext'].replace("\\n", "\n") + f"\n\n{person18.signature}"
        person18.send_mail(person13.email_address, msg['title'], body)

        duration = random.uniform(100, 150)
        time.sleep(duration)

    # Concat all reply data into one big DataFrame
    df = pd.DataFrame(columns=['author', 'body', 'previous message'])
    for data in replies:
        df = pd.concat([df, data], ignore_index=True)

    # Replies to all messages after some time
    time.sleep(30)
    person15.reply_unread_msgs(df, person14, max_results=5000)
    person17.reply_unread_msgs(df, person16, max_results=5000)
    person13.reply_unread_msgs(df, person18, max_results=5000)
    time.sleep(30)
    person14.reply_unread_msgs(df, person15, max_results=5000)
    person16.reply_unread_msgs(df, person17, max_results=5000)
    person18.reply_unread_msgs(df, person13, max_results=5000)
    time.sleep(30)
    person15.reply_unread_msgs(df, person14, max_results=5000)
    person17.reply_unread_msgs(df, person16, max_results=5000)
    person13.reply_unread_msgs(df, person18, max_results=5000)

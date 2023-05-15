"""
reddit main module
"""

import os
import json
from get_mods import get_mods
from datasets.concat_subreddit_dl_data import concat_data
from reddit_comments import prepare_subreddit

# Here you should specify the subreddit needed, e.g. 'SeriousConversation'
subreddit = 'teenagers'

new_mod_file_name = 'moderators' + '_' + subreddit
download_dir = os.path.join(os.path.dirname(__file__), 'reddit')
src_dir = download_dir + '/' + subreddit + '/'
dst_dir = os.path.join(os.path.dirname(__file__), subreddit)

mod_file_dir = dst_dir + '/' + 'moderators' + '.json'
new_mod_file_dir = dst_dir + '/' + new_mod_file_name + '.json'

# Download of the subreddit
subreddit_dir = os.path.join(os.path.dirname(__file__), 'reddit')

os.chdir(subreddit_dir)
download = os.popen(f'python3 {os.path.join(os.path.dirname(os.path.dirname(__file__)), "subreddit_downloader", "src", "subreddit_downloader.py")}'
                    f' {subreddit} --output-dir {download_dir} --batch-size 100'
                    f' --laps 3 --reddit-id fNz_i4oPdTt19w --reddit-secret SzL9ELsmgmA5LaGwYeHib_Qp3raBBQ '
                    f'--reddit-username Mean_Plankton_87')
os.wait()
download.close()
# Data concatenation
concat_data(src_dir, dst_dir)

# Download of the moderators list
data = get_mods(subreddit)

with open(new_mod_file_dir, 'w') as f:
    json.dump(data, f)

# Prepares the data for conversations
prepare_subreddit(dst_dir, data)

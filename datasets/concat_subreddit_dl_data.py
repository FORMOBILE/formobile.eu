"""
Module to concat the multiple downloaded data from subreddit-comments-dl
"""
import os
import pandas as pd


# pylint: disable=invalid-name
def concat_data(directory: str, path_to_store: str) -> None:
    """
    Concatenates all of the downloaded data in the given directory

    Assumptions:
                    - the directory has the subfolders: 'submissions' and 'comments'

    :param directory: path to the directory
    :param path_to_store: path where the concatenated data should be stored
    :return: Nothing
    """
    final_submission_df = pd.DataFrame()
    final_comments_df = pd.DataFrame()
    list_of_folders = os.listdir(directory)
    for folder in list_of_folders:
        submissions_folder = os.path.join(directory, folder, 'submissions')
        for csv in os.listdir(submissions_folder):
            if csv == 'raw':
                continue
            file = os.path.join(submissions_folder, csv)
            df = pd.read_csv(file)
            final_submission_df = final_submission_df.append(df, ignore_index=True)
        comments_folder = os.path.join(directory, folder, 'comments')
        for csv in os.listdir(comments_folder):
            if csv == 'raw':
                continue
            file = os.path.join(comments_folder, csv)
            df = pd.read_csv(file)
            final_comments_df = final_comments_df.append(df, ignore_index=True)
    final_submission_df.drop_duplicates(inplace=True, ignore_index=True)
    final_comments_df.drop_duplicates(inplace=True, ignore_index=True)

    if not os.path.exists(path_to_store):
        os.mkdir(path_to_store)

    sub_outdir = os.path.join(path_to_store, 'submissions')
    if not os.path.exists(sub_outdir):
        os.mkdir(sub_outdir)
    final_submission_df.to_csv(os.path.join(sub_outdir, '0.csv'), index=False)

    com_outdir = os.path.join(path_to_store, 'comments')
    if not os.path.exists(com_outdir):
        os.mkdir(com_outdir)
    final_comments_df.to_csv(os.path.join(com_outdir, '0.csv'), index=False)

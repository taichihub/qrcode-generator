import pandas as pd
import re
from config.setting import PROGRAM_SETTINGS
from config.setup_log import LOG_MESSAGES, logger


def is_valid_url(url):
    # URLが有効な形式かどうかを検証する。
    valid = re.match(PROGRAM_SETTINGS["URL_PATTERN"], url) is not None
    if not valid:
        logger.error(LOG_MESSAGES["VALIDATE"]["INVALID_URL_FORMAT"].format(url))
    return valid


def is_valid_filename(filename):
    # ファイル名が有効な形式（拡張子が'.png'であるか）を検証する。
    valid = str(filename).endswith(PROGRAM_SETTINGS["EXTENSION"]["IMG"])
    if not valid:
        logger.error(LOG_MESSAGES["VALIDATE"]["INVALID_EXTENSION"].format(filename))
    return valid


# CSVファイルの構造を検証する
def validate_csv_structure(df):
    csv_header_count = len(PROGRAM_SETTINGS['CSV_HEADER'])
    if df.empty:
        logger.error(LOG_MESSAGES["VALIDATE"]["EMPTY_FILE"])
        return False
    if len(df.columns) != csv_header_count:
        logger.error(LOG_MESSAGES["VALIDATE"]["INVALID_COLUMN_COUNT"])
        return False
    return True


# 各行のデータを検証する
def validate_csv_row(df):
    for index, row in df.iterrows():
        if not is_valid_filename(row[PROGRAM_SETTINGS["CSV_HEADER"]["FILE_NAME"]]):
            logger.error(LOG_MESSAGES["VALIDATE"]["INVALID_EXTENSION"].format(index + 1))
        if not is_valid_url(row[PROGRAM_SETTINGS["CSV_HEADER"]["FILE_URL"]]):
            logger.error(LOG_MESSAGES["VALIDATE"]["INVALID_URL_FORMAT"].format(index + 1))


# ファイルの中に連続した改行があるかどうかを検証する
def has_consecutive_newlines(file_path):
    with open(file_path, PROGRAM_SETTINGS["FILE_MODE"], encoding=PROGRAM_SETTINGS["ENCODING"]) as file:
        previous_line_empty = False
        line_number = 0
        for line in file:
            line_number += 1
            if line.strip() == '':
                if previous_line_empty:
                    logger.error(LOG_MESSAGES["VALIDATE"]["CONSECUTIVE_NEWLINES_FOUND"].format(line_number - 1))
                    return False
                previous_line_empty = True
            else:
                previous_line_empty = False
    return True


# CSVファイル全体を検証する
def validate_csv(file_path):
    if not has_consecutive_newlines(file_path):
        return
    try:
        df = pd.read_csv(file_path)
        if not validate_csv_structure(df):
            return
        validate_csv_row(df)
    except pd.errors.EmptyDataError:
        logger.error(LOG_MESSAGES["VALIDATE"]["EMPTY_DATA_ERROR"])
    except pd.errors.ParserError:
        logger.error(LOG_MESSAGES["VALIDATE"]["FORMAT_ERROR"])
    except Exception as e:
        logger.error(LOG_MESSAGES["VALIDATE"]["GENERIC_READ_ERROR"].format(e))

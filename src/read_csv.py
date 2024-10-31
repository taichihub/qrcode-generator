import os
import pandas as pd
import argparse
import sys
from src.validate import validate_csv
from src.generate_qr import generate_qr_code
from config.setting import PROGRAM_SETTINGS
from config.setup_log import LOG_MESSAGES, logger


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(PROGRAM_SETTINGS["RESUME_OPTION"]["SHORT"], PROGRAM_SETTINGS["RESUME_OPTION"]["LONG"], type=int, default=PROGRAM_SETTINGS["START_ROW"])
    parser.add_argument(PROGRAM_SETTINGS["NUMBER_OPTION"]["SHORT"], PROGRAM_SETTINGS["NUMBER_OPTION"]["LONG"], action=PROGRAM_SETTINGS["ACTION"])
    return parser.parse_args()


def get_logo_image_path(img_directory):
    if os.path.exists(img_directory):
        for file in os.listdir(img_directory):
            if file.lower().endswith(PROGRAM_SETTINGS["EXTENSION"]["IMG"]):
                return os.path.join(img_directory, file)
    return None


def create_subfolder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(LOG_MESSAGES["READ_CSV"]["CREATE_SUBFOLDER"].format(path))


def get_output_subfolder(base_folder, file_index):
    folder_number = ((file_index - 1) // PROGRAM_SETTINGS["QR_CODE_FILES_PER_DIR"] + 1) * PROGRAM_SETTINGS["QR_CODE_FILES_PER_DIR"]
    subfolder = os.path.join(base_folder, str(folder_number))
    create_subfolder(subfolder)
    return subfolder


def validate_file(file_path, use_numbering):
    validation_errors = validate_csv(file_path, use_numbering)
    if validation_errors:
        for error in validation_errors:
            logger.error(error)
        return False
    return True


def prepare_subfolder(file_path):
    base_subfolder = os.path.join(PROGRAM_SETTINGS["DIRECTORY"]["OUTPUT"], os.path.splitext(os.path.basename(file_path))[0])
    create_subfolder(base_subfolder)
    return base_subfolder


def should_process_row(row_counter, start_row):
    return row_counter >= start_row


def generate_qr_for_row(row, row_counter, base_subfolder, use_numbering, logo_image_path):
    output_subfolder = get_output_subfolder(base_subfolder, row_counter)
    if use_numbering:
        qr_code_filename = os.path.join(output_subfolder, f"{row_counter}{PROGRAM_SETTINGS['EXTENSION']['IMG']}")
    else:
        qr_code_filename = os.path.join(output_subfolder, row[PROGRAM_SETTINGS["CSV_HEADER"]["FILE_NAME"]])
    logger.info(LOG_MESSAGES["READ_CSV"]["QR_GENERATING"].format(row_counter, qr_code_filename))
    generate_qr_code(row[PROGRAM_SETTINGS["CSV_HEADER"]["FILE_URL"]], qr_code_filename, logo_image_path)


def process_chunk(chunk, base_subfolder, row_counter, start_row, use_numbering, logo_image_path):
    for index, row in chunk.iterrows():
        row_counter += 1
        if should_process_row(row_counter, start_row):
            generate_qr_for_row(row, row_counter, base_subfolder, use_numbering, logo_image_path)
    return row_counter


def process_chunks(file_path, base_subfolder, start_row, chunk_size, use_numbering, logo_image_path):
    row_counter = 0
    for chunk_index, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
        chunk_start = row_counter + 1
        chunk_end = row_counter + len(chunk)
        if chunk_end < start_row:
            row_counter = chunk_end
            continue
        logger.info(LOG_MESSAGES["READ_CSV"]["CHUNK_PROCESS"].format(chunk_index + 1, chunk_start, chunk_end))
        row_counter = process_chunk(chunk, base_subfolder, row_counter, start_row, use_numbering, logo_image_path)


def process_csv_file(file_path, qr_code_directory, logo_image_path, start_row=PROGRAM_SETTINGS["START_ROW"], chunk_size=PROGRAM_SETTINGS["QR_CODE_FILES_PER_DIR"], use_numbering=False):
    logger.info(LOG_MESSAGES["READ_CSV"]["CSV_PROCESS_START"].format(file_path, start_row, chunk_size))
    if not validate_file(file_path, use_numbering):  
        return
    base_subfolder = prepare_subfolder(file_path)
    process_chunks(file_path, base_subfolder, start_row, chunk_size, use_numbering, logo_image_path)
    logger.info(LOG_MESSAGES["READ_CSV"]["CSV_PROCESS_COMPLETE"].format(file_path))


def process_all_csv_files(data_directory, qr_code_directory, img_directory, start_row=PROGRAM_SETTINGS["START_ROW"], chunk_size=PROGRAM_SETTINGS["QR_CODE_FILES_PER_DIR"], use_numbering=False):
    try:
        logo_image_path = get_logo_image_path(img_directory)
        for filename in os.listdir(data_directory):
            if filename.endswith(PROGRAM_SETTINGS["EXTENSION"]["INPUT_FILE"]):
                correct_file_path = os.path.join(data_directory, filename)
                process_csv_file(correct_file_path, qr_code_directory, logo_image_path, start_row, chunk_size, use_numbering)
                start_row = PROGRAM_SETTINGS["START_ROW"]
        return True
    except Exception as e:
        logger.error(LOG_MESSAGES["READ_CSV"]["CSV_READ_ERROR"], exc_info=True)
        return False


def main():
    args = parse_args()
    logger.info(LOG_MESSAGES["READ_CSV"]["START_PROCESS"])
    success = process_all_csv_files(PROGRAM_SETTINGS["DIRECTORY"]["INPUT"], PROGRAM_SETTINGS["DIRECTORY"]["OUTPUT"], PROGRAM_SETTINGS["DIRECTORY"]["IMG"], start_row=args.resume, chunk_size=PROGRAM_SETTINGS["QR_CODE_FILES_PER_DIR"], use_numbering=args.number)
    if success:
        logger.info(LOG_MESSAGES["READ_CSV"]["END_PROCESS"])
        return 0
    else:
        logger.error(LOG_MESSAGES["READ_CSV"]["ERROR_PROCESS"])
        return 1

if __name__ == "__main__":
    sys.exit(main())

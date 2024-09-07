import pytest
from io import StringIO
from src.validate import validate_csv
import pandas as pd


# ダミーのCSVデータを作成するヘルパー関数
def create_test_csv_data(data):
    return StringIO(data)


# 有効なファイル名とURLを持つCSVデータ
@pytest.fixture
def valid_csv_data():
    return create_test_csv_data("ファイル名,URL\n" "image.png,http://example.com\n")


# 無効なファイル名を持つCSVデータ
@pytest.fixture
def invalid_filename_csv_data():
    return create_test_csv_data("ファイル名,URL\n" "image.jpg,http://example.com\n")


# 無効なURLを持つCSVデータ
@pytest.fixture
def invalid_url_csv_data():
    return create_test_csv_data("ファイル名,URL\n" "image.png,invalid_url\n")


# 無効なファイル名とURLの両方を持つCSVデータ
@pytest.fixture
def invalid_both_csv_data():
    return create_test_csv_data("ファイル名,URL\n" "image.jpg,invalid_url\n")


# 空のCSVデータ
@pytest.fixture
def empty_csv_data():
    return create_test_csv_data("")


# 不正なフォーマットのCSVデータ
@pytest.fixture
def malformed_csv_data():
    return create_test_csv_data("無効なデータ")


# 有効なデータのテスト：エラーが返されないことを確認
def test_validate_csv_with_valid_data(valid_csv_data):
    errors = validate_csv(valid_csv_data)
    assert len(errors) == 0, "No errors should be returned for valid data"


# 無効なファイル名のテスト：適切なエラーメッセージが返されることを確認
def test_validate_csv_with_invalid_filename(invalid_filename_csv_data):
    errors = validate_csv(invalid_filename_csv_data)
    assert len(errors) == 1
    assert "拡張子をpngにしてください" in errors[0]


# 無効なURLのテスト：適切なエラーメッセージが返されることを確認
def test_validate_csv_with_invalid_url(invalid_url_csv_data):
    errors = validate_csv(invalid_url_csv_data)
    assert len(errors) == 1
    assert "URLが正しい形式ではありません" in errors[0]


# ファイル名とURLの両方が無効なデータのテスト：適切なエラーメッセージが両方返されることを確認
def test_validate_csv_with_invalid_both(invalid_both_csv_data):
    errors = validate_csv(invalid_both_csv_data)
    assert len(errors) == 2


# 空のデータのテスト：適切なエラーメッセージが返されることを確認
def test_validate_csv_with_empty_data(empty_csv_data):
    errors = validate_csv(empty_csv_data)
    assert len(errors) == 1, "An error should be returned for empty data"
    assert errors[0] == "CSVファイルが空です"


# 不正なフォーマットのデータのテスト：エラーメッセージが返されることを確認
def test_validate_csv_with_malformed_data(malformed_csv_data):
    errors = validate_csv(malformed_csv_data)
    assert len(errors) > 0, "Errors should be returned for malformed data"


# 不正なフォーマットのCSVデータ（ヘッダなし）
@pytest.fixture
def malformed_header_csv_data():
    return create_test_csv_data(
        "image.png,http://example.com\n" "image2.png,http://example2.com\n"
    )


# 列数が不一致のCSVデータ
@pytest.fixture
def mismatched_column_csv_data():
    return create_test_csv_data("ファイル名,URL,余分な列\n" "image.png,http://example.com,余分\n")


# 不正なフォーマットのデータのテスト（ヘッダなし）
def test_validate_csv_with_malformed_header(malformed_header_csv_data):
    errors = validate_csv(malformed_header_csv_data)
    assert len(errors) > 0, "Errors should be returned for malformed header"


# 列数が不一致のデータのテスト
def test_validate_csv_with_mismatched_column(mismatched_column_csv_data):
    errors = validate_csv(mismatched_column_csv_data)
    assert len(errors) > 0, "Errors should be returned for mismatched column count"

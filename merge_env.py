import os
import sys
import argparse
from pathlib import Path
from typing import Sequence

import pytest

ROOT_DIR_PATH = Path(__file__).parent.resolve()

# production
# ----------------------------------------------------------------------
PRODUCTION_DOTENVS_DIR_PATH = ROOT_DIR_PATH / ".envs" / ".production"
PRODUCTION_DOTENV_FILE_PATHS = [
    PRODUCTION_DOTENVS_DIR_PATH / ".django",
    PRODUCTION_DOTENVS_DIR_PATH / ".postgres",
]

# local
# ----------------------------------------------------------------------
LOCAL_DOTENVS_DIR_PATH = ROOT_DIR_PATH / ".envs" / ".local"
LOCAL_DOTENV_FILE_PATH = [
    LOCAL_DOTENVS_DIR_PATH / ".django",
    LOCAL_DOTENVS_DIR_PATH / ".postgres",
]

# test
# ----------------------------------------------------------------------
TEST_DOTENVS_DIR_PATH = ROOT_DIR_PATH / ".envs" / ".test"
TEST_DOTENV_FILE_PATH = [
    TEST_DOTENVS_DIR_PATH / ".django",
    TEST_DOTENVS_DIR_PATH / ".postgres",
]

DOTENV_FILE_PATH = ROOT_DIR_PATH / ".env"

ENVS = ['prod', 'local', 'test']


def merge(
        output_file_path: Path, merged_file_paths: Sequence[Path], append_linesep: bool = True
) -> None:
    with open(output_file_path, "w") as output_file:
        for merged_file_path in merged_file_paths:
            with open(merged_file_path, "r") as merged_file:
                merged_file_content = merged_file.read()
                output_file.write(merged_file_content)
                if append_linesep:
                    output_file.write(os.linesep)


def main():
    parser = argparse.ArgumentParser(description="merges environment")
    parser.add_argument("-e", "--env", type=str, help="env to merge example prod, dev or test")

    args = parser.parse_args()

    if args.env not in ENVS:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.env == ENVS[0]:
        print(f"--> merging {args.env}")
        merge(DOTENV_FILE_PATH, PRODUCTION_DOTENV_FILE_PATHS)
    elif args.env == ENVS[1]:
        print(f"--> merging {args.env}")
        merge(DOTENV_FILE_PATH, LOCAL_DOTENV_FILE_PATH)
    elif args.env == ENVS[2]:
        print(f"--> merging {args.env}")
        merge(DOTENV_FILE_PATH, TEST_DOTENV_FILE_PATH)


@pytest.mark.parametrize("merged_file_count", range(3))
@pytest.mark.parametrize("append_linesep", [True, False])
def test_merge(tmpdir_factory, merged_file_count: int, append_linesep: bool):
    tmp_dir_path = Path(str(tmpdir_factory.getbasetemp()))

    output_file_path = tmp_dir_path / ".env"

    expected_output_file_content = ""
    merged_file_paths = []
    for i in range(merged_file_count):
        merged_file_ord = i + 1

        merged_filename = ".services{}".format(merged_file_ord)
        merged_file_path = tmp_dir_path / merged_filename

        merged_file_content = merged_filename * merged_file_ord

        with open(merged_file_path, "w+") as file:
            file.write(merged_file_content)

        expected_output_file_content += merged_file_content
        if append_linesep:
            expected_output_file_content += os.linesep

        merged_file_paths.append(merged_file_path)

    merge(output_file_path, merged_file_paths, append_linesep)

    with open(output_file_path, "r") as output_file:
        actual_output_file_content = output_file.read()

    assert actual_output_file_content == expected_output_file_content


if __name__ == "__main__":
    main()

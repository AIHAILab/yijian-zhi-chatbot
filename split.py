import logging
from pathlib import Path

import docx

from settings import settings
from setup_logging import setup_logging

logger = logging.getLogger(__name__)


def is_bold(paragraph: docx.text.paragraph.Paragraph) -> bool:  # type: ignore
    for run in paragraph.runs:
        if run.bold:
            return True
    return False


def split_docx(input_dir: str, output_dir: str) -> None:
    try:
        input_dir_path = Path(input_dir)
        if not input_dir_path.is_dir():
            raise FileNotFoundError(f"Input path '{input_dir}' is not a directory.")

        output_dir_path = Path(output_dir)
        output_dir_path.mkdir(parents=True, exist_ok=True)

        current_filename = None
        current_content = ""
        file_counter = 1

        docx_files = sorted(list(input_dir_path.glob("*.docx")))
        if not docx_files:
            raise FileNotFoundError(f"No .docx files found in '{input_dir_path}'.")

        for docx_file in docx_files:
            logger.info(f"Splitting {docx_file.name}...")
            doc = docx.Document(str(docx_file))

            for paragraph in doc.paragraphs:
                if is_bold(paragraph):
                    if current_filename and current_content:
                        filepath = output_dir_path / f"{current_filename}.txt"
                        with filepath.open("w", encoding="utf-8") as f:
                            f.write(f"《夷堅志》{current_content.strip()}")
                    current_filename = f"{file_counter:08d}"
                    file_counter += 1
                    current_content = paragraph.text + "(南宋洪邁撰)："
                elif current_filename:
                    current_content += paragraph.text
        if current_filename and current_content:
            filepath = output_dir_path / f"{current_filename}.txt"
            with filepath.open("w", encoding="utf-8") as f:
                f.write(f"《夷堅志》{current_content.strip()}")

        logger.info(
            f"All Word documents in '{input_dir_path}' have been successfully split and saved to '{output_dir_path}'."
        )
    except FileNotFoundError as e:
        logger.error(f"Word docx file '{input_dir}' not found: {e}")
    except Exception as e:
        logger.error(f"An error occurred: {e}")


def main():
    setup_logging()
    split_docx(settings.data_source_original_dir, settings.data_source_splitted_dir)


if __name__ == "__main__":
    main()

from pathlib import Path

import docx


def is_bold(paragraph: docx.text.paragraph.Paragraph) -> bool:  # type: ignore
    for run in paragraph.runs:
        if run.bold:
            return True
    return False


def split_word(input_path: str, output_path: str) -> None:
    try:
        doc = docx.Document(input_path)
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        current_filename = None
        current_content = ""
        file_counter = 1

        for paragraph in doc.paragraphs:
            if is_bold(paragraph):
                if current_filename and current_content:
                    filepath = output_dir / f"{current_filename}.txt"
                    with filepath.open("w", encoding="utf-8") as f:
                        f.write(f"《夷堅志》南宋洪邁撰\n篇章 {current_content.strip()}")
                current_filename = f"{file_counter:08d}"
                file_counter += 1
                current_content = paragraph.text + "\n"
            elif current_filename:
                current_content += paragraph.text + "\n"
        if current_filename and current_content:
            filepath = output_dir / f"{current_filename}.txt"
            with filepath.open("w", encoding="utf-8") as f:
                f.write(f"《夷堅志》南宋洪邁撰\n篇章 {current_content.strip()}")

        print(f"Word document has been successfully split and saved to '{output_dir}' directory.")

    except FileNotFoundError:
        print(f"Error: Word document '{input_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    input_path = "data/original/yijian_zhi.docx"
    output_path = "data/splitted"
    split_word(input_path, output_path)

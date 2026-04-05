import csv
from pathlib import Path

def collect_fieldnames(rows):

    fieldnames = list(rows[0].keys())

    for row in rows[1:]:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    return fieldnames


def save_dataset_as_csv(rows, output_path):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        output.write_text("", encoding="utf-8")
        return output

    fieldnames = collect_fieldnames(rows)

    with output.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()

        for row in rows:
            normalized_row = {field: row.get(field, "") for field in fieldnames}
            writer.writerow(normalized_row)

    return output

import csv
from pathlib import Path


DEFAULT_PRIORITY_FIELDS = ["titol", "url", "estat", "pdfs"]


def build_fieldnames(rows):
    seen = set()
    extra_fields = []

    for row in rows:
        for key in row.keys():
            if key not in seen and key not in DEFAULT_PRIORITY_FIELDS:
                seen.add(key)
                extra_fields.append(key)

    return DEFAULT_PRIORITY_FIELDS + sorted(extra_fields)


def save_dataset_as_csv(rows, output_path):
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    if not rows:
        output.write_text("", encoding="utf-8")
        return output

    fieldnames = build_fieldnames(rows)

    with output.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()

        for row in rows:
            normalized_row = {field: row.get(field, "") for field in fieldnames}
            writer.writerow(normalized_row)

    return output

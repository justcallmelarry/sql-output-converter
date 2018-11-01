from io import StringIO
from typing import TextIO
import csv
import sys


class SqlOutputConverter:
    def __init__(self) -> None:
        self.encoding = 'latin-1'
        self.delimiter = ','
        self.output_filename = 'output'

    def to_csv(self, sql_output: TextIO) -> None:
        with open(
            f'{self.output_filename}.csv',
            'w',
            newline='',
            encoding=self.encoding
        ) as output_file:
            writer = csv.writer(
                output_file,
                delimiter=self.delimiter,
                quotechar='"'
            )
            for row in sql_output:
                if row.startswith('+'):
                    continue
                row = row[2:-2].strip()
                if row == '':
                    continue
                output_row = list(csv.reader(
                    StringIO(row),
                    delimiter='|',
                    quotechar='\'',
                    skipinitialspace=True
                ))
                scrubbed_output_row = [
                    self._format_output(x) for x in output_row[0]
                ]
                writer.writerow(scrubbed_output_row)

    def _format_output(self, value: str) -> str:
        return value.strip().encode(
            self.encoding,
            errors='ignore'
        ).decode(self.encoding)


if __name__ == '__main__':
    csv.field_size_limit(sys.maxsize)
    SOC = SqlOutputConverter()
    if '-d' in sys.argv:
        SOC.delimiter = ';'
    with open(sys.argv[1]) as sql_output:
        filename = sys.argv[1][:sys.argv[1].rfind('.')]
        SOC.output_filename = filename
        SOC.to_csv(sql_output)

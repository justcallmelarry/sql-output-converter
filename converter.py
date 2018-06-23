from io import StringIO
import csv
import sys


class SqlOutputConverter:
    def __init__(self):
        self.encoding = 'latin-1'
        self.delimiter = ';'
        self.output_filename = 'output'

    class _Capturing(list):
        '''
        class for capturing the output from functions
        '''
        def __enter__(self):
            self._stdout = sys.stdout
            sys.stdout = self._stringio = StringIO()
            return self

        def __exit__(self, *args):
            self.extend(self._stringio.getvalue().splitlines())
            del self._stringio
            sys.stdout = self._stdout

    def to_csv(self, sql_output):
        with self._Capturing() as cleaned_output:
            for row in sql_output:
                if row.startswith('+'):
                    continue
                self._output(row[2:-2].strip())
        test = csv.reader(cleaned_output, delimiter='|', quotechar='\'', skipinitialspace=True)
        with open(f'{self.output_filename}.csv', 'w', newline='', encoding=self.encoding) as output_file:
            writer = csv.writer(output_file, delimiter=self.delimiter, quotechar='"')
            for row in test:
                row = [self._format_output(x) for x in row]
                writer.writerow(row)

    def _format_output(self, value):
        return value.strip().encode(self.encoding, errors='ignore').decode(self.encoding)

    @staticmethod
    def _output(*message: str) -> None:
        sys.stdout.write('{}\n'.format(' '.join(message)))


if __name__ == '__main__':
    SOC = SqlOutputConverter()
    SOC.delimiter = ','
    with open(sys.argv[1]) as sql_output:
        filename = sys.argv[1][:sys.argv[1].rfind('.')]
        SOC.output_filename = filename
        SOC.to_csv(sql_output)

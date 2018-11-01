# sql-output-converter
A simple converter for converting the table outputted by sql to a csv file.
Currently needs the columns that might contain a pipe in the value to be quoted _(`quote(column)`)_ in order for it to work properly.

Uses the csv module to quickly sort the data and then exporting it as a csv.

I often do reports straight from the command line via mysql, and this helps me share it in a format that is easier for people to work with.


### Usage
```
$ python converter.py input-text.txt [-d]
```

The `-d` option changes the delimiter in the file from `,` to `;` (european excel standard)

#### Requires Python 3.6

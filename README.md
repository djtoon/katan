# Katan : Small in hebrew
Python minifying HTML website

### Simple tool using some lib's to help package a website for distribution.

scans directory for html or js files and makes them ready for uploading to production servers:
- minify html code
- minify js files and html <script> tags
- removes inline css styles into new css file ( adds link to stylesheet in head )


### Install
```
python setup.py install
```

### Running
```
python katan.py -i <input directory> -o <output directory>
```
### Requires
- htmlmin
- bs4
- jsmin

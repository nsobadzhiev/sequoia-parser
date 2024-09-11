# Sequoia companies parser

Scrapes Sequoia capital's website, parses all the companies they invested in (currently only the ones that IPO'ed) and generates a CSV file with their information.

Their website provides good filtering options that can also be supplied as parameters to the URL, which makes it easy to work with different set of companies - not just ones that did an IPO. To do that, open the website, select your filters in the companies page. Once you're done, just copy the URL you see in the address bar and use it in this script:

```python
url = 'https://www.sequoiacap.com/our-companies/?_stage_current=ipo'
```

Then just run the `parse_companies` script:

```commandline
python parse_companies.py
```

## Dependencies

You can install the dependencies needed to run this script via poetry:

```commandline
poetry install
```

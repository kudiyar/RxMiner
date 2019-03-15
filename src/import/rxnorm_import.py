import os
import re
import urllib2
import boto
from boto.s3.key import Key
import requests

"""
This file crawl RxNorm weekly updates from NIH's webpage using regex pattern and downloaded them into the S3 bucket.
"""

def rxnorm_crawler():
    """
    Crawl RxNorm weekly updates from NIH's webpage and store them in S3 bucket.
    """
    # Target webpage
    weburls=[
        'https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html',
        'https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormarchive.html'
        ]
    for weburl in weburls:
        # Get contents of webpage
        conn = urllib2.urlopen(weburl)
        html = conn.read()
        # Find urls of all RxNorm files
        pattern = '<a\s*href=[\'|"](.*?/kss/rxnorm/RxNorm_full_\d+.zip)[\'|"]>'
        rxnorm_urls = re.findall(pattern, html)
        for url in rxnorm_urls:
            r = requests.get(url)
            if r.status_code == 200:
                #upload the file
                file_name = re.findall('.*?(\d+.zip)', url)[0]
                k = Key(bucket)
                k.key = 'rxnorm/' + file_name
                k.content_type = r.headers['content-type']
                k.set_contents_from_string(r.content)
    # Need to add cookies information

if __name__ == "__main__":
    # Connect to the s3 bucket
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID', 'default')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'default')
    conn = boto.connect_s3(aws_access_key, aws_secret_access_key)
    bucket_name = os.getenv('AWS_BUCKET_NAME', 'default')
    # Setup the bucket
    bucket = conn.get_bucket(bucket_name)
    rxnorm_crawler()
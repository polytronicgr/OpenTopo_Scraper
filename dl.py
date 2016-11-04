import os
import csv
import urllib2
import requests


def get_OTids():

    IDs = []

    with open('cosmo_with_lidar.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        next(reader)
        next(reader)
        for i, row in enumerate(reader):
            if row[6]:
                IDs.append(row[6])

        return list(set(IDs))


def get_short_name(ID):
    base_URL = ('http://opentopo.sdsc.edu/datasetMetadata?otCollectionID={0}&' +
                'format=text')

    ID = ID[:2] + ID[5:]

    URL = base_URL.format(ID)

    metadata = urllib2.urlopen(URL).read(2000)
    metadata = metadata.split('\n')

    for line in metadata:
        if 'Short Name:' in line:
            return line.split(': ')[1].strip()


def build_URLs(short_name):
    '''
    returns a tuple of urls to the bulk pointcloud and bulk raster links
    for a give shortname. Index 0 is the pointcloud (always valid) and Index 1
    is the raster (does not always exist)
    '''
    base_URL_rast = 'https://cloud.sdsc.edu/v1/AUTH_opentopography/Raster/{0}'
    base_URL_pc = 'https://cloud.sdsc.edu/v1/AUTH_opentopography/PC_Bulk/{0}'

    return (base_URL_pc.format(short_name), base_URL_rast.format(short_name))


def test_URLs(URLs):
    '''
    Test if the converted urls are valid.
    returns a tuple of bools with true == valid url and false == invalid.
    Index 0 is the pointcloud (always valid) and Index 1
    is the raster (does not always exist)
    '''
    result = []
    for URL in URLs:
        request = requests.get(URL)
        if request.status_code < 400:
            result.append(True)
        else:
            result.append(False)

    return tuple(result)


def download(URL):
    pass


print test_URLs(build_URLs(get_short_name('OTLAS.082013.26910.1')))

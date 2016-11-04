import os
import csv
import urllib2


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


def build_URL(short_name):
    base_URL = 'https://cloud.sdsc.edu/v1/AUTH_opentopography/Raster/{0}'

    return base_URL.format(short_name)


def download(URL):
    pass


print build_URL(get_short_name('OTLAS.082013.26910.1'))

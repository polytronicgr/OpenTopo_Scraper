import os
import csv
import urllib2
import requests


def get_OTids():
    '''
    Return a list of all the opentopo IDs in the data file.
    needs to be made modular.
    '''

    IDs = []

    with open('cosmo_with_lidar.csv', 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        next(reader)
        next(reader)
        for i, row in enumerate(reader):
            if row[6]:
                IDs.append(row[6])

        return list(set(IDs))


def metadata_URL(ID):
    '''
    Build URL to the plaintext metadata at opentopo.
    '''
    base_URL = ('http://opentopo.sdsc.edu/datasetMetadata?otCollectionID={0}&' +
                'format=text')

    ID = ID[:2] + ID[5:]

    return base_URL.format(ID)


def get_short_name(ID):
    '''
    return the shortname for a given ID.
    '''
    URL = metadata_URL(ID)

    metadata = urllib2.urlopen(URL).read(2000)
    metadata = metadata.split('\n')

    for line in metadata:
        if 'Short Name:' in line:
            return line.split(': ')[1].strip()


def check_south(proj4):
    '''
    Check if a proj4 string has the south flag. Returns true if it is a
    utm south zone, false if not.
    '''
    if 'south' in proj4.lower():
        return True
    else:
        return False


def get_UTM_zone(EPSG):
    '''
    Use spatialreference.org to convert a EPSG code into a UTM zone.
    returns a tuple with the zone number and a boolean indicating if
    it is southern hemisphere (True) or northern (False)
    '''
    URL = 'http://spatialreference.org/ref/epsg/{0}/proj4/'.format(EPSG)

    proj4 = urllib2.urlopen(URL).read()
    south = check_south(proj4)

    return (proj4.split('+zone=')[1].split()[0].strip(), south)


def get_EPSG_code(ID):
    '''
    Assumes horizontal EPSG code is always reported first
    '''
    URL = metadata_URL(ID)

    metadata = urllib2.urlopen(URL).read(2000)
    metadata = metadata.split('\n')

    for line in metadata:
        if 'EPSG' in line:
            EPSG_str = line.split('[EPSG:')[1].strip()
            # this parses out the EPSG code
            return ''.join([s for s in EPSG_str if s.isdigit()])


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
    Index 0 is the pointcloud and Index 1 is the raster.
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


print get_UTM_zone(get_EPSG_code('OTLAS.082013.26910.1'))
#print test_URLs(build_URLs(get_short_name('OTLAS.082013.26910.1')))

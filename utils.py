from urllib.error import HTTPError
from urllib.request import urlretrieve
from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord
import tensorflow as tf

Vizier.ROW_LIMIT = -1  # enable unlimited length queries to ViZieR

def download_hyperleda_cat(out_loc):
    """
    Downloads the HyperLEDA catalog from ViZieR, the main online repository for astronomical data

    :param out_loc: location to write catalog to
    :return: None
    """

    print("Downloading HyperLEDA catalog")
    hl_source = Vizier.get_catalogs("VII/237/pgc")[0]
    hl_source.convert_bytestring_to_unicode()
    hl_source = hl_source.to_pandas()  # astropy tables are awful

    # this could take a while, has to parse 1M
    print("Parsing...")
    hl_coo = SkyCoord(
        hl_source.RAJ2000.values.astype(str),
        hl_source.DEJ2000.values.astype(str),
        unit=("hourangle", "deg"),
    )

    hl_source["ra"] = hl_coo.ra.value
    hl_source["dec"] = hl_coo.dec.value

    hl_source.to_csv(out_loc, index=False)
    return

def compute_optimal_platescale(imgsize, ld25, pad_factor=1.2):
    """
    Helper routine to compute the plate scale required to fit the galaxy in a stamp of fixed size based on the log(D25)
    param provided in HyperLEDA.

    :param imgsize: side length of square image, in pix
    :param ld25: log(D25) measure from HyperLEDA catalog (in log(0.1*arcmin))
    :param pad_factor: multiplicative factor to add border around galaxy
    :return: plate scale in arcsec/pix
    """
    # ld25 is in log10(0.1*arcmin), platescale in arcsec/pix
    plate_scale = pad_factor * (60 * 0.1 * (10 ** ld25) / imgsize)
    return plate_scale


def get_sdss_stamp(ra, dec, pscale, size, out_loc, verbose=False):
    """
    Simple routine to retrieve SDSS stamps from SkyServer DR16 using GET requests.
    Should be careful to not overuse this resource!

    :param verbose:
    :param ra: right ascension of centre of stamp, in degrees
    :param dec: declination of centre of stamp, in degrees
    :param pscale: plate scale in arcsec/pix
    :param size: side length of pixel stamp
    :param out_dir: directory to store retrieved image in
    :return: path to output file.
    """

    try:
        formatted_url =  "http://skyserver.sdss.org/dr16/SkyServerWS/ImgCutout/getjpeg?ra={}&dec={}&scale={}&width={}&height={}".format(
                ra, dec, pscale, size, size)
        print(formatted_url)
        _ = urlretrieve(
           formatted_url, out_loc)

    except HTTPError as err:
        if verbose:
            print(err)
        return None

    print("Retrieved {}".format(out_loc.split("/")[-1]))
    return out_loc

def load_image_from_path(path):
    """
    Decode a jpg image from the string filepath

    :param path: Path to image
    :return: 3D image tensor
    """
    raw_img = tf.io.read_file(path)
    img = tf.image.decode_jpeg(raw_img, channels=3)
    img = tf.image.convert_image_dtype(img, 'float32') # pre-normalises to 0,1

    return img.numpy()
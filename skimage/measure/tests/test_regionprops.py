from numpy.testing import assert_array_equal, assert_almost_equal, \
    assert_array_almost_equal, assert_raises
import numpy as np
import math

from skimage.measure._regionprops import regionprops, PROPS, perimeter


SAMPLE = np.array(
    [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
     [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
     [1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0],
     [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1],
     [0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1]]
)
INTENSITY_SAMPLE = SAMPLE.copy()
INTENSITY_SAMPLE[1, 9:11] = 2


def test_unsupported_dtype():
    assert_raises(TypeError, regionprops, np.zeros((10, 10), dtype=np.double))


def test_all_props():
    props = regionprops(SAMPLE, 'all', INTENSITY_SAMPLE)[0]
    for prop in PROPS:
        assert prop in props


def test_area():
    area = regionprops(SAMPLE, ['Area'])[0]['Area']
    assert area == np.sum(SAMPLE)


def test_bbox():
    bbox = regionprops(SAMPLE, ['BoundingBox'])[0]['BoundingBox']
    assert_array_almost_equal(bbox, (0, 0, SAMPLE.shape[0], SAMPLE.shape[1]))

    SAMPLE_mod = SAMPLE.copy()
    SAMPLE_mod[:, -1] = 0
    bbox = regionprops(SAMPLE_mod, ['BoundingBox'])[0]['BoundingBox']
    assert_array_almost_equal(bbox, (0, 0, SAMPLE.shape[0], SAMPLE.shape[1]-1))


def test_central_moments():
    mu = regionprops(SAMPLE, ['CentralMoments'])[0]['CentralMoments']
    #: determined with OpenCV
    assert_almost_equal(mu[0,2], 436.00000000000045)
    # different from OpenCV results, bug in OpenCV
    assert_almost_equal(mu[0,3], -737.333333333333)
    assert_almost_equal(mu[1,1], -87.33333333333303)
    assert_almost_equal(mu[1,2], -127.5555555555593)
    assert_almost_equal(mu[2,0], 1259.7777777777774)
    assert_almost_equal(mu[2,1], 2000.296296296291)
    assert_almost_equal(mu[3,0], -760.0246913580195)


def test_centroid():
    centroid = regionprops(SAMPLE, ['Centroid'])[0]['Centroid']
    # determined with MATLAB
    assert_array_almost_equal(centroid, (5.66666666666666, 9.444444444444444))


def test_convex_area():
    area = regionprops(SAMPLE, ['ConvexArea'])[0]['ConvexArea']
    # determined with MATLAB
    assert area == 124


def test_convex_image():
    img = regionprops(SAMPLE, ['ConvexImage'])[0]['ConvexImage']
    # determined with MATLAB
    ref = np.array(
        [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
         [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
         [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
         [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    )
    assert_array_equal(img, ref)


def test_coordinates():
    sample = np.zeros((10, 10), dtype=np.int8)
    coords = np.array([[3, 2], [3, 3], [3, 4]])
    sample[coords[:, 0], coords[:, 1]] = 1
    prop_coords = regionprops(sample, ['Coordinates'])[0]['Coordinates']
    assert_array_equal(prop_coords, coords)


def test_eccentricity():
    eps = regionprops(SAMPLE, ['Eccentricity'])[0]['Eccentricity']
    assert_almost_equal(eps, 0.814629313427)

    img = np.zeros((5, 5), dtype=np.int)
    img[2, 2] = 1
    eps = regionprops(img, ['Eccentricity'])[0]['Eccentricity']
    assert_almost_equal(eps, 0)


def test_equiv_diameter():
    diameter = regionprops(SAMPLE, ['EquivDiameter'])[0]['EquivDiameter']
    # determined with MATLAB
    assert_almost_equal(diameter, 9.57461472963)


def test_euler_number():
    en = regionprops(SAMPLE, ['EulerNumber'])[0]['EulerNumber']
    assert en == 0

    SAMPLE_mod = SAMPLE.copy()
    SAMPLE_mod[7, -3] = 0
    en = regionprops(SAMPLE_mod, ['EulerNumber'])[0]['EulerNumber']
    assert en == -1


def test_extent():
    extent = regionprops(SAMPLE, ['Extent'])[0]['Extent']
    assert_almost_equal(extent, 0.4)


def test_hu_moments():
    hu = regionprops(SAMPLE, ['HuMoments'])[0]['HuMoments']
    ref = np.array([
        3.27117627e-01,
        2.63869194e-02,
        2.35390060e-02,
        1.23151193e-03,
        1.38882330e-06,
        -2.72586158e-05,
        6.48350653e-06
    ])
    # bug in OpenCV caused in Central Moments calculation?
    assert_array_almost_equal(hu, ref)


def test_image():
    img = regionprops(SAMPLE, ['Image'])[0]['Image']
    assert_array_equal(img, SAMPLE)


def test_filled_area():
    area = regionprops(SAMPLE, ['FilledArea'])[0]['FilledArea']
    assert area == np.sum(SAMPLE)

    SAMPLE_mod = SAMPLE.copy()
    SAMPLE_mod[7, -3] = 0
    area = regionprops(SAMPLE_mod, ['FilledArea'])[0]['FilledArea']
    assert area == np.sum(SAMPLE)


def test_filled_image():
    img = regionprops(SAMPLE, ['FilledImage'])[0]['FilledImage']
    assert_array_equal(img, SAMPLE)


def test_major_axis_length():
    length = regionprops(SAMPLE, ['MajorAxisLength'])[0]['MajorAxisLength']
    # MATLAB has different interpretation of ellipse than found in literature,
    # here implemented as found in literature
    assert_almost_equal(length, 16.7924234999)


def test_max_intensity():
    intensity = regionprops(SAMPLE, ['MaxIntensity'], INTENSITY_SAMPLE
                            )[0]['MaxIntensity']
    assert_almost_equal(intensity, 2)


def test_mean_intensity():
    intensity = regionprops(SAMPLE, ['MeanIntensity'], INTENSITY_SAMPLE
                            )[0]['MeanIntensity']
    assert_almost_equal(intensity, 1.02777777777777)


def test_min_intensity():
    intensity = regionprops(SAMPLE, ['MinIntensity'], INTENSITY_SAMPLE
                            )[0]['MinIntensity']
    assert_almost_equal(intensity, 1)


def test_minor_axis_length():
    length = regionprops(SAMPLE, ['MinorAxisLength'])[0]['MinorAxisLength']
    # MATLAB has different interpretation of ellipse than found in literature,
    # here implemented as found in literature
    assert_almost_equal(length, 9.739302807263)


def test_moments():
    m = regionprops(SAMPLE, ['Moments'])[0]['Moments']
    #: determined with OpenCV
    assert_almost_equal(m[0,0], 72.0)
    assert_almost_equal(m[0,1], 408.0)
    assert_almost_equal(m[0,2], 2748.0)
    assert_almost_equal(m[0,3], 19776.0)
    assert_almost_equal(m[1,0], 680.0)
    assert_almost_equal(m[1,1], 3766.0)
    assert_almost_equal(m[1,2], 24836.0)
    assert_almost_equal(m[2,0], 7682.0)
    assert_almost_equal(m[2,1], 43882.0)
    assert_almost_equal(m[3,0], 95588.0)


def test_normalized_moments():
    nu = regionprops(SAMPLE, ['NormalizedMoments'])[0]['NormalizedMoments']
    #: determined with OpenCV
    assert_almost_equal(nu[0,2], 0.08410493827160502)
    assert_almost_equal(nu[1,1], -0.016846707818929982)
    assert_almost_equal(nu[1,2], -0.002899800614433943)
    assert_almost_equal(nu[2,0], 0.24301268861454037)
    assert_almost_equal(nu[2,1], 0.045473992910668816)
    assert_almost_equal(nu[3,0], -0.017278118992041805)


def test_orientation():
    orientation = regionprops(SAMPLE, ['Orientation'])[0]['Orientation']
    # determined with MATLAB
    assert_almost_equal(orientation, 0.10446844651921)
    # test correct quadrant determination
    orientation2 = regionprops(SAMPLE.T, ['Orientation'])[0]['Orientation']
    assert_almost_equal(orientation2, math.pi / 2 - orientation)
    # test diagonal regions
    diag = np.eye(10, dtype=int)
    orientation_diag = regionprops(diag, ['Orientation'])[0]['Orientation']
    assert_almost_equal(orientation_diag, -math.pi / 4)
    orientation_diag = regionprops(np.flipud(diag), ['Orientation']
                                  )[0]['Orientation']
    assert_almost_equal(orientation_diag, math.pi / 4)
    orientation_diag = regionprops(np.fliplr(diag), ['Orientation']
                                  )[0]['Orientation']
    assert_almost_equal(orientation_diag, math.pi / 4)
    orientation_diag = regionprops(np.fliplr(np.flipud(diag)), ['Orientation']
                                  )[0]['Orientation']
    assert_almost_equal(orientation_diag, -math.pi / 4)


def test_perimeter():
    per = regionprops(SAMPLE, ['Perimeter'])[0]['Perimeter']
    assert_almost_equal(per, 55.2487373415)

    per = perimeter(SAMPLE.astype('double'), neighbourhood=8)
    assert_almost_equal(per, 46.8284271247)


def test_solidity():
    solidity = regionprops(SAMPLE, ['Solidity'])[0]['Solidity']
    # determined with MATLAB
    assert_almost_equal(solidity, 0.580645161290323)


def test_weighted_central_moments():
    wmu = regionprops(SAMPLE, ['WeightedCentralMoments'], INTENSITY_SAMPLE
                     )[0]['WeightedCentralMoments']
    ref = np.array(
        [[  7.4000000000e+01, -2.1316282073e-13,  4.7837837838e+02,
            -7.5943608473e+02],
         [  3.7303493627e-14, -8.7837837838e+01, -1.4801314828e+02,
            -1.2714707125e+03],
         [  1.2602837838e+03,  2.1571526662e+03,  6.6989799420e+03,
             1.5304076361e+04],
         [ -7.6561796932e+02, -4.2385971907e+03, -9.9501164076e+03,
            -3.3156729271e+04]]
    )
    np.set_printoptions(precision=10)
    assert_array_almost_equal(wmu, ref)


def test_weighted_centroid():
    centroid = regionprops(SAMPLE, ['WeightedCentroid'], INTENSITY_SAMPLE
                           )[0]['WeightedCentroid']
    assert_array_almost_equal(centroid, (5.540540540540, 9.445945945945))


def test_weighted_hu_moments():
    whu = regionprops(SAMPLE, ['WeightedHuMoments'], INTENSITY_SAMPLE
                     )[0]['WeightedHuMoments']
    ref = np.array([
        3.1750587329e-01,
        2.1417517159e-02,
        2.3609322038e-02,
        1.2565683360e-03,
        8.3014209421e-07,
        -3.5073773473e-05,
        6.7936409056e-06
    ])
    assert_array_almost_equal(whu, ref)


def test_weighted_moments():
    wm = regionprops(SAMPLE, ['WeightedMoments'], INTENSITY_SAMPLE
                     )[0]['WeightedMoments']
    ref = np.array(
        [[  7.4000000000e+01, 4.1000000000e+02, 2.7500000000e+03,
            1.9778000000e+04],
         [  6.9900000000e+02, 3.7850000000e+03, 2.4855000000e+04,
            1.7500100000e+05],
         [  7.8630000000e+03, 4.4063000000e+04, 2.9347700000e+05,
            2.0810510000e+06],
         [  9.7317000000e+04, 5.7256700000e+05, 3.9007170000e+06,
            2.8078871000e+07]]
    )
    assert_array_almost_equal(wm, ref)


def test_weighted_normalized_moments():
    wnu = regionprops(SAMPLE, ['WeightedNormalizedMoments'], INTENSITY_SAMPLE
                     )[0]['WeightedNormalizedMoments']
    ref = np.array(
        [[       np.nan,        np.nan,  0.0873590903, -0.0161217406],
         [       np.nan, -0.0160405109, -0.0031421072, -0.0031376984],
         [  0.230146783,  0.0457932622,  0.0165315478,  0.0043903193],
         [-0.0162529732, -0.0104598869, -0.0028544152, -0.0011057191]]
    )
    assert_array_almost_equal(wnu, ref)


if __name__ == "__main__":
    from numpy.testing import run_module_suite
    run_module_suite()

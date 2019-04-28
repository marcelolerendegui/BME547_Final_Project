import pytest
import os


@pytest.mark.parametrize(
    "im_fname, expected",
    [
        ('image1.jpg', True),
        ('image1.png', True),
        ('image1.tif', True),
        ('not_image.jpg', False),
        ('not_image.png', False),
        ('not_image.tif', False),
    ]
)
def test_is_image(im_fname, expected):
    from core.img_proc_core import is_image

    path = os.path.realpath(__file__)
    cur_dir = os.path.split(path)[0]
    im_fname = os.path.join(cur_dir, im_fname)

    f = open(im_fname, 'rb')
    assert is_image(f) == expected


@pytest.mark.parametrize(
    "im_fname, expected",
    [
        ('image1.jpg', '123x456'),
        ('image1.png', '123x456'),
        ('image1.tif', '123x456'),
    ]
)
def test_get_image_size(im_fname, expected):
    from core.img_proc_core import get_image_size

    path = os.path.realpath(__file__)
    cur_dir = os.path.split(path)[0]
    im_fname = os.path.join(cur_dir, im_fname)

    f = open(im_fname, 'rb')
    assert get_image_size(f) == expected


@pytest.mark.parametrize(
    "im_fname, expected",
    [
        ('image1.jpg', 'JPEG'),
        ('image1.png', 'PNG'),
        ('image1.tif', 'TIFF'),
    ]
)
def test_get_image_format(im_fname, expected):
    from core.img_proc_core import get_image_format

    path = os.path.realpath(__file__)
    cur_dir = os.path.split(path)[0]
    im_fname = os.path.join(cur_dir, im_fname)

    f = open(im_fname, 'rb')
    assert get_image_format(f) == expected


@pytest.mark.parametrize(
    "algorithm, expected",
    [
        ('Histogram Equalization', True),
        ('Contrast Stretching', True),
        ('Log Compression', True),
        ('Contrast Invert', True),
        ('No Algorithm', True),
        ('HistogramEqualization', False),
        ('histogram equalization', False),
        ('Contrast invert', False),
    ]
)
def test_is_valid_algorithm(algorithm, expected):
    from core.img_proc_core import is_valid_algorithm
    assert is_valid_algorithm(algorithm) == expected


@pytest.mark.parametrize(
    "im_fname",
    [
        ('image1.jpg'),
        ('image1.png'),
        ('image1.tif'),
    ]
)
def test_transform_image_no_algorithm(im_fname):
    from core.img_proc_core import transform_image

    path = os.path.realpath(__file__)
    cur_dir = os.path.split(path)[0]
    im_fname = os.path.join(cur_dir, im_fname)

    f = open(im_fname, 'rb')

    dout = transform_image(f, 'No Algorithm').read()
    f.seek(0)
    din = f.read()
    assert dout == din

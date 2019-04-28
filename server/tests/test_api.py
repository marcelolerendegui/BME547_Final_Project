import pytest


@pytest.mark.parametrize(
    "upload_img_dict, success",
    [
        (
            {
                'filename': 1,
                'description': 'description',
                'data': 'data',
                'user_hash': 'user_hash'
            },
            False
        ),
        (
            {
                'filename': 'filename',
                'description': ['description'],
                'data': 'data',
                'user_hash': 'user_hash'
            },
            False
        ),
        (
            {
                'filename': 'filename',
                'description': 'description',
                'data': 2.0,
                'user_hash': 'user_hash'
            },
            False
        ),
        (
            {
                'filename': 'filename',
                'description': 'description',
                'data': 'data',
                'user_hash': b'user_hash'
            },
            False
        ),
        (
            {
                'filename': 'filename',
                'description': 'description',
                'data': 'dHB5ZXMgb2sgYnV0IGRhdGEgbm90IGI2NCBpbWFnZQ==',
                'user_hash': 'user_hash'
            },
            False
        ),
    ]

)
def test_upload_image(upload_img_dict, success):
    from server.api import upload_image
    ret = upload_image(upload_img_dict)

    assert ret.get('success') == success


@pytest.mark.parametrize(
    "upload_mult_img_dict, success",
    [
        (
            {
                'filename': 1,
                'data': 'data',
                'user_hash': 'user_hash'
            },
            False
        ),
        (
            {
                'filename': 'filename',
                'data': b'data',
                'user_hash': 'user_hash'
            },
            False
        ),
        (
            {
                'filename': 'filename',
                'data': 2.0,
                'user_hash': 'user_hash'
            },
            False
        ),
        (
            {
                'filename': 'filename',
                'data': 'data',
                'user_hash': b'user_hash'
            },
            False
        ),
        (
            {
                'filename': 'filename',
                'data': 'dHB5ZXMgb2sgYnV0IGRhdGEgbm90IGI2NCBpbWFnZQ==',
                'user_hash': 'user_hash'
            },
            False
        ),
    ]

)
def test_upload_multiple_images(upload_mult_img_dict, success):
    from server.api import upload_multiple_images
    ret = upload_multiple_images(upload_mult_img_dict)

    assert ret.get('success') == success


@pytest.mark.parametrize(
    "user_hash, success",
    [
        (1,  False),
        (1.0,  False),
        (['hash1', 'hash2'],  False),
    ]
)
def test_get_image_info(user_hash, success):
    from server.api import get_image_info
    ret = get_image_info(user_hash)

    assert ret.get('success') == success


@pytest.mark.parametrize(
    "edit_image_description_dict, success",
    [
        (
            {
                'image_id': 1,
                'description': 'description',
                'user_hash': 'user_hash'
            },
            False
        ),
        (
            {
                'image_id': 'image_id',
                'description': 1.0,
                'user_hash': 'user_hash'
            },
            False
        ),
        (
            {
                'image_id': 'image_id',
                'description': 'description',
                'user_hash': ['user_hash']
            },
            False
        ),
    ]
)
def test_edit_image_description_dict(edit_image_description_dict, success):
    from server.api import edit_image_description
    ret = edit_image_description(edit_image_description_dict)

    assert ret.get('success') == success


@pytest.mark.parametrize(
    "edit_image_filename_dict, success",
    [
        (
            {
                'image_id': 1,
                'filename': 'filename',
                'user_hash': 'user_hash'
            },
            False
        ),
        (
            {
                'image_id': 'image_id',
                'filename': 1.0,
                'user_hash': 'user_hash'
            },
            False
        ),
        (
            {
                'image_id': 'image_id',
                'filename': 'filename',
                'user_hash': ['user_hash']
            },
            False
        ),
    ]
)
def test_edit_image_filename(edit_image_filename_dict, success):
    from server.api import edit_image_filename
    ret = edit_image_filename(edit_image_filename_dict)

    assert ret.get('success') == success


@pytest.mark.parametrize(
    "download_images_dict, success",
    [
        (
            {
                'image_ids': 1,
                'format': 'filename',
                'user_hash': 'user_hash'
            },
            False
        ),
        (
            {
                'image_ids': ['image_id'],
                'filename': 1.0,
                'user_hash': 'user_hash'
            },
            False
        ),
        (
            {
                'image_ids': ['image_id'],
                'filename': 'filename',
                'user_hash': ['user_hash']
            },
            False
        ),
    ]
)
def test_download(download_images_dict, success):
    from server.api import download
    ret = download(download_images_dict)

    assert ret.get('success') == success


@pytest.mark.parametrize(
    "names, name, ext, expected",
    [
        (
            [],
            'filename',
            'ext',
            'filename.ext'
        ),
        (
            ['filename.ext'],
            'filename',
            'ext',
            'filename1.ext'
        ),
        (
            [
                'filename1.ext',
                'filename2.ext',
                'filename3.ext',
                'filename4.ext',
            ],
            'filename',
            'ext',
            'filename.ext'
        ),
        (
            [
                'filename1.ext',
                'filename.ext',
                'filename3.ext',
                'filename4.ext',
            ],
            'filename',
            'ext',
            'filename2.ext'
        ),
        (
            [
                'filename.ext',
                'filename1.ext',
                'filename2.ext',
                'filename3.ext',
                'filename4.ext',
                'filename5.ext',
                'filename6.ext',
                'filename7.ext',
                'filename8.ext',
            ],
            'filename',
            'ext',
            'filename9.ext'
        ),
        (
            [
                'filename.ext',
                'filename1.ext',
                'filename2.ext',
                'filename3.ext2',
                'filename4.ext',
                'filename5.ext',
                'filename6.ext',
                'filename7.ext',
                'filename8.ext',
            ],
            'filename',
            'ext',
            'filename3.ext'
        ),
    ]
)
def test_get_unique_filename(names, name, ext, expected):
    from server.api import get_unique_filename
    unique_name = get_unique_filename(names, name, ext)

    assert unique_name == expected


@pytest.mark.parametrize(
    "image_process_dict, success",
    [
        (
            {
                'image_id': ['image_id'],
                'algorithm':'algorithm',
                'out_image_format': 'format',
                'out_image_filename':'name',
                'user_hash': 'user_hash',
            },
            False
        ),
        (
            {
                'image_ID': 'image_id',
                'algorithm': 'algorithm',
                'out_image_format': 'format',
                'out_image_filename': 'name',
                'user_hash': 'user_hash',
            },
            False
        ),
        (
            {
                'image_id': 'image_id',
                'out_image_format': 'format',
                'out_image_filename': 'name',
                'user_hash': 'user_hash',
            },
            False
        ),
        (
            {
                'image_id': 'image_id',
                'algorithm': 1,
                'out_image_format': 'format',
                'out_image_filename': 'name',
                'user_hash': 'user_hash',
            },
            False
        ),
        (
            {
                'image_id': 'image_id',
                'algorithm': 'algorithm',
                'out_image_format': 1,
                'out_image_filename': 'name',
                'user_hash': 'user_hash',
            },
            False
        ),
        (
            {
                'image_id': 'image_id',
                'algorithm': 'algorithm',
                'out_image_format': 'format',
                'out_image_filename': 1,
                'user_hash': 'user_hash',
            },
            False
        ),
        (
            {
                'image_id': 'image_id',
                'algorithm': 'algorithm',
                'out_image_format': 'format',
                'out_image_filename': 'name',
                'user_hash': 1,
            },
            False
        ),

    ]
)
def test_image_process(image_process_dict, success):
    from server.api import image_process
    ret = image_process(image_process_dict)

    assert ret.get('success') == success


@pytest.mark.parametrize(
    "image_id, user_hash, success",
    [
        (
            'image_id',
            1,
            False
        ),
        (
            1,
            'user_hash',
            False
        ),
        (
            ['image_id'],
            'user_hash',
            False
        ),
    ]
)
def test_check_existance_and_fetch_image(image_id, user_hash, success):
    from server.api import check_existance_and_fetch_image
    succ, err, img = check_existance_and_fetch_image(image_id, user_hash)

    assert succ == success

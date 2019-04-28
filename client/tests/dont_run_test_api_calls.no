import pytest


@pytest.mark.parametrize(
    "image_id, algorithm, im_format, out_filename, user_hash, success",
    [
        (
            1,
            'algorithm',
            'im_format',
            'out_filename',
            'user_has',
            False,
        ),
        (
            'image_id',
            2,
            'im_format',
            'out_filename',
            'user_has',
            False,
        ),
        (
            'image_id',
            'algorithm',
            3,
            'out_filename',
            'user_has',
            False,
        ),
        (
            'image_id',
            'algorithm',
            'im_format',
            4,
            'user_has',
            False,
        ),
        (
            'image_id',
            'algorithm',
            'im_format',
            'out_filename',
            5,
            False,
        ),
    ]
)
def test_apply_algorithm(
    image_id,
    algorithm,
    im_format,
    out_filename,
    user_hash,
    success
):
    from client.api_calls import apply_algorithm
    ret = apply_algorithm(image_id,
                          algorithm,
                          im_format,
                          out_filename,
                          user_hash
                          )
    assert ret.get('success') == success


@pytest.mark.parametrize(
    "image_ids, im_format, user_hash, success",
    [
        (
            [1, 's'],
            'im_format',
            'user_has',
            False,
        ),
        (
            'image_id',
            'im_format',
            'user_has',
            False,
        ),
        (
            ['image_id'],
            3,
            'user_has',
            False,
        ),
        (
            ['image_id'],
            'im_format',
            4,
            False,
        ),
    ]
)
def test_get_download_images(
    image_ids,
    im_format,
    user_hash,
    success
):
    from client.api_calls import get_download_images
    ret = get_download_images(image_ids,
                              im_format,
                              user_hash
                              )
    assert ret.get('success') == success


@pytest.mark.parametrize(
    "image_id, user_hash, success",
    [
        (
            1,
            'user_has',
            False,
        ),
        (
            'id',
            1,
            False,
        ),
    ]
)
def test_get_single_image(
    image_id,
    user_hash,
    success
):
    from client.api_calls import get_single_image
    ret = get_single_image(image_id,
                           user_hash
                           )
    assert ret.get('success') == success


@pytest.mark.parametrize(
    "user_hash, success",
    [
        (1,  False),
        (1.0,  False),
        (['hash1', 'hash2'],  False),
    ]
)
def test_get_images_info(
    user_hash,
    success
):
    from client.api_calls import get_images_info
    ret = get_images_info(user_hash)
    assert ret.get('success') == success


@pytest.mark.parametrize(
    "image_b64s, filename, user_hash, success",
    [
        (
            1,
            'filename',
            'user_has',
            False,
        ),
        (
            'image_b64s',
            2,
            'user_has',
            False,
        ),
        (
            'image_b64s',
            'filename',
            3,
            False,
        ),
    ]
)
def test_upload_image(
    image_b64s,
    filename,
    user_hash,
    success
):
    from client.api_calls import upload_image
    ret = upload_image(image_b64s,
                       filename,
                       user_hash
                       )
    assert ret.get('success') == success


@pytest.mark.parametrize(
    "zip_b64s, filename, user_hash, success",
    [
        (
            1,
            'filename',
            'user_has',
            False,
        ),
        (
            'zip_b64s',
            2,
            'user_has',
            False,
        ),
        (
            'zip_b64s',
            'filename',
            3,
            False,
        ),
    ]
)
def test_upload_zip(
    zip_b64s,
    filename,
    user_hash,
    success
):
    from client.api_calls import upload_zip
    ret = upload_zip(zip_b64s,
                     filename,
                     user_hash
                     )
    assert ret.get('success') == success


@pytest.mark.parametrize(
    "image_id, filename, user_hash, success",
    [
        (
            1,
            'filename',
            'user_has',
            False,
        ),
        (
            'image_id',
            2,
            'user_has',
            False,
        ),
        (
            'image_id',
            'filename',
            3,
            False,
        ),
    ]
)
def test_edit_filename(
    image_id,
    filename,
    user_hash,
    success
):
    from client.api_calls import edit_filename
    ret = edit_filename(image_id,
                        filename,
                        user_hash
                        )
    assert ret.get('success') == success


@pytest.mark.parametrize(
    "image_id, description, user_hash, success",
    [
        (
            1,
            'description',
            'user_has',
            False,
        ),
        (
            'image_id',
            2,
            'user_has',
            False,
        ),
        (
            'image_id',
            'description',
            3,
            False,
        ),
    ]
)
def test_edit_description(
    image_id,
    description,
    user_hash,
    success
):
    from client.api_calls import edit_description
    ret = edit_description(image_id,
                           description,
                           user_hash
                           )
    assert ret.get('success') == success

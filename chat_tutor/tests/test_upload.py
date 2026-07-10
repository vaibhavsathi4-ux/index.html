import io
import pytest


# ---------------------------------------------------------
# PDF Upload
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_pdf_upload(client, auth_headers):

    file = io.BytesIO(b"dummy pdf")

    response = await client.post(

        "/upload",

        files={
            "file": ("sample.pdf", file, "application/pdf")
        },

        headers=auth_headers

    )

    assert response.status_code in (200, 201)


# ---------------------------------------------------------
# Image Upload
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_image_upload(client, auth_headers):

    image = io.BytesIO(b"image")

    response = await client.post(

        "/upload",

        files={
            "file": ("image.png", image, "image/png")
        },

        headers=auth_headers

    )

    assert response.status_code in (200, 201)


# ---------------------------------------------------------
# Invalid File
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_invalid_file(client, auth_headers):

    txt = io.BytesIO(b"text")

    response = await client.post(

        "/upload",

        files={
            "file": ("note.txt", txt, "text/plain")
        },

        headers=auth_headers

    )

    assert response.status_code in (400, 415)


# ---------------------------------------------------------
# No File
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_no_file(client, auth_headers):

    response = await client.post(

        "/upload",

        headers=auth_headers

    )

    assert response.status_code in (400, 422)


# ---------------------------------------------------------
# Large File
# ---------------------------------------------------------

@pytest.mark.asyncio
async def test_large_upload(client, auth_headers):

    file = io.BytesIO(b"A" * 20_000_000)

    response = await client.post(

        "/upload",

        files={
            "file": (
                "large.pdf",
                file,
                "application/pdf"
            )
        },

        headers=auth_headers

    )

    assert response.status_code in (200, 413)
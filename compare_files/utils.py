from django.http import FileResponse
from django.http import HttpResponse
from django.conf import settings
import os


def download_file(file_path):
    """Serves the file for download."""
    if os.path.exists(file_path):
        return FileResponse(
            open(file_path, "rb"),
            as_attachment=True,
            filename=os.path.basename(file_path),
        )
    else:
        return HttpResponse("File not found.", status=404)


def delete_file(file_path):
    """Deletes the file from the server."""
    if os.path.exists(file_path):
        os.remove(file_path)


def download_and_delete_file(request):
    """Handles downloading the file and then deletes it from the server."""
    file_path = os.path.join(settings.BASE_DIR, "compared.docx")

    response = download_file(file_path)
    if response.status_code == 200:
        delete_file(file_path)

    return response

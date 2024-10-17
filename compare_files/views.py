from django.shortcuts import render
from .forms import FileUploadForm
from .utils import download_and_delete_file
import aspose.words as aw
from io import BytesIO
import os
from django.conf import settings
from datetime import datetime


def compare_files(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file1 = request.FILES["file1"]
            file2 = request.FILES["file2"]
            file1_stream = BytesIO(file1.read())
            file2_stream = BytesIO(file2.read())

            doc1 = aw.Document(file1_stream)
            doc2 = aw.Document(file2_stream)
            doc1.compare(doc2, "author", datetime.now())

            comparison_output_path = os.path.join(settings.BASE_DIR, f"compared.docx")

            doc1.save(comparison_output_path)

            return download_and_delete_file(request)

    else:
        form = FileUploadForm()

    return render(request, "compare_files/compare.html", {"form": form})

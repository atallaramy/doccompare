from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileUploadForm
from docx import Document
from difflib import unified_diff, ndiff


def get_text_from_docx(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)


def compare_docs(text1, text2):
    text1 = text1.splitlines()
    text2 = text2.splitlines()

    diff = unified_diff(text1, text2, lineterm="", fromfile="file1", tofile="file2")
    return "\n".join(list(diff))


def compare_files(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file1 = request.FILES["file1"]
            file2 = request.FILES["file2"]

            text1 = get_text_from_docx(file1)
            text2 = get_text_from_docx(file2)

            differences = compare_docs(text1, text2)
            return render(
                request, "compare_files/results.html", {"differences": differences}
            )

    else:
        form = FileUploadForm()

    return render(request, "compare_files/compare.html", {"form": form})

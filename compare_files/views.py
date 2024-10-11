from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileUploadForm
from docx import Document
from difflib import ndiff


def get_text_from_docx(file):
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)


def highlight_differences(line1, line2):
    diff = list(ndiff(line1.split(), line2.split()))
    highlighted = []
    for word in diff:
        if word.startswith("+ "):  # Addition
            highlighted.append(f"<strong style='color: green;'>{word[2:]}</strong>")
        elif word.startswith("- "):  # Removal
            highlighted.append(f"<del style='color: red;'>{word[2:]}</del>")
        else:
            highlighted.append(word[2:])
    return " ".join(highlighted)


def compare_docs(text1, text2):
    text1 = text1.splitlines()
    text2 = text2.splitlines()

    result = []
    for line1, line2 in zip(text1, text2):
        if line1 != line2:
            result.append(highlight_differences(line1, line2))
        else:
            result.append("")
            result.append(line1.strip())
    return "\n".join(result)


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

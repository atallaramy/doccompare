from django.shortcuts import render
from django.http import HttpResponse
from .forms import FileUploadForm
from docx import Document
from difflib import ndiff


def get_text_from_docx(file):
    """Extracts all text from a DOCX file."""
    doc = Document(file)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    return "\n".join(full_text)


def highlight_differences(text1, text2):
    """Generates highlighted HTML for word-level differences."""
    diff = list(ndiff(text1.split(), text2.split()))
    highlighted = []

    for word in diff:
        if word.startswith("+ "):  # Word added
            highlighted.append(f"<strong style='color: green;'>{word[2:]}</strong>")
        elif word.startswith("- "):  # Word removed
            highlighted.append(f"<del style='color: red;'>{word[2:]}</del>")
        else:  # Unchanged word
            highlighted.append(word[2:])

    return " ".join(highlighted)


def compare_docs(text1, text2):
    """Compares entire documents and returns them with highlighted differences."""
    text1_lines = text1.splitlines(keepends=True)  # Preserve newlines
    text2_lines = text2.splitlines(keepends=True)

    result = ["\n"]
    max_len = max(len(text1_lines), len(text2_lines))

    for i in range(max_len):
        # Handle line mismatches by providing empty string for missing lines
        line1 = text1_lines[i] if i < len(text1_lines) else ""
        line2 = text2_lines[i] if i < len(text2_lines) else ""

        if line1 != line2:
            highlighted = highlight_differences(line1, line2)
            result.append("\n")
            result.append(highlighted)
        else:
            result.append("\n")
            result.append(line1)  # Add unchanged lines as is

    return "".join(result)  # Maintain original document structure


def compare_files(request):
    """Handles file uploads and renders comparison results."""
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

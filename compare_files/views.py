from django.shortcuts import render
from .forms import FileUploadForm
from docx import Document
from difflib import ndiff


def get_text_from_docx(file):
    """Extracts text from a DOCX file while preserving paragraphs."""
    doc = Document(file)
    full_text = [para.text for para in doc.paragraphs]
    return "\n".join(full_text)


def generate_html_from_diff(text1, text2):
    """Generate HTML to highlight line-level and word-level changes."""
    diff = list(ndiff(text1.splitlines(keepends=True), text2.splitlines(keepends=True)))
    result = []

    for line in diff:
        if line.startswith("+ "):  # Added line
            result.append(f"<strong style='color: green;'>{line[2:]}</strong>")
        elif line.startswith("- "):  # Removed line
            result.append(f"<del style='color: red;'>{line[2:]}</del>")
        elif line.startswith("? "):  # Indicator for word-level changes (optional)
            # Skip these, as they are not necessary for display
            continue
        else:  # Unchanged line
            result.append(line[2:])

    return "".join(result)


def compare_files(request):
    """Handles file uploads and renders comparison results."""
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file1 = request.FILES["file1"]
            file2 = request.FILES["file2"]

            text1 = get_text_from_docx(file1)
            text2 = get_text_from_docx(file2)

            differences = generate_html_from_diff(text1, text2)
            return render(
                request, "compare_files/results.html", {"differences": differences}
            )

    else:
        form = FileUploadForm()

    return render(request, "compare_files/compare.html", {"form": form})

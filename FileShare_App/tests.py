from django.test import TestCase

# Create your tests here.
import os
from pathlib import Path
def get_categories():
    dir_path = Path(__file__).resolve().parent.parent / 'media' / 'documents'
    categories = []
    for file in os.listdir(dir_path):
        if os.path.isdir(os.path.join(dir_path, file)):
            categories.append((file, file))
    return categories
print(get_categories())
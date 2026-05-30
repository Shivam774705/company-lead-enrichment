import os
import zipfile

def zipdir(path, ziph):
    # ziph is zipfile.ZipFile object
    for root, dirs, files in os.walk(path):
        # Skip virtualenv directories, node_modules, and cache files to keep zip under 10MB!
        if any(ignored in root for ignored in ['venv', '.venv', 'node_modules', '__pycache__', '.git', '.gemini', 'dist', 'staticfiles', '.idea', '.vscode']):
            continue
        for file in files:
            # Skip db.sqlite3, local JSON databases, and the zip script/output itself
            if file in ['db.sqlite3', 'in_memory_db.json', 'submission.zip', 'zip_project.py']:
                continue
            filePath = os.path.join(root, file)
            # Find relative path to write inside the zip
            relPath = os.path.relpath(filePath, os.path.dirname(path))
            print(f"Adding: {relPath}")
            ziph.write(filePath, relPath)

if __name__ == '__main__':
    zipf = zipfile.ZipFile('submission.zip', 'w', zipfile.ZIP_DEFLATED)
    # The workspace path is current dir
    zipdir('.', zipf)
    zipf.close()
    print("Project zipped successfully into 'submission.zip'")

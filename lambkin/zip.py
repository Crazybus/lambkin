import os
import zipfile

# REF: http://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html


def zip_function(function_name):
    zip_file_path = '/tmp/lambda-publish-%s.zip' % function_name
    zip_file = zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED)

    for root, dirs, files in os.walk(function_name):
        venv_dir = os.path.join(function_name, 'venv')
        site_dir = os.path.join(venv_dir, 'lib', 'python2.7', 'site-packages')
        dist_dir = os.path.join(venv_dir, 'lib', 'python2.7', 'dist-packages')
        for f in files:
            path = os.path.join(root, f)
            if root.startswith(site_dir):
                # Then strip the library dir, and put the file in the zip.
                trimmed_path = path[len(site_dir):]
                zip_file.write(path, trimmed_path)
            elif root.startswith(dist_dir):
                # Then strip the library dir, and put the file in the zip.
                trimmed_path = path[len(dist_dir):]
                zip_file.write(path, trimmed_path)
            elif root.startswith(venv_dir):
                # Then it's other junk in the virtualenv that we don't want.
                pass
            else:
                # Not sure what this is. The function author probably put
                # it here for a reason, so make sure it goes in the zip.
                zip_file.write(path, path[len(function_name):])
    zip_file.close()
    return zip_file_path
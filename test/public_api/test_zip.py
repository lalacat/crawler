import os
import zipfile
import logging

logger = logging.getLogger(__name__)

# path = os.getcwd()
# for root, dirs, files in os.walk(path):
#     print(root)
#     print(dirs)
#     print(files)
path = os.getcwd()
zip = zipfile.ZipFile('test', "w", zipfile.ZIP_DEFLATED, allowZip64=True)
# zip.write("import.sh")
for root, dirs, files in os.walk(os.getcwd()):
    for f in files:
        filename = os.path.join(root, f)
        logger.debug("packing filename %s", filename)
        zip.write(filename)
zip.setpassword('123'.encode('utf-8'))
zip.close()

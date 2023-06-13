import pytest

from app.services import FileManager
import os



@pytest.mark.parametrize(
    ('folder', 'file', 'links'),
    (
        ('test_artifacts', 'exp_1.txt', ['line1 data']),
        ('test_artifacts/path1', 'exp_2.txt', ['line1 data'])
    )
)
def test_save_links(folder, file, links):
    FileManager.save_links(links, file, folder)
    with open(os.path.join(folder, file), 'r+') as file:
        data = file.readlines()
        assert data == links, 'Content of file != writing data'
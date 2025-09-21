import os
import tempfile
import pytest

from internal.core.file_extractor.file_extractor import FileExtractor
from internal.model import UploadFile

class DummyCosService:
    """用于测试的假cos_service，只做本地文件拷贝"""
    def download_file(self, key, file_path):
        # 直接将key（本地路径）拷贝到file_path
        with open(key, "rb") as src, open(file_path, "wb") as dst:
            dst.write(src.read())

@pytest.fixture
def file_extractor():
    return FileExtractor(cos_service=DummyCosService())

def create_temp_file(suffix, content=b"test content"):
    fd, path = tempfile.mkstemp(suffix=suffix)
    with os.fdopen(fd, "wb") as f:
        f.write(content)
    return path

@pytest.mark.parametrize("suffix,loader_type", [
    (".xlsx", "UnstructuredExcelLoader"),
    (".xls", "UnstructuredExcelLoader"),
    (".pdf", "UnstructuredPDFLoader"),
    (".md", "UnstructuredMarkdownLoader"),
    (".markdown", "UnstructuredMarkdownLoader"),
    (".htm", "UnstructuredHTMLLoader"),
    (".html", "UnstructuredHTMLLoader"),
    (".csv", "UnstructuredCSVLoader"),
    (".ppt", "UnstructuredPowerPointLoader"),
    (".pptx", "UnstructuredPowerPointLoader"),
    (".xml", "UnstructuredXMLLoader"),
    (".txt", "TextLoader"),
    (".unknown", "UnstructuredFileLoader"),
])
def test_load_from_file(file_extractor, suffix, loader_type):
    # 创建临时文件
    path = create_temp_file(suffix)
    upload_file = UploadFile(key=path)
    # 测试load方法
    docs = file_extractor.load(upload_file, return_text=False, is_unstructured=(loader_type != "TextLoader"))
    assert isinstance(docs, list)
    # 测试返回文本
    text = file_extractor.load(upload_file, return_text=True, is_unstructured=(loader_type != "TextLoader"))
    assert isinstance(text, str)
    os.remove(path)

def test_load_from_url(monkeypatch):
    # 模拟requests.get
    class DummyResponse:
        content = b"dummy"
    monkeypatch.setattr("requests.get", lambda url: DummyResponse())
    # 测试
    text = FileExtractor.load_from_url("http://example.com/test.txt", return_text=True)
    assert isinstance(text, str)

def test_load_from_file_classmethod():
    path = create_temp_file(".test", b"hello world")
    text = FileExtractor.load_from_file(path, return_text=True, is_unstructured=True)
    assert "hello" in text
    os.remove(path)

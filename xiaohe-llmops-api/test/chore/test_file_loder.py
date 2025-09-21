
import os
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# 1. 禁用 SSL 验证警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# 2. 设置 HF 镜像
os.environ["HF_ENDPOINT"] = "https://hf-mirror.com"

# 3. 配置不验证 SSL 证书的会话
session = requests.Session()
session.verify = False  # 关闭 SSL 验证（风险！）

# 4. 让 huggingface_hub 使用这个会话
from huggingface_hub import configure_http_backend
configure_http_backend(backend_factory=lambda: session)

def test_pdf_file_loader():
    
    from dotenv import load_dotenv
    import os
    load_dotenv()
    HF_ENDPOINT = os.environ['HF_ENDPOINT']
    os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com/'
    from langchain_community.document_loaders import PyPDFLoader, UnstructuredPDFLoader
    from pathlib import Path
    file_path = Path("xiaohe-llmops-api/test/data/r97-ai.pdf")
    if not file_path.exists():
        raise FileNotFoundError("文件不存在")
    loader = UnstructuredPDFLoader(file_path=str(file_path))
    docs = loader.load()
    assert len(docs) > 0
    assert docs[0].page_content is not None
    assert docs[0].metadata is not None
    assert docs[0].metadata["source"] == str(file_path)
    assert docs[0].metadata["total_pages"] == 2
test_pdf_file_loader()
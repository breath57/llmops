
def test_nltk_download():
    import nltk
    result = nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')
    print(f'result: {result}')
    pass


def test_base_model_field():
    from pydantic import BaseModel, Field
    class TestModel(BaseModel):
        name: str = Field(description="姓名")
        age: int = Field(description="年龄")
    model = TestModel(name="张三", age=19)
    print(model.model_fields)
    pass
test_base_model_field()
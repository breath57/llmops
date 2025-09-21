from operator import itemgetter
from langchain_openai import ChatOpenAI
import pytest
from dotenv import load_dotenv
load_dotenv()


class TestLangGraph:

    def test_create_react_agent(self):
        from langgraph.graph import StateGraph,END
        from langgraph.graph.state import CompiledStateGraph
        from langgraph.prebuilt import create_react_agent
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage

        agent = create_react_agent(
            model=ChatOpenAI(model="deepseek-ai/DeepSeek-V3", temperature=0.5),
            tools=[],
        )

        result = agent.invoke({"messages": [HumanMessage(content="你好，你是谁？")]})    
        print(result)

    def test_my_functional_tool_agent(self):
        from langgraph.graph import StateGraph,END
        from langgraph.graph.state import CompiledStateGraph
        from langgraph.prebuilt import create_react_agent
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage
        from internal.core.agent.agents.function_call_agent import FunctionCallAgent
        from internal.core.agent.entities.agent_entity import AgentConfig, InvokeFrom
        from internal.core.language_model.providers.openai.chat import Chat
        from internal.core.language_model.entities.model_entity import ModelFeature
        import uuid

        llm =Chat(
            model="deepseek-ai/DeepSeek-V3",
            temperature=0.8,
            features=[ModelFeature.TOOL_CALL, ModelFeature.AGENT_THOUGHT],
            metadata={},
        )

        agent = FunctionCallAgent(
            llm=llm,
            agent_config=AgentConfig(
                user_id=uuid.uuid4(),
                invoke_from=InvokeFrom.DEBUGGER,
                enable_long_term_memory=True,
                tools=[],
            ),
        )

        result = agent.invoke({
            "messages": [HumanMessage(content="你好，你是谁？")],
            "history": [],
            "long_term_memory": "",
        })    
        print(result)

    
    def test_langgraph_thread_id(self):
        from langgraph.graph import StateGraph,END
        from langgraph.graph.state import CompiledStateGraph
        from langgraph.graph import MessageGraph
        from langgraph.prebuilt import create_react_agent
        from langchain_openai import ChatOpenAI
        from langchain_core.messages import HumanMessage
        import langgraph.checkpoint.memory as memory



        llm = ChatOpenAI(model="deepseek-ai/DeepSeek-V3", temperature=0.5)
        graph = MessageGraph()
        graph.add_node('llm', llm)
        graph.set_entry_point('llm')
        graph.set_finish_point('llm')

        checkpointer = memory.MemorySaver()
        compiled = graph.compile(checkpointer=checkpointer)
        thread_id = "hezhiwei"
        result1 = compiled.invoke([HumanMessage(content="你好，我叫何志伟, 喜欢编程")],
                                 config={
                                    "configurable": {
                                        "thread_id": thread_id,
                                    }
                                 },
                                 )
        print(result1)

        result2 = compiled.invoke([HumanMessage(content="我叫什么，我喜欢什么")],
                                 config={
                                    "configurable": {
                                        "thread_id": thread_id,
                                    }
                                 },
                                 )
        print(result2)

    
    # 测试对话历史记忆
    def test_conversation_history_memory(self):
        from langchain.memory import ConversationSummaryBufferMemory, ConversationBufferWindowMemory, ConversationEntityMemory, SQLiteEntityStore
        from langchain.prompts import ChatPromptTemplate
        from langgraph.store.memory import MemoryStore
        from langchain.memory import SQLiteEntityStore, InMemoryEntityStore, VectorStoreRetrieverMemory
        from langchain_community.chat_message_histories import SQLChatMessageHistory, FileChatMessageHistory, FirestoreChatMessageHistory
        from langchain.prompts import MessagesPlaceholder
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.runnables import  RunnablePassthrough, RunnableLambda



        llm = ChatOpenAI(model="deepseek-ai/DeepSeek-V3", temperature=0.5)

        memory = ConversationBufferWindowMemory(
            k=3,
            chat_memory=FileChatMessageHistory('./memory.txt'),
            memory_key="my_history",
            return_messages=True
        )

        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant. You are given a conversation history and a new message. You need to respond to the new message based on the conversation history. {history} {input}"),
            MessagesPlaceholder(variable_name="history", optional=False),
            ("human", "{input}"),
        ])

        chain = ( 
            RunnablePassthrough.assign(
                history=RunnableLambda(memory.load_memory_variables, {}) 
                | itemgetter("my_history"))
            | prompt | llm | StrOutputParser())

        
        # from langchain_core.runnables import ConfigurableField
        # chain.bind().with_config()
        # ChatOpenAI().configurable_fields()

        result = chain.invoke({
            "input": "你好，我叫何志伟, 喜欢编程"
        })

        memory.save_context(
            inputs={
                "input": "你好，我叫何志伟, 喜欢编程"
            },
            outputs={
                "output": result
            }
        )

        history = memory.load_memory_variables({})
        print(history)

        result = chain.invoke({
            "input": "我叫什么，我喜欢什么"
        })

        memory.save_context({
            "input": "我叫什么，我喜欢什么"
        }, {
            "output": result
        })

        history = memory.load_memory_variables({})
        print(history)


    def test_runnable_passthrough(self):
        from langchain_core.runnables import  RunnablePassthrough, RunnableLambda
        from langchain_core.messages import HumanMessage
        
        def add_one(x: dict) -> int:
            return  1

        chain1 = {} | RunnablePassthrough.assign(
            history=RunnableLambda(add_one)
            )
        chain1_result = chain1.invoke(100)
        print(chain1_result)

        chain2 = {
            "history": 1
        } | RunnablePassthrough.assign(
            history=RunnableLambda(add_one) | itemgetter("history")
            )
        chain2_result = chain2.invoke(1)
        print(chain2_result)

    def test_runnable_passthrough2(self):
        from langchain.schema.runnable import RunnablePassthrough
        from datetime import datetime
        # 创建一个处理链
        chain = {
            "original_query": RunnablePassthrough(),  # 保持原始输入
            "enriched_data": lambda x: f"增强的数据: {x}",  # 添加处理后的数据
        } | RunnablePassthrough.assign(
            timestamp=lambda _: datetime.now().isoformat(),  # 添加时间戳
            processed=lambda x: len(x["original_query"])  # 添加处理结果
        )

        # 使用
        result = chain.invoke("你好")
        # 输出类似：
        # {
        #     "original_query": "你好",
        #     "enriched_data": "增强的数据: 你好",
        #     "timestamp": "2024-01-01T12:00:00",
        #     "processed": 2
        # }
        print(result)
        from langchain_core.runnables import RunnableLambda
        chain2 = RunnablePassthrough.assign(
           extend=RunnableLambda(lambda x: x ) | itemgetter('input')
        )

        chain2_result = chain2.invoke({
            "input": "你好啊！"
        })
        pass

    def test_runnable_lambda(self):
        from langchain_core.runnables import RunnableLambda, RunnableConfig

        from langchain_openai  import ChatOpenAI
        ChatOpenAI().invoke()
        def add(x: int, y: int, config: RunnableConfig) -> int:
            # config: {'tags': [], 'metadata': {'c1': 1}, 'callbacks': <langchain_core.callbacks.manager.CallbackManager object at 0x7f3e68063b00>, 'recursion_limit': 25, 'configurable': {'c1': 1}}
            return x + y
        
        chain = RunnableLambda(func=add, name="add_func")

        result = chain.bind(y=2).invoke(1, config= {
            "configurable": {
                "c1": 1
            }
        })
        pass
    
    def test_langgraph_memory(self):
        import langgraph.store.memory as memory
        from langchain.memory import VectorStoreRetrieverMemory
        from langchain_core.runnables import chain

        @chain
        def my_runnable(x: int) -> int:
            return x + 1
            
        my_runnable.invoke(1)

        


        

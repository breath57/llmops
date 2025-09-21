import grpc
from weaviate.proto.v1 import health_pb2_grpc, health_pb2
import os
def check_weaviate_grpc(host: str, port: int):
    # 构建 gRPC 通道
    channel = grpc.insecure_channel(f"{host}:{port}")
    stub = health_pb2_grpc.HealthStub(channel)
    
    try:
        # 发送一个简单的 gRPC 请求（获取元数据）
        request = health_pb2.HealthCheckRequest(service="weaviate.Weaviate")
        response: health_pb2.HealthCheckResponse = stub.Check(request)
        print(f"gRPC 连接成功！status: {response.status}, {response.ListFields()}")
        return True
    except grpc.RpcError as e:
        print(f"gRPC 连接失败: {e.details()}")
        return False
    except Exception as e:
        print(f"其他错误: {str(e)}")
        return False

# 调用检查函数（替换为你的配置）
check_weaviate_grpc(
    host=os.getenv("WEAVIATE_HOST", "localhost"),
    port=int(os.getenv("WEAVIATE_GRPC_PORT", 50051))
)
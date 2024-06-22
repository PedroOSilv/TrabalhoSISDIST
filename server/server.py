from concurrent import futures
import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc
import os

class FileTransferServicer(file_transfer_pb2_grpc.FileTransferServicer):
    def __init__(self):
        self.storage_path = "uploaded_files"
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

    def Upload(self, request_iterator, context):
        for file_chunk in request_iterator:
            file_path = os.path.join(self.storage_path, file_chunk.filename)
            with open(file_path, 'ab') as f:
                f.write(file_chunk.content)
        return file_transfer_pb2.UploadStatus(success=True, message="File uploaded successfully")

    def Download(self, request, context):
        file_path = os.path.join(self.storage_path, request.filename)
        if not os.path.exists(file_path):
            context.abort(grpc.StatusCode.NOT_FOUND, "File not found")
        with open(file_path, 'rb') as f:
            while chunk := f.read(1024):
                yield file_transfer_pb2.FileChunk(content=chunk, filename=request.filename)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    file_transfer_pb2_grpc.add_FileTransferServicer_to_server(FileTransferServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

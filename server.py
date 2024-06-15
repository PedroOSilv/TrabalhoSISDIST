from concurrent import futures
import grpc
import filetransfer_pb2
import filetransfer_pb2_grpc
import os

class FileService(filetransfer_pb2_grpc.FileServiceServicer):
    def UploadFile(self, request_iterator, context):
        first_chunk = True
        filename = ""
        with open("/tmp/uploaded_file", "wb") as f:
            for chunk in request_iterator:
                if first_chunk:
                    filename = chunk.filename
                    first_chunk = False
                f.write(chunk.content)
        return filetransfer_pb2.UploadStatus(success=True, message=f"{filename} uploaded successfully")

    def DownloadFile(self, request, context):
        file_path = os.path.join("/tmp", request.filename)
        if not os.path.exists(file_path):
            context.set_details(f'File {request.filename} not found!')
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return
        
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(1024)
                if not chunk:
                    break
                yield filetransfer_pb2.FileChunk(content=chunk, filename=request.filename)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    filetransfer_pb2_grpc.add_FileServiceServicer_to_server(FileService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

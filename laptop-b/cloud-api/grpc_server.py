from concurrent import futures

import grpc

import penyimpanan as db
import sensor_pb2
import sensor_pb2_grpc

_server = None


class SensorServicer(sensor_pb2_grpc.SensorServicer):
    def Kirim(self, request, context):
        pesan = {
            "request_id": request.request_id,
            "node_id": request.node_id,
            "seq": request.seq,
            "nilai": request.nilai,
            "waktu": request.waktu,
        }
        hasil = db.simpan(pesan, jalur="grpc")
        return sensor_pb2.Status(diterima=True, duplikat=hasil["duplikat"])


def mulai_grpc(port=50051):
    global _server
    _server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sensor_pb2_grpc.add_SensorServicer_to_server(SensorServicer(), _server)
    _server.add_insecure_port(f"0.0.0.0:{port}")  # ingat pelajaran Praktikum 1
    _server.start()
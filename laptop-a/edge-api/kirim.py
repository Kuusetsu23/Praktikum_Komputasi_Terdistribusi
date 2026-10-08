import logging
import os
import grpc

import sensor_pb2
import sensor_pb2_grpc

# Inisialisasi logger
log = logging.getLogger(__name__)

# Definisi variabel konfigurasi
CLOUD_HOST = os.getenv("CLOUD_HOST", "localhost")
MAKS_COBA = 3
TIMEOUT_S = 5

# Inisialisasi dictionary PENGIRIM
PENGIRIM = {}

# ===== [PEKAN 5] gRPC =====
_kanal = grpc.insecure_channel(f"{CLOUD_HOST}:50051")
_stub = sensor_pb2_grpc.SensorStub(_kanal)


def kirim_grpc(pesan):
    for coba in range(1, MAKS_COBA + 1):
        try:
            status = _stub.Kirim(sensor_pb2.Bacaan(**pesan), timeout=TIMEOUT_S)
            log.info("gRPC seq=%s coba=%s -> diterima=%s duplikat=%s",
                     pesan["seq"], coba, status.diterima, status.duplikat)
            return {"terkirim": True, "coba": coba}
        except grpc.RpcError as e:
            log.warning("gRPC seq=%s coba=%s -> %s",
                        pesan["seq"], coba, e.code().name)
    return {"terkirim": False, "coba": MAKS_COBA}


PENGIRIM["grpc"] = kirim_grpc
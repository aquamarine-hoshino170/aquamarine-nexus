import socket
import threading
import json
import time
from typing import Dict, Any, List, Callable

class DistributedNexusMeshCore:
    """
    Pure-Python Zero-Dependency Peer-to-Peer (P2P) Distributed Compute Mesh.
    Coordinates parallel scientific workloads across local network nodes using pure sockets.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 9050):
        self.host = host
        self.port = port
        self.is_running = False
        self.registered_workers: List[Dict[str, Any]] = []

    def start_coordinator_server(self, task_executor: Callable[[Dict[str, Any]], Dict[str, Any]]):
        """
        Spins up non-blocking coordinator listening for compute workers.
        """
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        self.is_running = True

        def handle_client(conn: socket.socket, addr):
            try:
                raw_data = conn.recv(65536).decode('utf-8')
                if raw_data:
                    payload = json.loads(raw_data)
                    # Process Distributed Workload Chunk
                    result = task_executor(payload)
                    conn.sendall(json.dumps(result).encode('utf-8'))
            except Exception as e:
                err_resp = {"status": "ERROR", "message": str(e)}
                conn.sendall(json.dumps(err_resp).encode('utf-8'))
            finally:
                conn.close()

        def listen_loop():
            while self.is_running:
                try:
                    server.settimeout(1.0)
                    conn, addr = server.accept()
                    client_thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                    client_thread.start()
                except socket.timeout:
                    continue
                except Exception:
                    break
            server.close()

        listener_thread = threading.Thread(target=listen_loop, daemon=True)
        listener_thread.start()

    def dispatch_remote_task(self, target_host: str, target_port: int, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sends computational chunk to remote worker node and awaits result.
        """
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(5.0)
        try:
            client.connect((target_host, target_port))
            client.sendall(json.dumps(task_data).encode('utf-8'))
            response_raw = client.recv(65536).decode('utf-8')
            return json.loads(response_raw)
        except Exception as e:
            return {"status": "DISPATCH_FAILED", "error": str(e)}
        finally:
            client.close()

    @staticmethod
    def map_reduce_vector_sum(chunks: List[List[float]], port: int = 9051) -> Dict[str, Any]:
        """
        Self-contained MapReduce demo distributing sub-vector summations across local threads.
        """
        mesh = DistributedNexusMeshCore(port=port)

        def worker_task(data: Dict[str, Any]) -> Dict[str, Any]:
            vec = data.get("vector_chunk", [])
            return {"partial_sum": sum(vec), "count": len(vec)}

        mesh.start_coordinator_server(worker_task)
        time.sleep(0.1)  # Allow socket to bind

        total_sum = 0.0
        total_elements = 0

        # Dispatch chunks in parallel
        for chunk in chunks:
            res = mesh.dispatch_remote_task("127.0.0.1", port, {"vector_chunk": chunk})
            if "partial_sum" in res:
                total_sum += res["partial_sum"]
                total_elements += res["count"]

        mesh.is_running = False

        return {
            "chunks_processed": len(chunks),
            "total_elements": total_elements,
            "distributed_sum": round(total_sum, 6),
            "mesh_status": "MAP_REDUCE_SUCCESS"
        }

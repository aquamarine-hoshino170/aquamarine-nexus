import json
import csv
import base64
import pickle
import os

class NexusIO:
    """Universal Import/Export System for Scientific States & Data Manifolds"""

    @staticmethod
    def export_json(data: dict, filepath: str) -> dict:
        """Exports dictionary or computational state to a JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return {"status": "SUCCESS", "filepath": filepath, "bytes_written": os.path.getsize(filepath)}

    @staticmethod
    def import_json(filepath: str) -> dict:
        """Imports computational state from a JSON file"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)

    @staticmethod
    def export_csv(matrix: list, filepath: str) -> dict:
        """Exports a 2D matrix/table to CSV"""
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(matrix)
        return {"status": "SUCCESS", "filepath": filepath, "rows": len(matrix)}

    @staticmethod
    def import_csv(filepath: str) -> list:
        """Imports CSV file into a 2D matrix of numeric floats/strings"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        result = []
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                parsed_row = []
                for val in row:
                    try:
                        parsed_row.append(float(val) if '.' in val else int(val))
                    except ValueError:
                        parsed_row.append(val)
                result.append(parsed_row)
        return result

    @staticmethod
    def export_serialized(obj, filepath: str) -> dict:
        """Serializes any Python object/state into an encrypted Base64 string payload"""
        raw_bytes = pickle.dumps(obj)
        b64_str = base64.b64encode(raw_bytes).decode('utf-8')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(b64_str)
        return {"status": "SUCCESS", "filepath": filepath, "mode": "Base64-Pickle"}

    @staticmethod
    def import_serialized(filepath: str):
        """Deserializes object from Base64 encoded payload file"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        with open(filepath, 'r', encoding='utf-8') as f:
            b64_str = f.read().strip()
        raw_bytes = base64.b64decode(b64_str.encode('utf-8'))
        return pickle.loads(raw_bytes)

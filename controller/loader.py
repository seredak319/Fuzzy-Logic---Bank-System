import json
from typing import Any, Dict, List


def load_json(path: str) -> Any:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_input_mfs(path: str) -> Dict[str, Dict[str, Any]]:
    return load_json(path)


def load_output_mfs(path: str) -> Dict[str, Dict[str, Any]]:
    return load_json(path)


def load_rules(path: str) -> List[Dict[str, Any]]:
    return load_json(path)


def load_representatives(path: str) -> Dict[str, Dict[str, float]]:
    return load_json(path)
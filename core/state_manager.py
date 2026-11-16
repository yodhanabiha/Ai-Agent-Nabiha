import json
import os


class StateManager:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.project_dir = f"storage/projects/{project_name}"
        self.state_file = f"{self.project_dir}/state.json"

        # Buat folder proyek dan subfolder artifacts jika belum ada
        os.makedirs(f"{self.project_dir}/artifacts", exist_ok=True)

    def load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                return json.load(f)
        # Default state awal jika proyek baru dibuat
        return {
            "project_name": self.project_name,
            "chat_history": [],
            "current_stage": "initialized"
        }

    def save_state(self, state_data):
        with open(self.state_file, "w") as f:
            json.dump(state_data, f, indent=4)

    def save_artifact(self, filename: str, content: str):
        """Menyimpan file hasil kerja agent (misal: prd.md atau blueprint.md)"""
        artifact_path = f"{self.project_dir}/artifacts/{filename}"
        with open(artifact_path, "w", encoding="utf-8") as f:
            f.write(content)
        return artifact_path

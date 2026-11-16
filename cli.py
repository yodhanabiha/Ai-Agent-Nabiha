import os
import questionary
from core.state_manager import StateManager
from core.llm_router import call_llm

PROJECTS_DIR = "storage/projects"


def list_projects():
    if not os.path.exists(PROJECTS_DIR):
        return []
    return [d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))]


def main():
    print("==================================================")
    print("🤖 AI MULTI-AGENT WORKSPACE (Orchestrator Edition) 🚀")
    print("==================================================")

    while True:
        action = questionary.select(
            "Pilih menu utama:",
            choices=[
                "📂 Buka Proyek",
                "✨ Buat Proyek Baru",
                "❌ Keluar"
            ]
        ).ask()

        if action == "❌ Keluar" or action is None:
            print("Sampai jumpa!")
            break

        elif action == "✨ Buat Proyek Baru":
            project_name = questionary.text(
                "Masukkan nama proyek (contoh: proyek-bri):").ask()
            if project_name:
                manager = StateManager(project_name)
                manager.save_state(manager.load_state())
                print(f"✅ Proyek '{project_name}' berhasil diinisialisasi!\n")
                run_project_session(project_name)

        elif action == "📂 Buka Proyek":
            projects = list_projects()
            if not projects:
                print("⚠️ Belum ada proyek tersimpan. Silakan buat baru.\n")
                continue

            selected_project = questionary.select(
                "Pilih proyek:",
                choices=projects
            ).ask()

            if selected_project:
                run_project_session(selected_project)


def run_project_session(project_name):
    manager = StateManager(project_name)
    print(f"\n📂 [Masuk ke Workspace Proyek: {project_name}]")
    print("💡 Tips: Cukup ngobrol dengan PM. PM akan mengatur tim (Architect/Developer) di belakang layar.")
    print("Ketik 'exit' kapan saja untuk kembali ke menu utama.\n")

    while True:
        # Input murni berupa obrolan teks, seperti chat biasa
        user_input = questionary.text(f"[{project_name}] Kamu:").ask()

        if not user_input or user_input.lower() == 'exit':
            break

        state = manager.load_state()

        # Simpan chat user ke riwayat
        state["chat_history"].append({"role": "user", "content": user_input})

        print("\n🤖 [PM Agent sedang menganalisis & mengoordinasikan tim...]")

        # 1. PM Mengevaluasi kebutuhan user
        pm_system_prompt = (
            "Kamu adalah Senior IT Product Manager dan Team Orchestrator. "
            "Tugasmu adalah memandu user, menggali kebutuhan aplikasi, dan jika user sudah siap "
            "atau meminta arsitektur, kamu harus memanggil System Architect di belakang layar. "
            "Saat ini, tanggapi pesan user secara profesional, ajukan pertanyaan jika kurang jelas, "
            "atau berikan sinyal [TRIGGER_ARCHITECT] jika user sudah meminta/menyetujui pembuatan arsitektur."
        )

        pm_response = call_llm(user_input, mode="smart",
                               system_instruction=pm_system_prompt)

        # 2. Cek apakah PM memutuskan memanggil Architect di belakang layar
        final_output = pm_response
        if "[TRIGGER_ARCHITECT]" in pm_response or "buatkan arsitektur" in user_input.lower():
            print(
                "📐 [System Architect dipanggil oleh PM untuk merancang Blueprint...]")

            architect_system_prompt = (
                "Kamu adalah Principal Software Architect. "
                "Berdasarkan diskusi proyek sejauh ini, buatkan cetak biru arsitektur (Struktur Folder, "
                "Skema Database, dan Endpoint API) secara ringkas dan jelas."
            )
            # Architect merancang berdasarkan input terakhir
            arch_response = call_llm(
                user_input, mode="smart", system_instruction=architect_system_prompt)

            # Simpan hasil arsitektur ke file artifact proyek
            artifact_path = manager.save_artifact(
                "blueprint.md", arch_response)

            # Gabungkan respons PM dengan hasil Architect untuk dikonfirmasi ke user
            final_output = (
                f"{pm_response.replace('[TRIGGER_ARCHITECT]', '')}\n\n"
                f"--- [CETAK BIRU ARSITEKTUR OLEH ARCHITECT] ---\n"
                f"{arch_response}\n\n"
                f"💾 (Arsitektur telah disimpan otomatis ke {artifact_path})\n"
                f"❓ Apakah rancangan arsitektur di atas sudah disetujui, atau ada yang ingin dibahas lebih lanjut?"
            )

        print(f"\n🤖 [PM Agent]:\n{final_output}\n")

        # Simpan riwayat respons ke state
        state["chat_history"].append(
            {"role": "assistant", "content": final_output})
        manager.save_state(state)


if __name__ == "__main__":
    main()

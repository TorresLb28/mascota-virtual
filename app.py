# -*- coding: utf-8 -*-
# @Author: Your name
# @Date:   2026-10-02 19:24:45
# @Last Modified by:   Your name
# @Last Modified time: 2026-10-02 19:38:29
import random
import streamlit as st


class VirtualPet:
    """Clase que encapsula el estado y las reglas de negocio de la mascota."""

    def __init__(self, name: str):
        self.name = name
        self.hunger = 80
        self.energy = 80
        self.happiness = 80
        self.is_runaway = False
        self.turn_count = 0
        self.last_event = ""

    def feed(self):
        """Alimenta a la mascota."""
        if self.is_runaway:
            return
        self.hunger = min(100, self.hunger + 25)
        self.energy = max(0, self.energy - 5)
        self._advance_time("¡Mmm, qué rico alimento! 🍲")

    def play(self):
        """Juega con la mascota."""
        if self.is_runaway:
            return
        self.happiness = min(100, self.happiness + 25)
        self.energy = max(0, self.energy - 15)
        self.hunger = max(0, self.hunger - 10)
        self._advance_time("¡Yaaay! Jugar contigo es súper divertido 🎾")

    def sleep(self):
        """Pone a dormir a la mascota."""
        if self.is_runaway:
            return
        self.energy = min(100, self.energy + 35)
        self.hunger = max(0, self.hunger - 15)
        self._advance_time("Zzz... ¡Esa siesta me recuperó la energía! 💤")

    def _advance_time(self, base_dialogue: str):
        """Avanza los turnos, aplica desgaste y calcula eventos aleatorios."""
        self.turn_count += 1

        # Desgaste natural pasivo por turno
        self.hunger = max(0, self.hunger - random.randint(6, 12))
        self.energy = max(0, self.energy - random.randint(4, 10))
        self.happiness = max(0, self.happiness - random.randint(5, 11))

        # Evento aleatorio
        event_msg = self._trigger_random_event()
        self.last_event = f"{base_dialogue} {event_msg}".strip()

        # Condición de derrota: cualquier estadística llega a 0
        if self.hunger <= 0 or self.energy <= 0 or self.happiness <= 0:
            self.is_runaway = True

    def _trigger_random_event(self) -> str:
        """Sucesos aleatorios que afectan las estadísticas."""
        events = [
            ("⚡ Se asustó con un trueno (-10 Felicidad).", 0, 0, -10),
            ("🪰 Le dio dolor de panza (-15 Hambre).", -15, 0, 0),
            ("😱 Tuvo una pesadilla (-15 Energía).", 0, -15, 0),
            ("", 0, 0, 0)
        ]

        if random.random() < 0.5:
            desc, h_change, e_change, hap_change = random.choice(events[:3])
            self.hunger = max(0, self.hunger + h_change)
            self.energy = max(0, self.energy + e_change)
            self.happiness = max(0, self.happiness + hap_change)
            return desc
        return ""

    def get_dialogue(self) -> str:
        """Determina el mensaje de la mascota según su estado."""
        if self.is_runaway:
            return f"😢 {self.name} se sintió descuidado/a y se escapó de casa."
        if self.hunger < 30:
            return f"🍔 {self.name}: '¡Tengo muchísimo hambre, dame de comer!'"
        if self.energy < 30:
            return f"😴 {self.name}: 'Estoy muy cansado... necesito dormir.'"
        if self.happiness < 30:
            return f"💔 {self.name}: 'Me siento solo... ¡juega conmigo!'"
        return f"😸 {self.name}: '¡Me siento genial! ¡Gracias por cuidarme!'"


class PetGameUI:
    """Clase responsable de la interfaz gráfica en Streamlit."""

    def __init__(self):
        st.set_page_config(page_title="Mascota Virtual", page_icon="🐾", layout="centered")

    def run(self):
        st.title("🐾 Mi Mascota Virtual")

        # Inicialización de estado en session_state
        if "pet" not in st.session_state:
            st.session_state.pet = None

        if st.session_state.pet is None:
            self._render_creation_screen()
        else:
            self._render_game_screen()

    def _render_creation_screen(self):
        st.subheader("¡Adopta tu mascota!")
        pet_name = st.text_input("Ingresa el nombre de tu mascota:", value="Milo")
        if st.button("Adoptar", type="primary", use_container_width=True):
            if pet_name.strip():
                st.session_state.pet = VirtualPet(pet_name.strip())
                st.rerun()

    def _render_game_screen(self):
        pet: VirtualPet = st.session_state.pet

        # Mensaje de estado
        if pet.is_runaway:
            st.error(pet.get_dialogue())
        else:
            st.info(pet.get_dialogue())

        if pet.last_event:
            st.caption(f"📢 Último suceso: {pet.last_event}")

        st.write(f"**Turno actual:** {pet.turn_count}")
        st.divider()

        # Visualización de Estadísticas
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("🍗 Hambre", f"{pet.hunger}/100")
            st.progress(pet.hunger / 100)
        with c2:
            st.metric("⚡ Energía", f"{pet.energy}/100")
            st.progress(pet.energy / 100)
        with c3:
            st.metric("🎈 Felicidad", f"{pet.happiness}/100")
            st.progress(pet.happiness / 100)

        st.divider()

        # Pantalla de Game Over si escapa
        if pet.is_runaway:
            st.error(f"❌ GAME OVER: Una de las estadísticas de {pet.name} llegó a 0 y escapó.")
            if st.button("Adoptar otra mascota", type="primary", use_container_width=True):
                st.session_state.pet = None
                st.rerun()
            return

        # Botones de Acción
        st.subheader("Acciones")
        b1, b2, b3 = st.columns(3)

        with b1:
            if st.button("🍕 Alimentar", use_container_width=True):
                pet.feed()
                st.rerun()

        with b2:
            if st.button("🎮 Jugar", use_container_width=True):
                pet.play()
                st.rerun()

        with b3:
            if st.button("😴 Dormir", use_container_width=True):
                pet.sleep()
                st.rerun()


if __name__ == "__main__":
    app = PetGameUI()
    app.run()
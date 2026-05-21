import streamlit as st
import random

# --- Configuración de la página ---
st.set_page_config(
    page_title="Concentrese 2 Jugadores", page_icon="🧠", layout="centered"
)


# --- Inicializar variables de estado ---
def inicializar_juego():
    emojis = [
        "🍎",
        "🍎",
        "🍌",
        "🍌",
        "🍇",
        "🍇",
        "🍓",
        "🍓",
        "🍋",
        "🍋",
        "🍍",
        "🍍",
        "🥝",
        "🥝",
        "🍉",
        "🍉",
    ]
    random.shuffle(emojis)

    st.session_state.tablero = emojis
    st.session_state.reveladas = [False] * 16
    st.session_state.parejas_encontradas = []
    st.session_state.primer_clic = None
    st.session_state.segundo_clic = None

    # Sistema de turnos y puntuación
    st.session_state.jugador_actual = 1
    st.session_state.puntos_j1 = 0
    st.session_state.puntos_j2 = 0
    st.session_state.error_pendiente = False  # Bloquea el tablero si fallan


# Inicializar si no existe
if "tablero" not in st.session_state:
    inicializar_juego()

# --- Interfaz de Usuario ---
st.title("🧠 Concentrese 4x4 - Modo 2 Jugadores")

# Marcador de puntuación dinámico
col_j1, col_j2 = st.columns(2)
with col_j1:
    marcador_j1 = f"**Jugador 1:** {st.session_state.puntos_j1} pts"
    if (
        st.session_state.jugador_actual == 1
        and len(st.session_state.parejas_encontradas) < 16
    ):
        st.subheader(f"🟢 {marcador_j1}")
    else:
        st.write(marcador_j1)

with col_j2:
    marcador_j2 = f"**Jugador 2:** {st.session_state.puntos_j2} pts"
    if (
        st.session_state.jugador_actual == 2
        and len(st.session_state.parejas_encontradas) < 16
    ):
        st.subheader(f"🟢 {marcador_j2}")
    else:
        st.write(marcador_j2)

st.divider()

# --- Gestión del Error (Cambio de Turno OBLIGATORIO) ---
if st.session_state.error_pendiente:
    st.error(
        f"❌ ¡No coinciden! Turno para el **Jugador {st.session_state.jugador_actual}**"
    )

    if st.button("Continuar / Pasar Turno"):
        # Se vuelven a ocultar las dos cartas seleccionadas
        st.session_state.reveladas[st.session_state.primer_clic] = False
        st.session_state.reveladas[st.session_state.segundo_clic] = False
        # Limpiar selección
        st.session_state.primer_clic = None
        st.session_state.segundo_clic = None
        st.session_state.error_pendiente = False
        st.rerun()

# --- Lógica del Tablero ---
for fila in range(4):
    cols = st.columns(4)
    for col in range(4):
        idx = fila * 4 + col

        # Estado visual de la carta
        es_pareja = idx in st.session_state.parejas_encontradas
        esta_revelada = st.session_state.reveladas[idx]

        if es_pareja or esta_revelada:
            label = st.session_state.tablero[idx]
            # Deshabilitar si ya está emparejada o si hay un error esperando resolverse
            boton_deshabilitado = True
        else:
            label = "❓"
            # Si hay un error en pantalla, bloqueamos el resto del tablero
            boton_deshabilitado = st.session_state.error_pendiente

        if cols[col].button(label, key=f"btn_{idx}", disabled=boton_deshabilitado):
            if st.session_state.primer_clic is None:
                # Primer Clic
                st.session_state.primer_clic = idx
                st.session_state.reveladas[idx] = True
                st.rerun()
            else:
                # Segundo Clic
                st.session_state.segundo_clic = idx
                st.session_state.reveladas[idx] = True

                idx1 = st.session_state.primer_clic
                idx2 = st.session_state.segundo_clic

                # Caso 1: ¡Hacen Pareja!
                if st.session_state.tablero[idx1] == st.session_state.tablero[idx2]:
                    st.session_state.parejas_encontradas.extend([idx1, idx2])

                    # Sumar punto al jugador del turno actual
                    if st.session_state.jugador_actual == 1:
                        st.session_state.puntos_j1 += 1
                    else:
                        st.session_state.puntos_j2 += 1

                    # Como acertó, mantiene el turno. Solo limpiamos la selección.
                    st.session_state.primer_clic = None
                    st.session_state.segundo_clic = None
                    st.rerun()

                # Caso 2: Fallan (Se activa la bandera de error)
                else:
                    st.session_state.error_pendiente = True
                    # Cambia el turno inmediatamente para el siguiente movimiento
                    st.session_state.jugador_actual = (
                        2 if st.session_state.jugador_actual == 1 else 1
                    )
                    st.rerun()

# --- Pantalla de Victoria ---
if len(st.session_state.parejas_encontradas) == 16:
    st.balloons()
    if st.session_state.puntos_j1 > st.session_state.puntos_j2:
        st.success(
            f"🏆 ¡El Jugador 1 gana el juego con {st.session_state.puntos_j1} puntos!"
        )
    elif st.session_state.puntos_j2 > st.session_state.puntos_j1:
        st.success(
            f"🏆 ¡El Jugador 2 gana el juego con {st.session_state.puntos_j2} puntos!"
        )
    else:
        st.info(f"🤝 ¡Empate! Ambos consiguieron {st.session_state.puntos_j1} puntos.")

# Botón permanente para reiniciar
if st.sidebar.button("Reiniciar Partida"):
    inicializar_juego()
    st.rerun()

import streamlit as st
import pandas as pd
import altair as alt

# --- SESSION STATE INITIALIZATION ---
if 'started' not in st.session_state:
    st.session_state.started = False
if 'lowerbound' not in st.session_state:
    st.session_state.lowerbound = 0
if 'upperbound' not in st.session_state:
    st.session_state.upperbound = 100
if 'initial_min' not in st.session_state:
    st.session_state.initial_min = 0
if 'initial_max' not in st.session_state:
    st.session_state.initial_max = 100
if 'counter' not in st.session_state:
    st.session_state.counter = 1
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

def reset_game():
    st.session_state.started = False
    st.session_state.game_over = False
    st.session_state.counter = 1

# --- UI LAYOUT ---
st.title("🤖 AI Binary Search Guesser")
st.write("Set your range, think of a number, and let the machine find it!")

# --- PHASE 1: SETUP ---
if not st.session_state.started:
    st.subheader("Game Setup")
    col1, col2 = st.columns(2)
    with col1:
        min_val = st.number_input("Batas Bawah (Min)", value=0)
    with col2:
        max_val = st.number_input("Batas Atas (Max)", value=100)

    if st.button("Mulai Game", type="primary", use_container_width=True):
        if min_val >= max_val:
            st.error("Batas atas harus lebih besar dari batas bawah!")
        else:
            st.session_state.initial_min = min_val
            st.session_state.initial_max = max_val
            st.session_state.lowerbound = min_val
            st.session_state.upperbound = max_val
            st.session_state.started = True
            st.rerun()

# --- PHASE 2: GAMEPLAY ---
else:
    if not st.session_state.game_over:
        # Calculate current guess based on your algorithm: (up + low) / 2
        guess = (st.session_state.upperbound + st.session_state.lowerbound) // 2
        
        # Check for contradictions
        if st.session_state.lowerbound > st.session_state.upperbound:
            st.error("⚠️ Angkamu ngaco! (Your inputs are contradictory)")
            if st.button("Restart"):
                reset_game()
                st.rerun()
        else:
            st.subheader(f"Tebakan ke: {st.session_state.counter}")
            st.metric("Apakah angkamu:", guess)

            # Response Buttons
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("Kekecilan (+)", use_container_width=True):
                    st.session_state.lowerbound = guess + 1
                    st.session_state.counter += 1
                    st.rerun()
            with c2:
                if st.button("YA! ✅", type="primary", use_container_width=True):
                    st.session_state.game_over = True
                    st.rerun()
            with c3:
                if st.button("Kegedean (-)", use_container_width=True):
                    st.session_state.upperbound = guess - 1
                    st.session_state.counter += 1
                    st.rerun()

            st.divider()

            # --- VISUALIZATION ---
            st.write("### Visualisasi Range")
            
            # Data for Altair
            full_range = pd.DataFrame({
                'x': [st.session_state.initial_min, st.session_state.initial_max],
                'y': [1, 1]
            })
            active_range = pd.DataFrame({
                'x': [st.session_state.lowerbound, st.session_state.upperbound],
                'y': [1, 1]
            })
            current_guess = pd.DataFrame({
                'x': [guess],
                'y': [1]
            })

            # 1. Background line (Full Range)
            base = alt.Chart(full_range).mark_line(color='#4b4b4b', size=8, strokeCap='round').encode(
                x=alt.X('x:Q', 
                        scale=alt.Scale(domain=[st.session_state.initial_min, st.session_state.initial_max]),
                        title="Number Line"),
                y=alt.Y('y:Q', axis=None)
            )

            # 2. Highlight line (Active Range)
            active = alt.Chart(active_range).mark_line(color='#00d1b2', size=8).encode(
                x='x:Q', y='y:Q'
            )

            # 3. Guess Point (The Dot)
            point = alt.Chart(current_guess).mark_point(
                color='red', size=200, filled=True
            ).encode(x='x:Q', y='y:Q')

            # Combine chart
            viz = (base + active + point).properties(height=100)
            st.altair_chart(viz, use_container_width=True)
            
            st.info(f"Lower: {st.session_state.lowerbound} | Guess: {guess} | Upper: {st.session_state.upperbound}")

    else:
        # --- VICTORY SCREEN ---
        st.success(f"✨ Berhasil! Nomormu adalah { (st.session_state.upperbound + st.session_state.lowerbound) // 2 }")
        st.write(f"Tertebak dalam **{st.session_state.counter}** langkah.")
        st.balloons()
        if st.button("Main Lagi", use_container_width=True):
            reset_game()
            st.rerun()

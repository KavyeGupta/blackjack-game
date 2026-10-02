import streamlit as st
import random

# Page configuration
st.set_page_config(
    page_title="Royal Blackjack Casino",
    page_icon="🃏",
    layout="wide"
)

# Custom Casino Table CSS
st.markdown("""
<style>
    /* Dark Casino Background */
    .stApp {
        background: radial-gradient(circle at center, #0e4e2a 0%, #062b17 100%);
        color: #ffffff;
    }
    
    /* Casino Table Container */
    .table-container {
        background: rgba(0, 0, 0, 0.25);
        border: 2px solid #d4af37;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Realistic Card Styling */
    .card-row {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin: 10px 0;
    }
    .playing-card {
        width: 82px;
        height: 118px;
        background: #ffffff;
        border-radius: 8px;
        box-shadow: 0 5px 12px rgba(0,0,0,0.4);
        padding: 6px;
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-weight: bold;
        transition: transform 0.2s ease;
    }
    .playing-card:hover {
        transform: translateY(-4px);
    }
    .card-hidden {
        width: 82px;
        height: 118px;
        background: repeating-linear-gradient(
            45deg,
            #800020,
            #800020 8px,
            #a30029 8px,
            #a30029 16px
        );
        border: 2px solid #ffffff;
        border-radius: 8px;
        box-shadow: 0 5px 12px rgba(0,0,0,0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        color: #d4af37;
        font-size: 26px;
    }
    .card-red {
        color: #d63031;
    }
    .card-black {
        color: #2d3436;
    }
    .card-top {
        font-size: 14px;
        line-height: 1.1;
        text-align: left;
    }
    .card-center {
        font-size: 28px;
        text-align: center;
        margin-top: -4px;
    }
    .card-bottom {
        font-size: 14px;
        line-height: 1.1;
        text-align: right;
        transform: rotate(180deg);
    }
    
    /* Header & Badge Styling */
    .casino-title {
        text-align: center;
        font-family: 'Georgia', serif;
        color: #ffd700;
        text-shadow: 0 2px 8px rgba(0,0,0,0.8);
        margin-bottom: 5px;
    }
    .score-badge {
        display: inline-block;
        background: #111827;
        border: 1px solid #d4af37;
        color: #ffd700;
        padding: 4px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Card Definitions
SUITS = [("♠", "black"), ("♥", "red"), ("♦", "red"), ("♣", "black")]
RANKS = [
    ("2", 2), ("3", 3), ("4", 4), ("5", 5), ("6", 6),
    ("7", 7), ("8", 8), ("9", 9), ("10", 10),
    ("J", 10), ("Q", 10), ("K", 10), ("A", 11)
]

def make_deck():
    deck = []
    for suit, color in SUITS:
        for rank, val in RANKS:
            deck.append({"rank": rank, "val": val, "suit": suit, "color": color})
    random.shuffle(deck)
    return deck

def calc_score(hand):
    score = sum(card["val"] for card in hand)
    aces = sum(1 for card in hand if card["rank"] == "A")
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1
    return score

def render_cards_html(hand, hide_first=False):
    html = '<div class="card-row">'
    for idx, card in enumerate(hand):
        if idx == 0 and hide_first:
            html += '<div class="card-hidden">🃏</div>'
        else:
            c_class = "card-red" if card["color"] == "red" else "card-black"
            # Keep on one line or without 4-space indentation to prevent Markdown code block triggers
            html += f'<div class="playing-card {c_class}"><div class="card-top">{card["rank"]}<br>{card["suit"]}</div><div class="card-center">{card["suit"]}</div><div class="card-bottom">{card["rank"]}<br>{card["suit"]}</div></div>'
    html += '</div>'
    return html

def reset_round():
    st.session_state.deck = make_deck()
    st.session_state.p1_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
    st.session_state.p2_hand = []
    st.session_state.game_over = False
    st.session_state.result_text = ""
    st.session_state.result_badge = ""
    st.session_state.current_turn = "Player 1"

# Session State Initialization
if "deck" not in st.session_state or len(st.session_state.deck) < 15:
    reset_round()
if "p1_wins" not in st.session_state:
    st.session_state.p1_wins = 0
    st.session_state.p2_wins = 0
    st.session_state.draws = 0

# App Header
st.markdown("<h1 class='casino-title'>♠ ROYAL BLACKJACK CASINO ♠</h1>", unsafe_allow_html=True)

# Settings & Game Mode
col_mode, col_score = st.columns([1, 1])
with col_mode:
    mode = st.radio(
        "Game Mode",
        ["Player vs Dealer (Casino AI)", "2 Players (Pass & Play)"],
        horizontal=True
    )

with col_score:
    st.markdown(
        f"<div style='text-align: right; margin-top: 15px;'><span class='score-badge'>🏆 Wins: P1 ({st.session_state.p1_wins}) | P2/Dealer ({st.session_state.p2_wins}) | Draws ({st.session_state.draws})</span></div>",
        unsafe_allow_html=True
    )

st.write("")

# Table Area
col_left, col_right = st.columns(2)

p1_score = calc_score(st.session_state.p1_hand)

# Player 1 Section
with col_left:
    st.markdown("<div class='table-container'>", unsafe_allow_html=True)
    st.markdown(f"### 👤 Player 1 &nbsp; <span class='score-badge'>Score: {p1_score}</span>", unsafe_allow_html=True)
    st.markdown(render_cards_html(st.session_state.p1_hand), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Player 2 / Dealer Section
with col_right:
    target_name = "🤖 Dealer" if "Dealer" in mode else "👤 Player 2"
    st.markdown("<div class='table-container'>", unsafe_allow_html=True)
    
    if len(st.session_state.p2_hand) == 0:
        st.markdown(f"### {target_name} &nbsp; <span class='score-badge'>Waiting for Turn...</span>", unsafe_allow_html=True)
        st.write("Cards will be dealt when Player 1 stands.")
    else:
        hide = ("Dealer" in mode and not st.session_state.game_over)
        p2_score = calc_score(st.session_state.p2_hand)
        display_score = "?" if hide else p2_score
        st.markdown(f"### {target_name} &nbsp; <span class='score-badge'>Score: {display_score}</span>", unsafe_allow_html=True)
        st.markdown(render_cards_html(st.session_state.p2_hand, hide_first=hide), unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Game Control Logic
if not st.session_state.game_over:
    if st.session_state.current_turn == "Player 1":
        st.info("👉 **Player 1's turn!** Take another card or stand.")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("➕ Hit", use_container_width=True):
                st.session_state.p1_hand.append(st.session_state.deck.pop())
                if calc_score(st.session_state.p1_hand) > 21:
                    st.session_state.game_over = True
                    st.session_state.result_text = f"💥 Player 1 busts! {target_name} WINS!"
                    st.session_state.result_badge = "error"
                    st.session_state.p2_wins += 1
                st.rerun()
        with b2:
            if st.button("🛑 Stand", use_container_width=True):
                st.session_state.current_turn = "Player 2"
                st.session_state.p2_hand = [st.session_state.deck.pop(), st.session_state.deck.pop()]
                
                # If Dealer AI mode, automatically play out Dealer's hand
                if "Dealer" in mode:
                    while calc_score(st.session_state.p2_hand) < 17:
                        st.session_state.p2_hand.append(st.session_state.deck.pop())
                    
                    st.session_state.game_over = True
                    p1_final = calc_score(st.session_state.p1_hand)
                    d_final = calc_score(st.session_state.p2_hand)
                    
                    if d_final > 21:
                        st.session_state.result_text = "🎉 Dealer busts! **Player 1 WINS!**"
                        st.session_state.result_badge = "success"
                        st.session_state.p1_wins += 1
                    elif p1_final > d_final:
                        st.session_state.result_text = f"🎉 **Player 1 WINS!** ({p1_final} vs {d_final})"
                        st.session_state.result_badge = "success"
                        st.session_state.p1_wins += 1
                    elif d_final > p1_final:
                        st.session_state.result_text = f"💀 **Dealer WINS!** ({d_final} vs {p1_final})"
                        st.session_state.result_badge = "error"
                        st.session_state.p2_wins += 1
                    else:
                        st.session_state.result_text = f"🤝 **PUSH / DRAW!** ({p1_final} each)"
                        st.session_state.result_badge = "warning"
                        st.session_state.draws += 1
                st.rerun()

    elif st.session_state.current_turn == "Player 2" and "2 Players" in mode:
        st.info("👉 **Player 2's turn!** Take another card or stand.")
        b1, b2 = st.columns(2)
        with b1:
            if st.button("➕ Hit (Player 2)", use_container_width=True):
                st.session_state.p2_hand.append(st.session_state.deck.pop())
                if calc_score(st.session_state.p2_hand) > 21:
                    st.session_state.game_over = True
                    st.session_state.result_text = "💥 Player 2 busts! **Player 1 WINS!**"
                    st.session_state.result_badge = "success"
                    st.session_state.p1_wins += 1
                st.rerun()
        with b2:
            if st.button("🛑 Stand (Player 2)", use_container_width=True):
                st.session_state.game_over = True
                p1_final = calc_score(st.session_state.p1_hand)
                p2_final = calc_score(st.session_state.p2_hand)
                
                if p1_final > p2_final:
                    st.session_state.result_text = f"🎉 **Player 1 WINS!** ({p1_final} vs {p2_final})"
                    st.session_state.result_badge = "success"
                    st.session_state.p1_wins += 1
                elif p2_final > p1_final:
                    st.session_state.result_text = f"🎉 **Player 2 WINS!** ({p2_final} vs {p1_final})"
                    st.session_state.result_badge = "success"
                    st.session_state.p2_wins += 1
                else:
                    st.session_state.result_text = f"🤝 **IT'S A DRAW!** ({p1_final} each)"
                    st.session_state.result_badge = "warning"
                    st.session_state.draws += 1
                st.rerun()

# Result Presentation
if st.session_state.game_over:
    if st.session_state.result_badge == "success":
        st.success(st.session_state.result_text)
        st.balloons()
    elif st.session_state.result_badge == "error":
        st.error(st.session_state.result_text)
    else:
        st.warning(st.session_state.result_text)

    if st.button("🔄 Deal Next Round", use_container_width=True):
        reset_round()
        st.rerun()
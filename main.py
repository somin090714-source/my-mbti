import random
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="MBTI 단짝 포켓몬 찾기",
    page_icon="🌼",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 모든 스타일은 이 파일 안에 포함되어 있습니다.
st.markdown(
    """
    <style>
    :root {
        --cream: #fff9e9;
        --paper: #fffef9;
        --yellow: #f5d675;
        --yellow-dark: #e8bd4c;
        --brown: #66502d;
        --muted: #8c7958;
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 5%, rgba(255, 224, 125, .22), transparent 26%),
            linear-gradient(180deg, #fff9e9 0%, #fffdf6 100%);
        color: var(--brown);
        font-family: 'Noto Sans KR', sans-serif;
    }

    [data-testid="stHeader"] { background: rgba(255,249,233,.82); }
    .block-container {
        max-width: 900px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, p, label, button { font-family: 'Noto Sans KR', sans-serif; }

    .hero {
        text-align: center;
        padding: 1.2rem .8rem .7rem;
    }
    .hero .sparkle { font-size: 2rem; }
    .hero h1 {
        font-family: 'Jua', 'Noto Sans KR', sans-serif;
        font-size: clamp(2rem, 6vw, 3.15rem);
        line-height: 1.25;
        color: #745526;
        margin: .35rem 0 .65rem;
    }
    .hero p {
        color: var(--muted);
        font-size: 1.05rem;
        line-height: 1.85;
        margin: 0 auto;
    }
    .section-label {
        text-align: center;
        color: #8a6a32;
        font-weight: 800;
        margin: 1.2rem 0 .7rem;
        font-size: 1.05rem;
    }
    div[data-testid="stButton"] button {
        border: 2px solid #f0d994;
        border-radius: 15px;
        background: rgba(255,255,255,.82);
        color: #6f562d;
        min-height: 3rem;
        font-size: 1rem;
        font-weight: 800;
        transition: transform .15s ease, background .15s ease;
    }
    div[data-testid="stButton"] button:hover {
        border-color: #e6bd4b;
        background: #fff0bd;
        color: #5c451d;
        transform: translateY(-2px);
    }
    div[data-testid="stButton"] button:focus {
        box-shadow: 0 0 0 .18rem rgba(232,189,76,.22);
        border-color: #d9ad39;
    }
    .result-card {
        text-align: center;
        background: rgba(255,255,255,.88);
        border: 2px solid #f1d88f;
        border-radius: 26px;
        padding: 1.35rem 1.2rem 1.5rem;
        margin-top: 1.2rem;
        box-shadow: 0 12px 32px rgba(126, 97, 38, .08);
    }
    .badge {
        display: inline-block;
        background: #fff0bd;
        color: #795d27;
        border-radius: 999px;
        padding: .45rem .9rem;
        font-weight: 800;
        font-size: .92rem;
    }
    .poke-name {
        font-family: 'Jua', 'Noto Sans KR', sans-serif;
        font-size: clamp(2rem, 5vw, 2.6rem);
        color: #614a25;
        margin: .8rem 0 .1rem;
    }
    .english-name { color: #a18a5b; margin: 0 0 .7rem; }
    .type-pill {
        display: inline-block;
        margin: .15rem;
        padding: .35rem .75rem;
        border-radius: 999px;
        background: #f9edcc;
        color: #725629;
        font-size: .92rem;
        font-weight: 800;
    }
    .reason {
        max-width: 610px;
        margin: 1rem auto;
        color: #6e5a3b;
        font-size: 1.05rem;
        line-height: 1.95;
        word-break: keep-all;
    }
    .match-box {
        max-width: 520px;
        margin: 1rem auto .5rem;
        background: #fff7df;
        border-radius: 17px;
        padding: .9rem 1rem;
        line-height: 1.8;
    }
    .match-box strong { color: #987027; }
    .small-note {
        text-align: center;
        color: #a08c68;
        font-size: .82rem;
        line-height: 1.7;
        margin-top: 2rem;
    }
    @media (max-width: 520px) {
        .block-container { padding: 1rem .8rem 2rem; }
        .hero { padding-top: .5rem; }
        .result-card { padding: 1.1rem .75rem 1.25rem; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

POKEMON = {
    "INTJ": {
        "name": "뮤츠", "english": "Mewtwo", "dex": 150,
        "types": ["에스퍼"], "emoji": "🔮", "compatible": "ENFP",
        "trait": "전략가 · 독립적 · 통찰력",
        "reason": "깊이 생각하고 자신만의 목표를 향해 나아가는 모습이 뮤츠와 닮았어요.\n차분한 집중력과 강한 의지로 어려운 문제도 해결해 나가는 타입이에요."
    },
    "INTP": {
        "name": "메타몽", "english": "Ditto", "dex": 132,
        "types": ["노말"], "emoji": "🟣", "compatible": "ENTJ",
        "trait": "호기심 · 분석적 · 유연함",
        "reason": "새로운 가능성을 탐구하고 독특한 방식으로 생각하는 모습이 메타몽 같아요.\n정해진 틀에 갇히지 않고 여러 관점에서 세상을 바라봐요."
    },
    "ENTJ": {
        "name": "리자몽", "english": "Charizard", "dex": 6,
        "types": ["불꽃", "비행"], "emoji": "🔥", "compatible": "INTP",
        "trait": "리더십 · 추진력 · 자신감",
        "reason": "목표를 정하면 힘차게 앞으로 나아가는 리더 타입이에요.\n자신감과 추진력으로 주변에 강한 에너지를 전하는 점이 리자몽과 닮았어요."
    },
    "ENTP": {
        "name": "팬텀", "english": "Gengar", "dex": 94,
        "types": ["고스트", "독"], "emoji": "👻", "compatible": "INFJ",
        "trait": "재치 · 창의력 · 장난기",
        "reason": "기발한 아이디어와 장난스러운 매력으로 분위기를 바꾸는 타입이에요.\n뻔한 것보다 새롭고 재미있는 일을 찾아 나서는 점이 팬텀과 잘 어울려요."
    },
    "INFJ": {
        "name": "루카리오", "english": "Lucario", "dex": 448,
        "types": ["격투", "강철"], "emoji": "💙", "compatible": "ENTP",
        "trait": "공감력 · 신념 · 깊은 마음",
        "reason": "다른 사람의 마음을 세심하게 살피면서도 자신만의 신념을 지켜요.\n조용하지만 소중한 사람을 위해 용기를 내는 모습이 루카리오와 닮았어요."
    },
    "INFP": {
        "name": "이브이", "english": "Eevee", "dex": 133,
        "types": ["노말"], "emoji": "🤎", "compatible": "ENFJ",
        "trait": "상상력 · 다정함 · 가능성",
        "reason": "풍부한 감수성과 따뜻한 마음을 가진 당신은 이브이와 잘 어울려요.\n자신만의 가능성을 품고 천천히 성장해 가는 모습이 매력적이에요."
    },
    "ENFJ": {
        "name": "피카츄", "english": "Pikachu", "dex": 25,
        "types": ["전기"], "emoji": "⚡", "compatible": "INFP",
        "trait": "친화력 · 따뜻함 · 응원",
        "reason": "밝은 에너지로 친구들을 응원하고 함께 힘을 내게 해요.\n주변을 따뜻하게 챙기는 사교적인 모습이 피카츄와 닮았어요."
    },
    "ENFP": {
        "name": "파치리스", "english": "Pachirisu", "dex": 417,
        "types": ["전기"], "emoji": "🐿️", "compatible": "INTJ",
        "trait": "활발함 · 호기심 · 낙천적",
        "reason": "새로운 사람과 경험을 만나는 걸 좋아하는 활기찬 타입이에요.\n톡톡 튀는 에너지와 장난기 넘치는 매력이 파치리스와 잘 맞아요."
    },
    "ISTJ": {
        "name": "거북왕", "english": "Blastoise", "dex": 9,
        "types": ["물"], "emoji": "🐢", "compatible": "ESFP",
        "trait": "책임감 · 성실함 · 신뢰",
        "reason": "맡은 일을 차근차근 해내고 약속을 소중히 여기는 타입이에요.\n든든하게 자기 자리를 지키는 모습이 거북왕과 닮았어요."
    },
    "ISFJ": {
        "name": "잠만보", "english": "Snorlax", "dex": 143,
        "types": ["노말"], "emoji": "💤", "compatible": "ESFP",
        "trait": "배려 · 안정감 · 포근함",
        "reason": "편안한 분위기를 만들고 소중한 사람들을 조용히 챙겨 줘요.\n포근하고 믿음직한 매력이 잠만보와 잘 어울리는 이유예요."
    },
    "ESTJ": {
        "name": "괴력몬", "english": "Machamp", "dex": 68,
        "types": ["격투"], "emoji": "💪", "compatible": "ISFP",
        "trait": "실행력 · 책임감 · 조직력",
        "reason": "계획을 세우고 실제 행동으로 옮기는 데 강한 타입이에요.\n팀을 이끌고 끝까지 해내려는 책임감이 괴력몬을 떠올리게 해요."
    },
    "ESFJ": {
        "name": "푸린", "english": "Jigglypuff", "dex": 39,
        "types": ["노말", "페어리"], "emoji": "🎤", "compatible": "ISFP",
        "trait": "친절함 · 사교성 · 다정함",
        "reason": "사람들과 어울리고 모두가 즐거운 분위기를 만드는 걸 좋아해요.\n다정한 말과 행동으로 주변을 편안하게 해 주는 점이 푸린과 닮았어요."
    },
    "ISTP": {
        "name": "메타그로스", "english": "Metagross", "dex": 376,
        "types": ["강철", "에스퍼"], "emoji": "🤖", "compatible": "ESFJ",
        "trait": "침착함 · 분석력 · 실용성",
        "reason": "감정보다 상황을 차분히 분석하고 해결책을 찾는 데 능숙해요.\n말보다 실력으로 보여 주는 모습이 메타그로스와 잘 어울려요."
    },
    "ISFP": {
        "name": "치코리타", "english": "Chikorita", "dex": 152,
        "types": ["풀"], "emoji": "🍃", "compatible": "ESFJ",
        "trait": "감각적 · 온화함 · 자기만의 취향",
        "reason": "부드럽고 온화하며 자신만의 취향을 소중히 여겨요.\n평화로운 분위기를 좋아하고 주변에 편안함을 주는 점이 치코리타와 닮았어요."
    },
    "ESTP": {
        "name": "갸라도스", "english": "Gyarados", "dex": 130,
        "types": ["물", "비행"], "emoji": "🌊", "compatible": "ISFJ",
        "trait": "대담함 · 행동력 · 도전 정신",
        "reason": "망설이기보다 직접 도전하며 경험을 쌓는 행동파예요.\n강렬한 에너지와 대담함으로 상황을 돌파하는 모습이 갸라도스와 닮았어요."
    },
    "ESFP": {
        "name": "꼬부기", "english": "Squirtle", "dex": 7,
        "types": ["물"], "emoji": "💧", "compatible": "ISTJ",
        "trait": "명랑함 · 사교성 · 긍정 에너지",
        "reason": "즐거운 순간을 잘 찾아내고 친구들과 함께할 때 더 빛나요.\n명랑하고 친근한 매력으로 주변에 웃음을 주는 점이 꼬부기와 잘 어울려요."
    },
}

if "selected_mbti" not in st.session_state:
    st.session_state.selected_mbti = None

if "celebrate" not in st.session_state:
    st.session_state.celebrate = False


def choose_mbti(mbti):
    st.session_state.selected_mbti = mbti
    st.session_state.celebrate = True


st.markdown(
    """
    <div class="hero">
      <div class="sparkle">🌼 ✨ ⚡</div>
      <h1>MBTI 단짝 포켓몬 찾기</h1>
      <p>내 성격과 찰떡궁합인 포켓몬은 누구일까요?<br>
      나의 MBTI를 선택하고 운명의 단짝을 만나 보세요!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-label">💛 내 MBTI를 선택해 주세요</div>', unsafe_allow_html=True)

mbti_order = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP",
]

columns = st.columns(4)
for index, mbti in enumerate(mbti_order):
    with columns[index % 4]:
        label = "✓ " + mbti if st.session_state.selected_mbti == mbti else mbti
        st.button(
            label,
            key=f"mbti_{mbti}",
            use_container_width=True,
            on_click=choose_mbti,
            args=(mbti,),
        )

selected = st.session_state.selected_mbti

if selected:
    pokemon = POKEMON[selected]

    st.markdown("---")

    # 브라우저에서 축하 효과를 보여 줍니다. 별도 패키지가 필요하지 않습니다.
    if st.session_state.celebrate:
        st.balloons()
        components.html(
            """
            <div style="position:fixed; inset:0; pointer-events:none; z-index:999999;">
              <canvas id="confetti-canvas" style="width:100%;height:100%;"></canvas>
            </div>
            <script>
              const canvas = document.getElementById('confetti-canvas');
              const ctx = canvas.getContext('2d');
              let w = canvas.width = window.innerWidth;
              let h = canvas.height = window.innerHeight;
              const colors = ['#f5d675','#f8b84e','#f59a9a','#b8d9a2','#c7b7ed','#fff0bd'];
              const bits = Array.from({length:120}, () => ({
                x: Math.random()*w, y: -Math.random()*h,
                r: 3+Math.random()*5, s: 2+Math.random()*4,
                a: Math.random()*Math.PI*2,
                c: colors[Math.floor(Math.random()*colors.length)]
              }));
              let frame = 0;
              function draw() {
                ctx.clearRect(0,0,w,h);
                bits.forEach(b => {
                  b.y += b.s; b.x += Math.sin(b.a += .04)*1.4;
                  ctx.fillStyle = b.c;
                  ctx.beginPath();
                  ctx.ellipse(b.x,b.y,b.r,b.r*.65,b.a,0,Math.PI*2);
                  ctx.fill();
                  if (b.y > h+10) { b.y = -10; b.x = Math.random()*w; }
                });
                frame++;
                if (frame < 170) requestAnimationFrame(draw);
                else ctx.clearRect(0,0,w,h);
              }
              draw();
              window.addEventListener('resize', () => {
                w = canvas.width = window.innerWidth;
                h = canvas.height = window.innerHeight;
              });
            </script>
            """,
            height=0,
            scrolling=False,
        )
        st.session_state.celebrate = False

    st.markdown(
        f"""
        <div class="result-card">
          <div class="badge">🎉 {selected}의 단짝 포켓몬</div>
          <div class="poke-name">{pokemon["name"]}</div>
          <p class="english-name">{pokemon["english"]}</p>
          <div>{''.join(f'<span class="type-pill">{t} 타입</span>' for t in pokemon["types"])}</div>
          <p style="color:#9b8356;margin-top:.8rem;">{pokemon["trait"]}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 한국 포켓몬 공식 도감의 이미지 주소 규칙을 사용합니다.
    image_url = (
        "https://data1.pokemonkorea.co.kr/newdata/pokedex/mid/"
        + str(pokemon["dex"]).zfill(4)
        + "01.png"
    )

    # HTML img를 사용해 공식 이미지 서버에 Referer를 보내지 않도록 설정합니다.
    # 이미지가 로드되지 않으면 해당 포켓몬의 이모지를 대신 표시합니다.
    components.html(
        f"""
        <div style="display:flex;justify-content:center;align-items:center;min-height:250px;">
          <img
            src="{image_url}"
            alt="{pokemon['name']}"
            referrerpolicy="no-referrer"
            style="width:250px;height:250px;object-fit:contain;"
            onerror="this.style.display='none';this.nextElementSibling.style.display='block';"
          >
          <div style="display:none;font-size:100px;text-align:center;">{pokemon['emoji']}</div>
        </div>
        """,
        height=270,
        scrolling=False,
    )

    st.markdown(
        f"""
        <div class="reason">
          <strong>🌟 이런 점이 당신과 닮았어요</strong><br>
          {pokemon["reason"].replace(chr(10), "<br>")}
        </div>
        <div class="match-box">
          💛 <strong>환상의 궁합 MBTI</strong><br>
          <span style="font-size:1.35rem;font-weight:900;">{pokemon["compatible"]}</span><br>
          서로 다른 매력이 만나 좋은 팀이 될 수 있어요!
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("🔄 다른 포켓몬 만나기", use_container_width=True):
        choices = [m for m in mbti_order if m != selected]
        st.session_state.selected_mbti = random.choice(choices)
        st.session_state.celebrate = True
        st.rerun()

else:
    st.info("👆 위의 MBTI 버튼 중 하나를 눌러 결과를 확인해 보세요!")

st.markdown(
    """
    <div class="small-note">
      결과는 재미를 위한 MBTI 기반의 비공식 콘텐츠입니다.<br>
      포켓몬 이미지 출처: <a href="https://www.pokemonkorea.co.kr/pokedex"
      target="_blank" style="color:#9a7c42;">포켓몬코리아 공식 도감</a>
    </div>
    """,
    unsafe_allow_html=True,
)

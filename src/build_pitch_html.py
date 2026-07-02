# -*- coding: utf-8 -*-
"""
Gera o pitch em HTML (uma página, apresentável em tela cheia) com as figuras
embutidas em base64 — assim o arquivo é 100% autossuficiente.

Uso:  py src/build_pitch_html.py   ->   slides/pitch_lazypredict.html
"""
import base64
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FIG = RAIZ / "figuras"
DADOS = RAIZ / "dados"
SAIDA = RAIZ / "slides" / "pitch_lazypredict.html"


def b64(nome):
    dados = (FIG / nome).read_bytes()
    return "data:image/png;base64," + base64.b64encode(dados).decode()


IMG = {
    "serie": b64("01_serie_casos.png"),
    "dow": b64("03_efeito_dia_semana.png"),
    "tabela": b64("lazy_00_tabela.png"),
    "rank": b64("lazy_01_leaderboard.png"),
    "prev": b64("lazy_02_previsao.png"),
}

lz = json.loads((DADOS / "lazy_resultados.json").read_text(encoding="utf-8"))
melhor = lz["melhor"]

HTML = f"""<style>
:root {{
  --bg:#0a0a0a; --panel:#151515; --line:rgba(255,255,255,.09);
  --red:#C81E1E; --red-hi:#FF5C5C; --green:#43D17A;
  --ink:#ededed; --muted:#9a9a9a;
  --mono:ui-monospace,"Cascadia Code","Consolas","SFMono-Regular",monospace;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font-family:var(--sans);
       -webkit-font-smoothing:antialiased; }}
.deck {{ scroll-snap-type:y mandatory; height:100vh; overflow-y:auto; scroll-behavior:smooth; }}
@media (prefers-reduced-motion:reduce){{ .deck{{scroll-behavior:auto;}} }}

.slide {{ scroll-snap-align:start; min-height:100vh; padding:6vh 7vw 8vh;
         display:flex; flex-direction:column; justify-content:center;
         position:relative; border-bottom:1px solid var(--line); }}
.slide-inner {{ width:100%; max-width:1060px; margin:0 auto; }}

.eyebrow {{ font-family:var(--mono); font-size:.78rem; letter-spacing:.22em;
           text-transform:uppercase; color:var(--muted); margin:0 0 1.1rem; }}
.head {{ display:flex; align-items:center; gap:.7rem; margin:0 0 .3rem; }}
.pill {{ width:26px; height:12px; border-radius:6px; background:var(--red); flex:none; }}
.ftitle {{ font-family:var(--mono); font-weight:700; font-size:1.05rem;
          text-transform:lowercase; letter-spacing:.02em; color:#fff; margin:0; }}
.rule {{ height:2px; background:var(--red); border-radius:2px; margin:.55rem 0 1.8rem;
        width:100%; }}
h1.big {{ font-size:clamp(2.1rem,5vw,3.9rem); line-height:1.04; margin:.2rem 0 1rem;
         font-weight:800; letter-spacing:-.02em; text-wrap:balance; }}
h2.q {{ font-size:clamp(1.7rem,3.8vw,2.9rem); line-height:1.12; margin:.2rem 0 1.1rem;
       font-weight:800; letter-spacing:-.015em; text-wrap:balance; }}
p.lead {{ font-size:clamp(1.05rem,1.7vw,1.35rem); line-height:1.55; color:#dcdcdc;
         max-width:60ch; margin:.2rem 0 1rem; }}
.em {{ color:var(--red-hi); font-weight:700; }}
.good {{ color:var(--green); font-weight:700; }}
.muted {{ color:var(--muted); }}

.figcard {{ background:#fff; border:3px solid var(--red); border-radius:12px;
           padding:10px; margin:.4rem 0; box-shadow:0 18px 50px rgba(0,0,0,.45); }}
.figcard img {{ display:block; width:100%; height:auto; border-radius:4px; }}
.figdark {{ background:#0d0d0d; border:1px solid var(--line); border-radius:12px;
           padding:8px; margin:.4rem 0; box-shadow:0 18px 50px rgba(0,0,0,.45); }}
.figdark img {{ display:block; width:100%; height:auto; border-radius:6px; }}
.cap {{ font-size:.92rem; color:var(--muted); margin:.7rem 0 0; max-width:70ch; }}

.stats {{ display:flex; flex-wrap:wrap; gap:1.4rem 2.6rem; margin:.4rem 0 1.4rem; }}
.stat b {{ display:block; font-family:var(--mono); font-weight:700;
          font-size:clamp(1.8rem,4vw,3rem); color:#fff; line-height:1;
          font-variant-numeric:tabular-nums; }}
.stat span {{ font-size:.9rem; color:var(--muted); letter-spacing:.02em; }}
.stat .hl {{ color:var(--red-hi); }}

.chips {{ display:flex; flex-wrap:wrap; gap:.7rem; margin:1.2rem 0 0; }}
.chip {{ font-family:var(--mono); font-size:.9rem; color:#fff; padding:.5rem .9rem;
        border:1.5px solid var(--red); border-radius:999px; background:rgba(200,30,30,.12); }}

.codebox {{ font-family:var(--mono); font-size:clamp(.82rem,1.3vw,1rem);
           background:#050505; border:1px solid var(--line); border-left:3px solid var(--red);
           border-radius:8px; padding:1rem 1.2rem; margin:.6rem 0 1.1rem; overflow-x:auto;
           color:#e8e8e8; line-height:1.7; }}
.codebox .k {{ color:var(--red-hi); }}
.codebox .c {{ color:var(--muted); }}

.formula {{ font-family:var(--mono); font-size:clamp(1rem,2.1vw,1.7rem); text-align:center;
           background:#050505; border:1px solid var(--line); border-radius:10px;
           padding:1.4rem 1rem; margin:1rem 0; color:#fff; overflow-x:auto;
           letter-spacing:.02em; }}

.grid2 {{ display:grid; grid-template-columns:1.05fr .95fr; gap:2.4rem; align-items:center; }}
@media (max-width:820px){{ .grid2{{grid-template-columns:1fr;}} }}

ol.pts {{ counter-reset:p; list-style:none; padding:0; margin:.6rem 0 0;
         display:flex; flex-direction:column; gap:1.1rem; }}
ol.pts li {{ position:relative; padding-left:3.1rem; font-size:clamp(1rem,1.6vw,1.28rem);
            line-height:1.5; max-width:66ch; }}
ol.pts li::before {{ counter-increment:p; content:counter(p); position:absolute; left:0; top:-2px;
   font-family:var(--mono); font-weight:700; color:var(--red); font-size:1.5rem;
   border-bottom:2px solid var(--red); padding:0 .5rem .1rem; }}

.pagenum {{ position:absolute; right:2.2vw; bottom:2.2vh; font-family:var(--mono);
           font-size:.78rem; color:var(--muted); font-variant-numeric:tabular-nums; }}
.hint {{ font-family:var(--mono); font-size:.82rem; color:var(--muted); margin-top:2.4rem; }}
.hint b {{ color:var(--red-hi); }}
.author {{ font-family:var(--mono); font-size:.92rem; color:var(--muted); margin-top:1.6rem; }}
.author b {{ color:var(--ink); font-weight:700; }}

.dots {{ position:fixed; right:1.1vw; top:50%; transform:translateY(-50%); z-index:20;
        display:flex; flex-direction:column; gap:.55rem; }}
.dots a {{ width:9px; height:9px; border-radius:50%; background:#3a3a3a; display:block;
          transition:background .2s,transform .2s; }}
.dots a.on {{ background:var(--red); transform:scale(1.35); }}
:focus-visible {{ outline:2px solid var(--red-hi); outline-offset:3px; }}
</style>

<nav class="dots" id="dots" aria-label="Navegação dos slides"></nav>

<div class="deck" id="deck">

  <!-- 1 CAPA -->
  <section class="slide" id="s1">
    <div class="slide-inner">
      <p class="eyebrow">Seminário · Séries Temporais · UFPB</p>
      <h1 class="big">EpiCurve<br>Analyzer</h1>
      <p class="lead">Prever a próxima onda da COVID-19 —
        <span class="em">sem deduzir uma única fórmula</span>.</p>
      <div class="chips"><span class="chip">powered by LazyPredict</span></div>
      <p class="author"><b>Allan Vasconcelos</b> · UFPB · 2026</p>
      <p class="hint">use <b>←</b> <b>→</b> ou role a página para navegar</p>
    </div>
    <span class="pagenum">01</span>
  </section>

  <!-- 2 O PROBLEMA -->
  <section class="slide" id="s2">
    <div class="slide-inner">
      <div class="head"><span class="pill"></span><p class="ftitle">o problema</p></div>
      <div class="rule"></div>
      <h2 class="q">Quantos casos teremos nas <span class="em">próximas 4 semanas</span>?</h2>
      <p class="lead">Essa única resposta decide leitos de UTI, oxigênio, insumos e escala de
        equipes. Prever cedo é <span class="good">se preparar</span>; errar é hospital
        lotado — ou recurso caríssimo jogado fora.</p>
      <div class="chips">
        <span class="chip">UTI &amp; leitos</span>
        <span class="chip">oxigênio &amp; insumos</span>
        <span class="chip">escala de equipes</span>
        <span class="chip">quando afrouxar / apertar</span>
      </div>
    </div>
    <span class="pagenum">02</span>
  </section>

  <!-- 3 A ESCALA -->
  <section class="slide" id="s3">
    <div class="slide-inner">
      <div class="head"><span class="pill"></span><p class="ftitle">a curva que precisamos prever</p></div>
      <div class="rule"></div>
      <div class="stats">
        <div class="stat"><b class="hl">5,23 mi</b><span>casos confirmados</span></div>
        <div class="stat"><b>167 mil</b><span>óbitos</span></div>
        <div class="stat"><b class="hl">37.611</b><span>pico de casos em 1 dia</span></div>
      </div>
      <div class="figcard"><img src="{IMG['serie']}" alt="Casos e óbitos diários de COVID-19 em São Paulo, 2020 a 2022"></div>
      <p class="cap">São Paulo, 2020–2022. Três ondas, subidas explosivas e um serrilhado
        semanal — difícil de prever no olho.</p>
    </div>
    <span class="pagenum">03</span>
  </section>

  <!-- 4 OS DADOS -->
  <section class="slide" id="s4">
    <div class="slide-inner">
      <div class="head"><span class="pill"></span><p class="ftitle">os dados · escala big data</p></div>
      <div class="rule"></div>
      <h2 class="q"><span class="em">3,85 milhões</span> de registros brutos.</h2>
      <div class="stats">
        <div class="stat"><b>18</b><span>colunas</span></div>
        <div class="stat"><b>5.570</b><span>municípios do Brasil</span></div>
        <div class="stat"><b>762</b><span>dias após recortar SP</span></div>
        <div class="stat"><b>92 MB</b><span>comprimido (.csv.gz)</span></div>
      </div>
      <p class="lead">Fonte oficial <span class="em">DataSUS / Brasil.IO</span>, de 25/02/2020 a
        27/03/2022. Filtramos o estado de SP e agregamos por dia:
        <span class="good">uma série diária limpa de 762 pontos</span> — a matéria-prima da previsão.</p>
    </div>
    <span class="pagenum">04</span>
  </section>

  <!-- 5 O DESAFIO -->
  <section class="slide" id="s5">
    <div class="slide-inner">
      <div class="head"><span class="pill"></span><p class="ftitle">o dado é sujo</p></div>
      <div class="rule"></div>
      <div class="grid2">
        <div>
          <h2 class="q">Fim de semana quase não testa.</h2>
          <p class="lead">A curva <span class="em">serrilha toda semana</span>: domingo registra
            metade da média; quinta, quase 40% acima. Não é a epidemia mudando —
            é o <span class="muted">cartório</span> (subnotificação).</p>
          <div class="chips">
            <span class="chip">domingo ≈ 0,49×</span>
            <span class="chip">quinta ≈ 1,38×</span>
          </div>
        </div>
        <div class="figcard"><img src="{IMG['dow']}" alt="Fator sazonal por dia da semana"></div>
      </div>
      <p class="cap">Esse padrão semanal é justamente o que um bom modelo precisa capturar.</p>
    </div>
    <span class="pagenum">05</span>
  </section>

  <!-- 6 O JEITO DIFÍCIL -->
  <section class="slide" id="s6">
    <div class="slide-inner">
      <div class="head"><span class="pill"></span><p class="ftitle">o caminho difícil</p></div>
      <div class="rule"></div>
      <h2 class="q">O jeito clássico: <span class="em">SARIMA</span>.</h2>
      <div class="formula">Φ<sub>P</sub>(B<sup>s</sup>) φ<sub>p</sub>(B) (1−B)<sup>d</sup>(1−B<sup>s</sup>)<sup>D</sup> y<sub>t</sub> = Θ<sub>Q</sub>(B<sup>s</sup>) θ<sub>q</sub>(B) ε<sub>t</sub></div>
      <p class="lead">Semanas escolhendo estacionariedade, lendo ACF/PACF e caçando os parâmetros
        (p,d,q)(P,D,Q)… <span class="muted">Eu não vi quase nada disso — e não quero deduzir na mão.</span></p>
      <h2 class="q" style="margin-top:1.4rem">E se a <span class="good">máquina</span> escolhesse o modelo por mim?</h2>
    </div>
    <span class="pagenum">06</span>
  </section>

  <!-- 7 O TRUQUE -->
  <section class="slide" id="s7">
    <div class="slide-inner">
      <div class="head"><span class="pill"></span><p class="ftitle">o truque: série → tabela</p></div>
      <div class="rule"></div>
      <p class="lead">Toda série temporal vira uma <span class="em">tabela comum</span>: para prever
        <span class="good">hoje</span>, uso como pistas o passado dela mesma.</p>
      <div class="figdark"><img src="{IMG['tabela']}" alt="Série temporal transformada em tabela supervisionada"></div>
      <p class="cap">Pistas (features): ontem, 7 dias atrás, média da semana, dia da semana…
        → alvo: casos de hoje. Resultado: {lz['n_treino']+lz['n_teste']} linhas × {lz['n_features']} pistas.
        Agora é um problema de aprendizado de máquina qualquer.</p>
    </div>
    <span class="pagenum">07</span>
  </section>

  <!-- 8 A MÁGICA -->
  <section class="slide" id="s8">
    <div class="slide-inner">
      <div class="head"><span class="pill"></span><p class="ftitle">a mágica: uma linha</p></div>
      <div class="rule"></div>
      <div class="codebox">
<span class="c"># o professor sugeriu isto:</span><br>
<span class="k">from</span> lazypredict.Supervised <span class="k">import</span> LazyRegressor<br>
modelos, _ = LazyRegressor().<span class="k">fit</span>(X_tr, X_te, y_tr, y_te)
      </div>
      <h2 class="q"><span class="em">{lz['n_modelos_testados']} modelos</span> treinados e ranqueados
        sozinhos. Em segundos.</h2>
      <div class="figdark"><img src="{IMG['rank']}" alt="Ranking automático dos modelos pelo LazyPredict"></div>
    </div>
    <span class="pagenum">08</span>
  </section>

  <!-- 9 O RESULTADO -->
  <section class="slide" id="s9">
    <div class="slide-inner">
      <div class="head"><span class="pill"></span><p class="ftitle">o resultado</p></div>
      <div class="rule"></div>
      <div class="grid2">
        <div>
          <div class="stat" style="margin-bottom:1.2rem">
            <b class="good" style="font-size:clamp(1.6rem,3.4vw,2.5rem)">{melhor['modelo']}</b>
            <span>vencedor escolhido pelo LazyPredict</span>
          </div>
          <div class="stats">
            <div class="stat"><b class="good">{melhor['rmse']:.0f}</b><span>RMSE (erro)</span></div>
            <div class="stat"><b>{melhor['mae']:.0f}</b><span>MAE</span></div>
          </div>
          <p class="lead">Sem deduzir nada, o vencedor <span class="good">empatou com o SARIMA</span>
            feito à mão no seminário inteiro (<span class="muted">567</span>) e
            <span class="em">ganhou</span> de ARIMA (714), SES (725) e Holt (709).</p>
        </div>
        <div class="figdark"><img src="{IMG['prev']}" alt="Previsão do melhor modelo contra os casos reais"></div>
      </div>
      <p class="cap">Honestidade: o dado é ruidoso, então o acerto dia-a-dia é modesto. A mágica
        acha rápido o melhor candidato; o humano depois refina.</p>
    </div>
    <span class="pagenum">09</span>
  </section>

  <!-- 10 FECHO -->
  <section class="slide" id="s10">
    <div class="slide-inner">
      <div class="head"><span class="pill"></span><p class="ftitle">resumo do pitch</p></div>
      <div class="rule"></div>
      <ol class="pts">
        <li><b>O problema se vende sozinho.</b> Prever a onda com 4 semanas de antecedência
          significa leitos, oxigênio e vidas.</li>
        <li><b>Big data real.</b> 3,85 milhões de registros do DataSUS viram uma série diária
          limpa de São Paulo.</li>
        <li><b>LazyPredict é o atalho.</b> Uma linha, {lz['n_modelos_testados']} modelos testados,
          e o melhor deles competindo de igual com o SARIMA — <span class="em">sem matemática pesada</span>.</li>
      </ol>
      <div class="chips" style="margin-top:2.4rem"><span class="chip">Obrigado! · Perguntas?</span></div>
    </div>
    <span class="pagenum">10</span>
  </section>

</div>

<script>
(function(){{
  var deck=document.getElementById('deck');
  var slides=Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var dots=document.getElementById('dots');
  slides.forEach(function(s,i){{
    var a=document.createElement('a'); a.href='#'+s.id;
    a.setAttribute('aria-label','Slide '+(i+1)); dots.appendChild(a);
  }});
  var links=Array.prototype.slice.call(dots.children);
  var io=new IntersectionObserver(function(es){{
    es.forEach(function(e){{
      if(e.isIntersecting){{
        var i=slides.indexOf(e.target);
        links.forEach(function(l,j){{ l.classList.toggle('on', j===i); }});
      }}
    }});
  }}, {{threshold:.55}});
  slides.forEach(function(s){{ io.observe(s); }});
  function cur(){{
    var top=deck.scrollTop, best=0, d=1e9;
    slides.forEach(function(s,i){{ var dd=Math.abs(s.offsetTop-top); if(dd<d){{d=dd;best=i;}} }});
    return best;
  }}
  document.addEventListener('keydown',function(e){{
    if(e.key==='ArrowRight'||e.key==='ArrowDown'||e.key===' '||e.key==='PageDown'){{
      e.preventDefault(); var n=Math.min(slides.length-1,cur()+1);
      slides[n].scrollIntoView(); }}
    else if(e.key==='ArrowLeft'||e.key==='ArrowUp'||e.key==='PageUp'){{
      e.preventDefault(); var p=Math.max(0,cur()-1); slides[p].scrollIntoView(); }}
  }});
}})();
</script>
"""

SAIDA.write_text(HTML, encoding="utf-8")
kb = len(HTML.encode("utf-8")) / 1024
print(f">> {SAIDA.relative_to(RAIZ)} gerado ({kb:.0f} KB, imagens embutidas)")

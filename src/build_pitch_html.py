# -*- coding: utf-8 -*-
"""
Gera o deck em HTML (uma página, apresentável em tela cheia) com as figuras
embutidas em base64 — arquivo 100% autossuficiente.

É um deck de SÉRIES TEMPORAIS: além do LazyPredict (sugestão do professor), cobre
a análise clássica (decomposição, estacionariedade, ACF/PACF, Holt-Winters,
SARIMA). Os slides marcados com "ao vivo no Colab" são demonstrados no notebook
notebooks/predicao_curvas_epidemicas.ipynb.

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
    "dist": b64("slide_distribuicao.png"),
    "dow": b64("slide_dia_semana.png"),
    "decomp": b64("04_decomposicao.png"),
    "classicos": b64("10_arima_sarima_previsao.png"),
    "tabela": b64("lazy_00_tabela.png"),
    "split": b64("slide_treino_teste.png"),
    "rank": b64("lazy_01_leaderboard.png"),
    "comp": b64("slide_comparacao.png"),
}

lz = json.loads((DADOS / "lazy_resultados.json").read_text(encoding="utf-8"))
res = json.loads((DADOS / "resultados.json").read_text(encoding="utf-8"))
melhor = lz["melhor"]
ntab = lz["n_treino"] + lz["n_teste"]
N = 14

HTML = f"""<style>
:root {{
  --bg:#0a0a0a; --panel:#151515; --line:rgba(255,255,255,.09);
  --red:#C81E1E; --red-hi:#FF5C5C; --green:#43D17A; --purple:#9B7BE0;
  --ink:#ededed; --muted:#9a9a9a;
  --mono:ui-monospace,"Cascadia Code","Consolas","SFMono-Regular",monospace;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink); font-family:var(--sans);
       -webkit-font-smoothing:antialiased; }}
.deck {{ scroll-snap-type:y mandatory; height:100vh; overflow-y:auto; scroll-behavior:smooth; }}
@media (prefers-reduced-motion:reduce){{ .deck{{scroll-behavior:auto;}} }}

.slide {{ scroll-snap-align:start; min-height:100vh; padding:5vh 6.5vw 6.5vh;
         display:flex; flex-direction:column; justify-content:center;
         position:relative; border-bottom:1px solid var(--line); }}
.slide-inner {{ width:100%; max-width:1080px; margin:0 auto; }}

.eyebrow {{ font-family:var(--mono); font-size:.78rem; letter-spacing:.22em;
           text-transform:uppercase; color:var(--muted); margin:0 0 1.1rem; }}
.head {{ display:flex; align-items:center; gap:.7rem; margin:0 0 .3rem; }}
.pill {{ width:26px; height:12px; border-radius:6px; background:var(--red); flex:none; }}
.ftitle {{ font-family:var(--mono); font-weight:700; font-size:1.02rem;
          text-transform:lowercase; letter-spacing:.02em; color:#fff; margin:0; }}
.demo {{ margin-left:auto; font-family:var(--mono); font-size:.72rem; color:var(--green);
        border:1px solid rgba(67,209,122,.5); border-radius:999px; padding:.2rem .7rem;
        letter-spacing:.03em; white-space:nowrap; }}
.rule {{ height:2px; background:var(--red); border-radius:2px; margin:.5rem 0 1.4rem; width:100%; }}
h1.big {{ font-size:clamp(2.1rem,5vw,3.8rem); line-height:1.04; margin:.2rem 0 1rem;
         font-weight:800; letter-spacing:-.02em; text-wrap:balance; }}
h2.q {{ font-size:clamp(1.5rem,3.4vw,2.5rem); line-height:1.12; margin:.2rem 0 .9rem;
       font-weight:800; letter-spacing:-.015em; text-wrap:balance; }}
p.lead {{ font-size:clamp(1rem,1.55vw,1.28rem); line-height:1.5; color:#dcdcdc;
         max-width:64ch; margin:.2rem 0 .9rem; }}
.em {{ color:var(--red-hi); font-weight:700; }}
.good {{ color:var(--green); font-weight:700; }}
.pur {{ color:var(--purple); font-weight:700; }}
.muted {{ color:var(--muted); }}

.figcard {{ background:#fff; border:3px solid var(--red); border-radius:12px;
           padding:9px; margin:.2rem 0; box-shadow:0 16px 46px rgba(0,0,0,.45); }}
.figcard img {{ display:block; width:100%; height:auto; border-radius:4px; }}
.figdark {{ background:#0d0d0d; border:1px solid var(--line); border-radius:12px;
           padding:8px; margin:.2rem 0; box-shadow:0 16px 46px rgba(0,0,0,.45); }}
.figdark img {{ display:block; width:100%; height:auto; border-radius:6px; }}
.tall img {{ max-height:54vh; width:auto; max-width:100%; margin:0 auto; }}
.cap {{ font-size:.9rem; color:var(--muted); margin:.6rem 0 0; max-width:74ch; }}

.stats {{ display:flex; flex-wrap:wrap; gap:1.1rem 2.2rem; margin:.4rem 0 1.1rem; }}
.stat b {{ display:block; font-family:var(--mono); font-weight:700;
          font-size:clamp(1.6rem,3.6vw,2.7rem); color:#fff; line-height:1;
          font-variant-numeric:tabular-nums; }}
.stat span {{ font-size:.86rem; color:var(--muted); letter-spacing:.02em; }}
.stat .hl {{ color:var(--red-hi); }}

.chips {{ display:flex; flex-wrap:wrap; gap:.6rem; margin:1rem 0 0; }}
.chip {{ font-family:var(--mono); font-size:.86rem; color:#fff; padding:.45rem .85rem;
        border:1.5px solid var(--red); border-radius:999px; background:rgba(200,30,30,.12); }}

.steps {{ list-style:none; padding:0; margin:.3rem 0 0; display:flex; flex-direction:column; gap:.6rem; }}
.steps li {{ display:flex; gap:.8rem; align-items:baseline; font-size:clamp(.98rem,1.45vw,1.18rem); line-height:1.4; }}
.steps li b {{ color:#fff; }}
.steps .n {{ font-family:var(--mono); color:var(--red); font-weight:700; flex:none; }}

.codebox {{ font-family:var(--mono); font-size:clamp(.8rem,1.25vw,.98rem);
           background:#050505; border:1px solid var(--line); border-left:3px solid var(--red);
           border-radius:8px; padding:.9rem 1.1rem; margin:.4rem 0 .9rem; overflow-x:auto;
           color:#e8e8e8; line-height:1.65; }}
.codebox .k {{ color:var(--red-hi); }}
.codebox .c {{ color:var(--muted); }}

.tbl {{ width:100%; border-collapse:collapse; font-size:clamp(.9rem,1.3vw,1.05rem); margin:.3rem 0; }}
.tbl th, .tbl td {{ text-align:left; padding:.4rem .6rem; border-bottom:1px solid var(--line); }}
.tbl td.n {{ text-align:right; font-family:var(--mono); font-variant-numeric:tabular-nums; }}
.tbl .win td {{ color:var(--green); font-weight:700; }}

.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:2rem; align-items:center; }}
.grid2.wide {{ grid-template-columns:1.15fr .85fr; }}
@media (max-width:820px){{ .grid2,.grid2.wide{{grid-template-columns:1fr;}} }}

ol.pts {{ counter-reset:p; list-style:none; padding:0; margin:.4rem 0 0;
         display:flex; flex-direction:column; gap:.9rem; }}
ol.pts li {{ position:relative; padding-left:3rem; font-size:clamp(1rem,1.5vw,1.22rem);
            line-height:1.48; max-width:70ch; }}
ol.pts li::before {{ counter-increment:p; content:counter(p); position:absolute; left:0; top:-2px;
   font-family:var(--mono); font-weight:700; color:var(--red); font-size:1.45rem;
   border-bottom:2px solid var(--red); padding:0 .5rem .1rem; }}

.pagenum {{ position:absolute; right:2vw; bottom:2vh; font-family:var(--mono);
           font-size:.76rem; color:var(--muted); font-variant-numeric:tabular-nums; }}
.hint {{ font-family:var(--mono); font-size:.82rem; color:var(--muted); margin-top:2rem; }}
.hint b {{ color:var(--red-hi); }}
.author {{ font-family:var(--mono); font-size:.9rem; color:var(--muted); margin-top:1.4rem; }}
.author b {{ color:var(--ink); font-weight:700; }}

.dots {{ position:fixed; right:1vw; top:50%; transform:translateY(-50%); z-index:20;
        display:flex; flex-direction:column; gap:.45rem; }}
.dots a {{ width:8px; height:8px; border-radius:50%; background:#3a3a3a; display:block;
          transition:background .2s,transform .2s; }}
.dots a.on {{ background:var(--red); transform:scale(1.4); }}
:focus-visible {{ outline:2px solid var(--red-hi); outline-offset:3px; }}
</style>

<nav class="dots" id="dots" aria-label="Navegação dos slides"></nav>
<div class="deck" id="deck">

  <!-- 1 CAPA -->
  <section class="slide" id="s1"><div class="slide-inner">
    <p class="eyebrow">Seminário · Séries Temporais · UFPB</p>
    <h1 class="big">Predição de<br>curvas epidêmicas</h1>
    <p class="lead">COVID-19 em São Paulo: da análise clássica de séries temporais
      (<span class="good">decomposição, ACF/PACF, SARIMA</span>) à modelagem automática
      com <span class="em">LazyPredict</span> — tudo <span class="em">ao vivo no Colab</span>.</p>
    <div class="chips"><span class="chip">séries temporais</span><span class="chip">análise no Colab</span><span class="chip">LazyPredict</span></div>
    <p class="author"><b>Allan Vasconcelos</b> · UFPB · 2026</p>
    <p class="hint">use <b>←</b> <b>→</b> ou role a página para navegar</p>
  </div><span class="pagenum">01 / {N}</span></section>

  <!-- 2 O PROBLEMA -->
  <section class="slide" id="s2"><div class="slide-inner">
    <div class="head"><span class="pill"></span><p class="ftitle">o problema</p></div>
    <div class="rule"></div>
    <h2 class="q">Quantos casos teremos nas <span class="em">próximas 4 semanas</span>?</h2>
    <p class="lead">Essa resposta decide leitos de UTI, oxigênio, insumos e escala de
      equipes. Prever cedo é <span class="good">se preparar</span>; errar é hospital
      lotado — ou recurso caríssimo jogado fora.</p>
    <div class="chips"><span class="chip">UTI &amp; leitos</span><span class="chip">oxigênio &amp; insumos</span><span class="chip">escala de equipes</span><span class="chip">afrouxar / apertar</span></div>
  </div><span class="pagenum">02 / {N}</span></section>

  <!-- 3 A CURVA -->
  <section class="slide" id="s3"><div class="slide-inner">
    <div class="head"><span class="pill"></span><p class="ftitle">a curva que precisamos prever</p></div>
    <div class="rule"></div>
    <div class="stats">
      <div class="stat"><b class="hl">5,23 mi</b><span>casos confirmados</span></div>
      <div class="stat"><b>167 mil</b><span>óbitos</span></div>
      <div class="stat"><b class="hl">37.611</b><span>pico de casos em 1 dia</span></div>
    </div>
    <div class="figcard"><img src="{IMG['serie']}" alt="Casos e óbitos diários de COVID-19 em SP, 2020–2022"></div>
    <p class="cap">São Paulo, 2020–2022. Três ondas e um serrilhado semanal — difícil de prever no olho.</p>
  </div><span class="pagenum">03 / {N}</span></section>

  <!-- 4 OS DADOS -->
  <section class="slide" id="s4"><div class="slide-inner">
    <div class="head"><span class="pill"></span><p class="ftitle">os dados · escala big data</p></div>
    <div class="rule"></div>
    <h2 class="q"><span class="em">3,85 milhões</span> de registros brutos.</h2>
    <div class="stats">
      <div class="stat"><b>18</b><span>colunas</span></div>
      <div class="stat"><b>5.570</b><span>municípios do Brasil</span></div>
      <div class="stat"><b>92 MB</b><span>comprimido (.csv.gz)</span></div>
      <div class="stat"><b class="hl">762</b><span>dias após recortar SP</span></div>
    </div>
    <p class="lead">Fonte oficial <span class="em">DataSUS / Brasil.IO</span>, de 25/02/2020 a
      27/03/2022. A matéria-prima é grande; o desafio é <span class="good">tratá-la</span>
      até virar uma série diária utilizável.</p>
  </div><span class="pagenum">04 / {N}</span></section>

  <!-- 5 TRATAMENTO -->
  <section class="slide" id="s5"><div class="slide-inner">
    <div class="head"><span class="pill"></span><p class="ftitle">tratamento dos dados</p><span class="demo">▸ ao vivo no Colab</span></div>
    <div class="rule"></div>
    <ol class="steps">
      <li><span class="n">1</span><span>Ler só <b>6 de 18 colunas</b> — eficiência de memória com dado grande.</span></li>
      <li><span class="n">2</span><span>Filtrar o <b>nível estadual de SP</b> (já é a soma diária de todos os municípios).</span></li>
      <li><span class="n">3</span><span>Garantir <b>frequência diária contínua</b> (sem buracos no calendário).</span></li>
      <li><span class="n">4</span><span><b>Zerar valores negativos</b> das correções retroativas do governo.</span></li>
      <li><span class="n">5</span><span>Converter tipos e ordenar → <b>série diária de 762 dias</b>.</span></li>
    </ol>
    <p class="cap">Honestidade: para SP a série já vinha íntegra —
      <span class="good">0 datas faltando e 0 negativos</span>. As travas existem e deixam
      o código robusto para qualquer estado, mas nada precisou ser corrigido.</p>
  </div><span class="pagenum">05 / {N}</span></section>

  <!-- 6 DISTRIBUIÇÃO -->
  <section class="slide" id="s6"><div class="slide-inner">
    <div class="head"><span class="pill"></span><p class="ftitle">distribuição dos dados</p><span class="demo">▸ ao vivo no Colab</span></div>
    <div class="rule"></div>
    <div class="figdark"><img src="{IMG['dist']}" alt="Distribuição dos casos diários, escala real e log"></div>
    <p class="cap">A distribuição dos casos é <span class="em">muito assimétrica</span>
      (muitos dias baixos, poucos picos enormes). Em <span class="good">escala log</span> ela
      se equilibra — por isso modelamos em <span class="muted">log(1+casos)</span> para estabilizar a variância.</p>
  </div><span class="pagenum">06 / {N}</span></section>

  <!-- 7 SAZONALIDADE -->
  <section class="slide" id="s7"><div class="slide-inner">
    <div class="head"><span class="pill"></span><p class="ftitle">sazonalidade semanal · o dado é sujo</p><span class="demo">▸ ao vivo no Colab</span></div>
    <div class="rule"></div>
    <div class="grid2 wide">
      <div>
        <h2 class="q">Fim de semana quase não testa.</h2>
        <p class="lead">A curva <span class="em">serrilha toda semana</span>: domingo registra
          metade da média; quinta, quase 40% acima. Não é a epidemia — é o
          <span class="muted">cartório</span> (subnotificação), criando sazonalidade de <b>período 7</b>.</p>
        <div class="chips"><span class="chip">domingo ≈ 0,49×</span><span class="chip">quinta ≈ 1,38×</span></div>
      </div>
      <div class="figdark"><img src="{IMG['dow']}" alt="Distribuição de casos por dia da semana"></div>
    </div>
  </div><span class="pagenum">07 / {N}</span></section>

  <!-- 8 ANÁLISE DE SÉRIE TEMPORAL -->
  <section class="slide" id="s8"><div class="slide-inner">
    <div class="head"><span class="pill"></span><p class="ftitle">análise de série temporal</p><span class="demo">▸ ao vivo no Colab</span></div>
    <div class="rule"></div>
    <div class="grid2 wide">
      <div class="figcard tall"><img src="{IMG['decomp']}" alt="Decomposição da série em tendência, sazonalidade e resíduo"></div>
      <div>
        <p class="lead"><b>Decomposição:</b> a série (em log) = <span class="good">tendência</span>
          (as ondas) + <span class="em">sazonalidade semanal</span> + resíduo.</p>
        <p class="lead"><b>Estacionariedade (ADF/KPSS):</b> em nível os testes divergem; após
          <span class="em">1 diferença</span> a série estaciona → <span class="muted">d = 1</span>.</p>
        <p class="lead"><b>ACF/PACF:</b> picos em <span class="em">7, 14, 21</span> confirmam o
          ciclo semanal → pede um modelo <span class="good">SARIMA</span>.</p>
      </div>
    </div>
  </div><span class="pagenum">08 / {N}</span></section>

  <!-- 9 TREINO/TESTE -->
  <section class="slide" id="s9"><div class="slide-inner">
    <div class="head"><span class="pill"></span><p class="ftitle">treino + teste (no tempo)</p><span class="demo">▸ ao vivo no Colab</span></div>
    <div class="rule"></div>
    <div class="figdark"><img src="{IMG['split']}" alt="Separação treino e teste no tempo"></div>
    <p class="cap">Treino = tudo até <span class="good">31/10/2021</span> ({lz['n_treino']} dias);
      teste = os <span class="em">28 dias seguintes</span> (nov/2021), que o modelo nunca viu.
      O teste vem <span class="em">sempre depois</span> do treino — senão seria usar o futuro
      para prever o passado (vazamento). <b>Todos</b> os modelos usam esta mesma divisão.</p>
  </div><span class="pagenum">09 / {N}</span></section>

  <!-- 10 MODELOS CLÁSSICOS -->
  <section class="slide" id="s10"><div class="slide-inner">
    <div class="head"><span class="pill"></span><p class="ftitle">modelos clássicos de série temporal</p><span class="demo">▸ ao vivo no Colab</span></div>
    <div class="rule"></div>
    <div class="grid2 wide">
      <div class="figcard"><img src="{IMG['classicos']}" alt="Previsão de 28 dias: ARIMA plano vs SARIMA sazonal"></div>
      <div>
        <p class="lead"><b>Holt-Winters</b> e <b>SARIMA</b> aprendem o ciclo de 7 dias e
          reproduzem o zigue-zague; o <b>ARIMA</b> prevê quase uma <span class="em">linha plana</span>.</p>
        <table class="tbl">
          <tr><th>Modelo</th><th class="n">RMSE</th></tr>
          <tr class="win"><td>Holt-Winters</td><td class="n">498</td></tr>
          <tr><td>SARIMA</td><td class="n">567</td></tr>
          <tr><td>Naïve sazonal</td><td class="n">652</td></tr>
          <tr><td>ARIMA</td><td class="n">714</td></tr>
        </table>
        <p class="cap">A sazonalidade é o que mais reduz o erro.</p>
      </div>
    </div>
  </div><span class="pagenum">10 / {N}</span></section>

  <!-- 11 SÉRIE -> TABELA -->
  <section class="slide" id="s11"><div class="slide-inner">
    <div class="head"><span class="pill"></span><p class="ftitle">alternativa automática: série → tabela</p><span class="demo">▸ ao vivo no Colab</span></div>
    <div class="rule"></div>
    <p class="lead">E se a máquina escolhesse o modelo? Primeiro viramos a série numa
      <span class="em">tabela</span>: para prever <span class="good">hoje</span>, as pistas são o passado dela.</p>
    <div class="figdark"><img src="{IMG['tabela']}" alt="Série temporal transformada em tabela supervisionada"></div>
    <p class="cap">Pistas: ontem, 7 dias atrás, média da semana, dia da semana → casos de hoje.
      Vira <span class="em">{ntab} linhas × {lz['n_features']} pistas</span>. Sem “colar”: toda pista usa só o passado.</p>
  </div><span class="pagenum">11 / {N}</span></section>

  <!-- 12 LAZYPREDICT -->
  <section class="slide" id="s12"><div class="slide-inner">
    <div class="head"><span class="pill"></span><p class="ftitle">a mágica: LazyPredict</p><span class="demo">▸ ao vivo no Colab</span></div>
    <div class="rule"></div>
    <div class="codebox">
<span class="c"># ferramenta sugerida pelo professor:</span><br>
<span class="k">from</span> lazypredict.Supervised <span class="k">import</span> LazyRegressor<br>
modelos, _ = LazyRegressor().<span class="k">fit</span>(X_tr, X_te, y_tr, y_te)
    </div>
    <h2 class="q"><span class="em">{lz['n_modelos_testados']} modelos</span> treinados e ranqueados sozinhos, em segundos.</h2>
    <div class="figdark"><img src="{IMG['rank']}" alt="Ranking automático dos modelos pelo LazyPredict"></div>
  </div><span class="pagenum">12 / {N}</span></section>

  <!-- 13 COMPARAÇÃO -->
  <section class="slide" id="s13"><div class="slide-inner">
    <div class="head"><span class="pill"></span><p class="ftitle">comparação geral</p><span class="demo">▸ ao vivo no Colab</span></div>
    <div class="rule"></div>
    <div class="figdark"><img src="{IMG['comp']}" alt="Comparação de RMSE: modelos clássicos e LazyPredict"></div>
    <p class="cap">Na mesma janela: o <span class="good">Holt-Winters</span> (sazonal, feito à mão)
      vence; o <span class="pur">LazyPredict</span> ({melhor['modelo']}, {melhor['rmse']:.0f}) chega
      competitivo com <span class="em">uma linha</span>. <span class="muted">Nota: a avaliação do
      LazyPredict é um-passo-à-frente — tarefa mais fácil que os 28 dias “cegos” dos clássicos.</span></p>
  </div><span class="pagenum">13 / {N}</span></section>

  <!-- 14 CONCLUSÕES -->
  <section class="slide" id="s14"><div class="slide-inner">
    <div class="head"><span class="pill"></span><p class="ftitle">conclusões</p></div>
    <div class="rule"></div>
    <ol class="pts">
      <li><b>É um problema de série temporal.</b> Decomposição, ADF/KPSS e ACF/PACF
        revelaram a <span class="em">sazonalidade semanal (período 7)</span> da notificação.</li>
      <li><b>Quem capta a sazonalidade vence.</b> Holt-Winters e SARIMA batem folgado o
        ARIMA (linha plana) e o naïve.</li>
      <li><b>LazyPredict é o atalho.</b> Em uma linha, testou dezenas de modelos e chegou
        perto dos clássicos — ótimo para <span class="em">explorar rápido</span>. Automatizar acha
        o candidato; conhecer a série ainda dá o melhor resultado.</li>
    </ol>
    <div class="chips" style="margin-top:2rem"><span class="chip">Obrigado! · Perguntas?</span></div>
  </div><span class="pagenum">14 / {N}</span></section>

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
      e.preventDefault(); slides[Math.min(slides.length-1,cur()+1)].scrollIntoView(); }}
    else if(e.key==='ArrowLeft'||e.key==='ArrowUp'||e.key==='PageUp'){{
      e.preventDefault(); slides[Math.max(0,cur()-1)].scrollIntoView(); }}
  }});
}})();
</script>
"""

SAIDA.write_text(HTML, encoding="utf-8")
print(f">> {SAIDA.relative_to(RAIZ)} gerado ({len(HTML.encode('utf-8'))/1024:.0f} KB)")

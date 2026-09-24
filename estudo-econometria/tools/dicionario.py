# Gera parts/07c_dicionario.html a partir da lista E abaixo.
import os, html
OUT=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"parts","07c_dicionario.html")
# (grupo, nome, fórmula TeX, significado, unidade, onde, cuidado, palavras-chave)
E=[
(r"Estatística descritiva (Aula 2)",r"Somatório",r"\sum_{i=1}^{n}x_i=x_1+\dots+x_n",r"Soma de todos os valores.",r"A mesma de x.",r"Aula 2 (P1–P5)",r"\(\sum x_i^2\neq(\sum x_i)^2\) e \(\sum x_i/y_i\neq\sum x_i/\sum y_i\).",r"soma sigma"),
(r"Estatística descritiva (Aula 2)",r"Média amostral",r"\bar x=\frac1n\sum_{i=1}^{n}x_i",r"Centro da amostra.",r"A mesma de x.",r"Aulas 2 e 3",r"A reta de MQO sempre passa por \((\bar x,\bar y)\).",r"media barra"),
(r"Estatística descritiva (Aula 2)",r"Desvio em relação à média",r"x_i-\bar x,\qquad\sum_i(x_i-\bar x)=0",r"Quanto cada observação se afasta da média. A soma é sempre zero.",r"A mesma de x.",r"Aula 2 (P1)",r"Use a soma zero para conferir contas.",r"desvio"),
(r"Estatística descritiva (Aula 2)",r"Soma dos quadrados totais de x",r"SQT_x=\sum_i(x_i-\bar x)^2=\sum_ix_i^2-n\bar x^2",r"Variação total de x: quanta informação a amostra tem para estimar a inclinação.",r"Unidade de x ao quadrado.",r"Aulas 3 e 5",r"Não confunda com SQT (variação de <em>y</em>). Tem que ser &gt; 0 (RLS.3).",r"sqtx variacao"),
(r"Estatística descritiva (Aula 2)",r"Variância amostral",r"s_x^2=\widehat{Var}(x)=\frac{\sum_i(x_i-\bar x)^2}{n-1}",r"Dispersão média ao quadrado em torno da média.",r"Unidade de x ao quadrado.",r"Aula 2; Lista 1 Q6; Lista 2 Ex. 1 e 2",r"Variância = desvio-padrão ao quadrado.",r"variancia"),
(r"Estatística descritiva (Aula 2)",r"Desvio-padrão amostral",r"s_x=\sqrt{s_x^2}",r"Quanto a variável tipicamente se afasta da média.",r"A mesma de x.",r"Aula 2; Lista 2 Ex. 1",r"Na Lista 2 Ex. 1, \(s=10\Rightarrow Var=100\).",r"desvio padrao dp"),
(r"Estatística descritiva (Aula 2)",r"Covariância amostral",r"\widehat{Cov}(x,y)=\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}{n-1}=\frac{\sum_ix_iy_i-n\bar x\bar y}{n-1}",r"Se x e y andam juntos (+) ou em sentidos opostos (−).",r"Unidade de x vezes unidade de y.",r"Aula 2; Lista 2 Ex. 1 e 2",r"Depende das unidades; o sinal é o que importa para a direção.",r"covariancia"),
(r"Estatística descritiva (Aula 2)",r"Correlação",r"Corr(x,y)=\frac{Cov(x,y)}{s_x\,s_y}\ \Rightarrow\ Cov=Corr\cdot s_x\cdot s_y",r"Associação linear padronizada.",r"Sem unidade (entre −1 e 1).",r"Aula 2; Lista 2 Ex. 1",r"Correlação zero não é independência (\(Y=X^2\)).",r"correlacao"),
(r"Probabilidade (Aula 2)",r"Esperança",r"E[X]=\sum_xx\,p(x)\quad\text{ou}\quad E[X]=\int x\,f(x)\,dx",r"Média teórica (populacional), ponderada pelas probabilidades.",r"A mesma de X.",r"Aula 2",r"Não precisa ser um valor possível (dado: 3,5).",r"esperanca media populacional"),
(r"Probabilidade (Aula 2)",r"Linearidade da esperança",r"E[aX+bY+c]=aE[X]+bE[Y]+c",r"A esperança passa por somas e constantes.",r"A mesma de X.",r"Aula 2; Lista 1 Q24",r"",r""),
(r"Probabilidade (Aula 2)",r"Variância",r"Var(X)=E[(X-E[X])^2]=E[X^2]-(E[X])^2",r"Dispersão teórica em torno da média.",r"Unidade de X ao quadrado.",r"Aula 2",r"Desvio-padrão = raiz da variância.",r"variancia populacional"),
(r"Probabilidade (Aula 2)",r"Variância de transformações",r"Var(a+bX)=b^2Var(X),\qquad Var(aX+bY+c)=a^2Var(X)+b^2Var(Y)+2ab\,Cov(X,Y)",r"Constante somada não espalha; fator multiplicativo entra ao quadrado.",r"Unidade ao quadrado.",r"Aula 2; Lista 1 Q19 e Q24",r"Esquecer o termo \(2ab\,Cov\).",r"variancia combinacao linear"),
(r"Probabilidade (Aula 2)",r"Covariância (definição e regras)",r"Cov(X,Y)=E[XY]-E[X]E[Y],\qquad Cov(aX+c,bY+d)=ab\,Cov(X,Y)",r"Associação linear teórica; bilinear.",r"Unidade de X vezes unidade de Y.",r"Aula 2; Lista 1 Q22, Q24, Q28",r"Somar constantes não muda covariância nem correlação.",r"covariancia"),
(r"Probabilidade (Aula 2)",r"Bernoulli",r"E[D]=\pi,\qquad Var(D)=\pi(1-\pi)",r"Variável 0/1: a média é uma proporção.",r"Sem unidade (proporção).",r"Aula 2; Lista 1 Q17 e Q27",r"Variância máxima em π = 0,5.",r"binaria dummy proporcao"),
(r"Probabilidade (Aula 2)",r"Probabilidade condicional e Bayes",r"p(y\mid x)=\frac{p(x,y)}{p(x)},\qquad p(y\mid x)=\frac{p(x\mid y)\,p(y)}{p(x)}",r"Distribuição de Y dentro do grupo X = x.",r"Probabilidade (sem unidade).",r"Aula 2",r"Independência: \(p(y\mid x)=p(y)\).",r"condicional bayes"),
(r"Probabilidade (Aula 2)",r"Lei das Expectativas Iteradas",r"E[Y]=E\big[E[Y\mid X]\big]",r"A média geral é a média das médias dos grupos, ponderada pelo tamanho de cada grupo.",r"A mesma de Y.",r"Aulas 2 e 5; Lista 1 Q23 e Q25",r"É usada na prova de não viés da Aula 5.",r"lei expectativas iteradas lei"),
(r"Probabilidade (Aula 2)",r"Decomposição da variância",r"Var(Y)=E[Var(Y\mid X)]+Var[E(Y\mid X)]",r"Variação dentro dos grupos + variação entre as médias dos grupos.",r"Unidade de Y ao quadrado.",r"Lista 1 Q30",r"",r""),
(r"Probabilidade (Aula 2)",r"Média amostral como estimador",r"E[\hat\mu]=\mu,\qquad Var(\hat\mu)=\frac{\sigma^2}{N},\qquad ep=\frac{\sigma}{\sqrt N}",r"Não viesada; fica mais precisa com N maior.",r"\(\hat\mu\) e ep na unidade de Y; Var na unidade ao quadrado.",r"Aula 2; Lista 1 Q26",r"Quadruplicar N corta o ep pela metade.",r"media amostral"),
(r"Probabilidade (Aula 2)",r"Estatística z e t da média",r"Z=\frac{\hat\mu-\mu_0}{\sigma/\sqrt N},\qquad T=\frac{\hat\mu-\mu_0}{S/\sqrt N}\sim t_{N-1}",r"Distância até \(\mu_0\) em unidades de erro-padrão.",r"Sem unidade.",r"Aula 2",r"|Z| &gt; 1,96 rejeita a 5%.",r"teste z t"),
(r"Probabilidade (Aula 2)",r"Viés e erro quadrático médio",r"Vi\acute es=E[\hat\theta]-\theta,\qquad EQM=Var(\hat\theta)+Vi\acute es^2",r"Viés: erro do centro. EQM: erro total médio.",r"Viés na unidade do parâmetro; EQM ao quadrado.",r"Lista 1 Q8; Aula 5",r"",r""),
(r"Regressão simples (Aula 3)",r"Modelo populacional",r"Y=\beta_0+\beta_1X+U",r"Y = parte sistemática + erro (outros fatores).",r"\(\beta_0\) e U na unidade de Y; \(\beta_1\) em unid. Y / unid. X.",r"Aula 3; RLS.1",r"U não é simples ruído: tem conteúdo econômico.",r"modelo"),
(r"Regressão simples (Aula 3)",r"Média condicional zero e FRP",r"E[U\mid X]=0\ \Rightarrow\ E[Y\mid X]=\beta_0+\beta_1X",r"Os fatores omitidos não se relacionam, em média, com X.",r"—",r"Aulas 3 e 5 (RLS.4)",r"Não implica homocedasticidade nem independência.",r"frp media condicional zero"),
(r"Regressão simples (Aula 3)",r"Inclinação do MQO",r"\hat\beta_1=\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}{\sum_i(x_i-\bar x)^2}=\frac{\widehat{Cov}(x,y)}{\widehat{Var}(x)}",r"Variação média de ŷ por unidade a mais de x (associação).",r"Unidade de y por unidade de x (ex.: R$ por m²).",r"Aula 3; Listas 1 e 2 ★",r"Calcule antes de \(\hat\beta_0\). Divisor n ou n − 1 cancela se for o mesmo.",r"beta1 inclinacao mqo formula"),
(r"Regressão simples (Aula 3)",r"Inclinação: outras formas",r"\hat\beta_1=\frac{\sum x_iy_i-n\bar x\bar y}{\sum x_i^2-n\bar x^2}=Corr(x,y)\,\frac{s_y}{s_x}",r"As mesmas contas a partir de somas brutas ou de correlação e desvios-padrão.",r"Unidade de y por unidade de x.",r"Lista 2 Ex. 1 e 2",r"",r""),
(r"Regressão simples (Aula 3)",r"Intercepto do MQO",r"\hat\beta_0=\bar y-\hat\beta_1\bar x",r"Altura da reta em x = 0; garante que a reta passe por \((\bar x,\bar y)\).",r"Unidade de y.",r"Aula 3; Listas 1 e 2 ★",r"Só tem leitura econômica se x = 0 fizer sentido.",r"beta0 intercepto formula"),
(r"Regressão simples (Aula 3)",r"Valor ajustado e resíduo",r"\hat y_i=\hat\beta_0+\hat\beta_1x_i,\qquad \hat u_i=y_i-\hat y_i",r"Valor da reta para a observação i; distância do observado até a reta.",r"Unidade de y.",r"Aula 3; Lista 2",r"Resíduo = observado − ajustado. Resíduo ≠ erro.",r"residuo ajustado"),
(r"Regressão simples (Aula 3)",r"Propriedades algébricas",r"\sum_i\hat u_i=0,\qquad\sum_ix_i\hat u_i=0,\qquad\bar{\hat y}=\bar y",r"Saem das CPOs; valem em qualquer amostra.",r"—",r"Aula 3; Lista 1 Q33, Q37, Q41",r"Ortogonalidade não é exogeneidade.",r"propriedades cpo"),
(r"Regressão simples (Aula 3)",r"SQT, SQE e SQR",r"SQT=\sum(y_i-\bar y)^2,\quad SQE=\sum(\hat y_i-\bar y)^2,\quad SQR=\sum\hat u_i^2,\quad SQT=SQE+SQR",r"Variação total = sinal capturado pela reta + ruído residual.",r"Unidade de y ao quadrado.",r"Aula 3; Lista 2 Ex. 3",r"O termo cruzado some pela ortogonalidade.",r"sqt sqe sqr"),
(r"Regressão simples (Aula 3)",r"Coeficiente de determinação",r"R^2=\frac{SQE}{SQT}=1-\frac{SQR}{SQT}",r"Fração da variação amostral de y contabilizada pela reta.",r"Sem unidade (0 a 1 com intercepto).",r"Aula 3; Listas 1 e 2",r"Não mede causalidade; não se compara Y com ln Y; não muda com unidades.",r"r2 r quadrado ajuste"),
(r"Regressão simples (Aula 3)",r"Variância do erro estimada",r"\hat\sigma^2=\frac{SQR}{n-2},\qquad\hat\sigma=\sqrt{\hat\sigma^2}",r"Dispersão dos pontos em torno da reta (não viesada sob RLS.1–5).",r"\(\hat\sigma^2\) em unidade de y ao quadrado; \(\hat\sigma\) em unidade de y.",r"Aulas 3 e 5; Lista 02 Q4",r"n − 2 porque estimamos 2 parâmetros (pela origem: n − 1).",r"sigma chapeu variancia erro"),
(r"Regressão simples (Aula 3)",r"Inclinação como soma ponderada",r"\hat\beta_1=\sum_iw_iy_i,\quad w_i=\frac{x_i-\bar x}{SQT_x},\quad\sum w_i=0,\ \sum w_ix_i=1",r"Cada y entra com peso que depende só de x.",r"\(w_i\) em 1/unidade de x.",r"Prática Aula 3; Aula 5",r"",r""),
(r"Unidades e forma funcional (Aula 4)",r"Mudança de escala",r"\tilde y=by,\ \tilde x=cx\ \Rightarrow\ \tilde\beta_1=\frac bc\hat\beta_1,\quad\tilde\beta_0=b\hat\beta_0",r"Trocar unidades muda os números, não a relação.",r"—",r"Aula 4; Lista 1 Q42 e Q44",r"\(R^2\) igual; escalar só x não muda \(\hat\beta_0\).",r"escala unidade"),
(r"Unidades e forma funcional (Aula 4)",r"Transformação afim",r"\tilde y=a+by,\ \tilde x=d+cx\ \Rightarrow\ \tilde\beta_1=\frac bc\hat\beta_1,\quad\tilde\beta_0=a+b\hat\beta_0-\frac bc\hat\beta_1d",r"Escala muda inclinação; deslocamentos de origem mudam só o intercepto.",r"—",r"Aula 4; Lista 1 Q51 e Q59",r"Celsius → Fahrenheit é afim.",r"afim"),
(r"Unidades e forma funcional (Aula 4)",r"Log e variação percentual",r"\Delta\ln x\approx\frac{\Delta x}{x},\qquad\Delta\ln x=\ln(1+g)",r"Diferença de logs ≈ variação proporcional.",r"Sem unidade (proporção; × 100 = %).",r"Aula 4",r"Boa só para variações pequenas.",r"log percentual"),
(r"Unidades e forma funcional (Aula 4)",r"Log–nível",r"\ln y=\beta_0+\beta_1x:\quad\%\Delta y\approx100\beta_1\Delta x,\quad\text{exato }100(e^{\beta_1\Delta x}-1)\%",r"+1 em x ⇒ cerca de \(100\beta_1\)% em y.",r"\(\beta_1\) em proporção por unidade de x.",r"Aula 4; Lista 1 Q52 e Q60",r"A aproximação subestima para Δ grandes.",r"log nivel semielasticidade"),
(r"Unidades e forma funcional (Aula 4)",r"Nível–log",r"y=\beta_0+\beta_1\ln x:\quad\frac{dy}{dx}=\frac{\beta_1}{x},\quad+1\%\text{ em }x\Rightarrow\Delta y\approx\frac{\beta_1}{100}",r"+1% em x ⇒ cerca de \(\beta_1/100\) unidades em y.",r"\(\beta_1\) na unidade de y.",r"Aula 4; Lista 1 Q53",r"Exato: \(\beta_1\ln(1+g)\).",r"nivel log"),
(r"Unidades e forma funcional (Aula 4)",r"Log–log (elasticidade)",r"\ln y=\beta_0+\beta_1\ln x:\quad\beta_1=\frac{d\ln y}{d\ln x},\quad\text{exato }100[(1+g)^{\beta_1}-1]\%",r"+1% em x ⇒ cerca de \(\beta_1\)% em y.",r"Sem unidade (elasticidade).",r"Aula 4; Lista 1 Q54",r"A aproximação superestima no exemplo 0,45.",r"log log elasticidade"),
(r"Unidades e forma funcional (Aula 4)",r"Quadrático",r"\frac{\partial E(Y\mid X)}{\partial X}=\beta_1+2\beta_2X,\qquad X^*=-\frac{\beta_1}{2\beta_2}",r"Efeito marginal que muda com X; ponto de retorno.",r"Efeito em unid. y / unid. x; \(X^*\) em unidade de x.",r"Aula 4; Lista 2 Ex. 4 ★; Lista 1 Q55",r"\(\beta_2&lt;0\) côncava (máximo); \(\beta_1\) é o efeito em X = 0.",r"quadratico efeito marginal ponto retorno"),
(r"Unidades e forma funcional (Aula 4)",r"Interação",r"\frac{\partial E(Y\mid X_1,X_2)}{\partial X_1}=\beta_1+\beta_3X_2",r"O efeito de \(X_1\) depende de \(X_2\).",r"Unid. y / unid. \(X_1\).",r"Aula 4; Lista 1 Q56",r"Mantenha \(X_1\) e \(X_2\) no modelo.",r"interacao"),
(r"Unidades e forma funcional (Aula 4)",r"Retransformação do log",r"E[Y\mid X]\neq\exp(E[\ln Y\mid X]);\quad\text{erros normais: }E[Y\mid X=x]=e^{\beta_0+\beta_1x+\sigma^2/2}",r"Exponenciar a previsão em log não dá a média de Y.",r"Unidade de y.",r"Aula 4 (apêndice)",r"",r""),
(r"Propriedades do MQO (Aula 5)",r"Equação-chave",r"\hat\beta_1=\beta_1+\frac{1}{SQT_x}\sum_id_iu_i,\qquad d_i=x_i-\bar x",r"Estimativa = parâmetro + erro de estimação (combinação dos erros).",r"Unid. y / unid. x.",r"Aula 5 ★",r"Base de todas as provas da aula.",r"equacao chave"),
(r"Propriedades do MQO (Aula 5)",r"Ausência de viés",r"E(\hat\beta_1)=\beta_1,\quad E(\hat\beta_0)=\beta_0\quad\text{(RLS.1–RLS.4)}",r"O centro da distribuição amostral é o parâmetro.",r"—",r"Aula 5 ★; Lista 02 Q1",r"Não diz que cada estimativa está perto; RLS.5 não é usada.",r"nao viesado vies"),
(r"Propriedades do MQO (Aula 5)",r"Variância da inclinação",r"Var(\hat\beta_1\mid X)=\frac{\sigma^2}{SQT_x}\quad\text{(RLS.1–RLS.5)}",r"Precisão: cai com mais variação em x, sobe com mais ruído.",r"(Unid. y / unid. x) ao quadrado.",r"Aula 5 ★; Lista 02 Q4 e Q10",r"Precisa de RLS.2 e RLS.5.",r"variancia beta1 precisao"),
(r"Propriedades do MQO (Aula 5)",r"Variância do intercepto",r"Var(\hat\beta_0\mid X)=\frac{\sigma^2\,\frac1n\sum_ix_i^2}{SQT_x}",r"Precisão do intercepto.",r"Unidade de y ao quadrado.",r"Aula 5 (exercício)",r"",r""),
(r"Propriedades do MQO (Aula 5)",r"Não viés de σ̂²",r"E\Big[\sum_i\hat u_i^2\Big]=(n-2)\sigma^2\ \Rightarrow\ E\left[\frac{SQR}{n-2}\right]=\sigma^2",r"Por que dividir por n − 2.",r"Unidade de y ao quadrado.",r"Aula 5 (apêndice)",r"Os 3 termos: (n−1)σ² − 2σ² + σ².",r"sigma n-2"),
(r"Propriedades do MQO (Aula 5)",r"Erros-padrão",r"ep(\hat\beta_1)=\frac{\hat\sigma}{\sqrt{SQT_x}},\qquad ep(\hat\beta_0)=\frac{\hat\sigma\sqrt{\sum x_i^2}}{\sqrt{n\,SQT_x}}",r"Estimativas do desvio-padrão dos estimadores.",r"A mesma do coeficiente correspondente.",r"Aulas 5 e 6; Lista 02",r"ep = raiz da variância estimada.",r"erro padrao ep"),
(r"Propriedades do MQO (Aula 5)",r"Consistência",r"\text{plim}\,\hat\beta_1=\beta_1+\frac{Cov(X,U)}{Var(X)}",r"Para onde o estimador vai com n muito grande.",r"Unid. y / unid. x.",r"Aula 5",r"Consistente se Cov(X, U) = 0.",r"consistencia plim"),
(r"Propriedades do MQO (Aula 5)",r"Viés de variável omitida (prática)",r"Y=2+0{,}8X+1{,}2Z+\varepsilon,\ Z=0{,}7X+v\ \Rightarrow\ E(\hat\alpha_1)=0{,}8+1{,}2\times0{,}7=1{,}64",r"A regressão curta atribui a X o efeito que passa por Z.",r"Unid. y / unid. x.",r"Prática 4–5",r"n maior não corrige.",r"variavel omitida vies"),
(r"Propriedades do MQO (Aula 5)",r"Viés de atenuação",r"\text{plim}\,\hat\beta_1=\beta_1\frac{Var(X^*)}{Var(X^*)+Var(r)}",r"Erro de medida clássico em X empurra a inclinação para zero.",r"Unid. y / unid. x.",r"Prática 4–5",r"",r""),
(r"Inferência (Aula 6)",r"Estatística t",r"t=\frac{\hat\beta_1-\beta_{1,0}}{ep(\hat\beta_1)}\sim t_{n-2}",r"Distância até \(H_0\) em erros-padrão.",r"Sem unidade.",r"Aula 6 ★; Lista 02",r"Nunca “aceitar” \(H_0\).",r"t teste hipotese"),
(r"Inferência (Aula 6)",r"Intervalo de confiança",r"IC=\hat\beta_1\pm t_{\alpha/2,\,n-2}\cdot ep(\hat\beta_1)",r"Valores de \(\beta_1\) compatíveis com os dados.",r"A mesma de \(\beta_1\).",r"Aula 6; Lista 02 Q7 e Q10",r"0 fora do IC ⇔ rejeita \(H_0:\beta_1=0\).",r"intervalo confianca ic"),
(r"Inferência (Aula 6)",r"p-valor",r"p=P(\text{estatística tão ou mais extrema}\mid H_0)",r"Compatibilidade dos dados com \(H_0\).",r"Probabilidade (0 a 1).",r"Aulas 2 e 6; Lista 02 Q2 e Q5",r"Não é a probabilidade de \(H_0\) ser verdadeira.",r"p valor"),
(r"Inferência (Aula 6)",r"Erros tipo I e II e poder",r"P(\text{tipo I})=\alpha,\quad P(\text{tipo II})=\beta,\quad\text{poder}=1-\beta",r"Rejeitar H₀ verdadeira; não rejeitar H₀ falsa; detectar um efeito que existe.",r"Probabilidades.",r"Aula 6; Lista 02 Q8",r"",r""),
(r"Inferência (Aula 6)",r"Erro-padrão robusto (HC0)",r"\widehat{Var}_{HC0}(\hat\beta_1)=\frac{\sum_i(x_i-\bar x)^2\hat u_i^2}{SQT_x^2}",r"Variância válida sob heterocedasticidade.",r"(Unid. y / unid. x) ao quadrado.",r"Aula 6; Lista 02 Q9",r"Pode ser maior ou menor; é assintótico.",r"robusto hc0 heterocedasticidade"),
(r"Inferência (Aula 6)",r"Origem da distribuição t",r"Z=\frac{\hat\beta_1-\beta_1}{\sigma/\sqrt{SQT_x}}\sim N(0,1),\quad\frac{(n-2)\hat\sigma^2}{\sigma^2}\sim\chi^2_{n-2},\quad t_{n-2}=\frac{Z}{\sqrt{\chi^2_{n-2}/(n-2)}}",r"Trocar σ por \(\hat\sigma\) gera caudas mais gordas.",r"Sem unidade.",r"Aula 6 (apêndice; RLS.6)",r"",r""),
(r"Inferência (Aula 6)",r"Breusch–Pagan",r"\hat u_i^2=\delta_0+\delta_1X_i+v_i,\qquad LM=nR^2_{aux}\xrightarrow{d}\chi^2_1",r"Testa se a variância muda com X.",r"Sem unidade.",r"Aula 6 (apêndice)",r"Não rejeitar não prova homocedasticidade.",r"breusch pagan"),
(r"Dummies e origem (Aula 7)",r"Regressão com uma dummy",r"\hat\beta_0=\bar y_0,\qquad\hat\beta_1=\bar y_1-\bar y_0",r"Média da referência e diferença de médias.",r"Unidade de y.",r"Aula 7",r"Diferença observada não é causal por si só.",r"dummy diferenca medias"),
(r"Dummies e origem (Aula 7)",r"Precisão da diferença",r"Var(\hat\beta_1\mid D)=\sigma^2\left(\frac1{n_1}+\frac1{n_0}\right)",r"Grupos desbalanceados reduzem a precisão.",r"Unidade de y ao quadrado.",r"Aula 7",r"",r""),
(r"Dummies e origem (Aula 7)",r"Dummy em log",r"100[\exp(\beta_1)-1]\%",r"Diferença percentual entre grupos.",r"Percentual.",r"Aula 7",r"\(100\beta_1\)% só para \(\beta_1\) pequeno.",r"dummy log"),
(r"Dummies e origem (Aula 7)",r"Regressão pela origem",r"\hat\beta_1=\frac{\sum x_iy_i}{\sum x_i^2},\quad Var=\frac{\sigma^2}{\sum x_i^2},\quad Vi\acute es=\beta_0\frac{\sum x_i}{\sum x_i^2},\quad\hat\sigma^2=\frac{SQR}{n-1}",r"Reta forçada a passar por (0, 0).",r"Unid. y / unid. x.",r"Aula 7",r"Se \(\beta_0\neq0\), fica viesado; \(\sum\hat u_i\neq0\) em geral.",r"origem"),
(r"Matemática de apoio",r"Derivadas básicas",r"(x^n)'=nx^{n-1},\quad(e^x)'=e^x,\quad(\ln x)'=\frac1x,\quad[f(g(x))]'=f'(g(x))\,g'(x)",r"Inclinação da curva num ponto (efeito marginal).",r"Unid. y / unid. x.",r"Módulo Derivadas; lousa",r"Constante deriva em zero.",r"derivada regra"),
(r"Matemática de apoio",r"Logaritmo",r"\ln(ab)=\ln a+\ln b,\quad\ln(a/b)=\ln a-\ln b,\quad\ln a^b=b\ln a",r"O log transforma produto em soma e potência em produto.",r"—",r"Módulo Log",r"\(\ln(a+b)\neq\ln a+\ln b\); só para valores &gt; 0.",r"log propriedades"),
(r"Matemática de apoio",r"Integral definida",r"\int_a^bf(x)\,dx=F(b)-F(a),\quad F'=f",r"Área sob a curva; na densidade, uma probabilidade.",r"Unid. f × unid. x.",r"Módulo Integrais; Aula 2",r"",r""),
(r"Matemática de apoio",r"Lagrangiano",r"\mathcal L=f(x,y)-\lambda[g(x,y)-c],\qquad\lambda=\frac{df^*}{dc}",r"Otimização com restrição; λ = preço sombra.",r"Unid. f / unid. c.",r"Módulo λ (fora do material)",r"",r""),
]
groups=[]
for g in E:
    if g[0] not in groups: groups.append(g[0])
out=[]
out.append('''
<!-- ================= DICIONÁRIO DE FÓRMULAS ================= -->
<section class="mod" id="dicionario" data-title="Dicionário">
  <div class="eyebrow">Revisão · todas as fórmulas do curso</div>
  <h2>Dicionário de fórmulas e unidades</h2>
  <p>Cada fórmula do curso com o que ela significa em palavras, a sua <strong>unidade de medida</strong>, onde aparece e o erro mais comum. Digite no campo abaixo para filtrar (ex.: “variância”, “log”, “R2”, “Lista 2”).</p>
  <div class="field"><label for="dictSearch">Buscar fórmula</label><input id="dictSearch" type="search" autocomplete="off" placeholder="ex.: erro padrão, elasticidade, Bayes"></div>
  <p class="small muted" id="dictCount"></p>

  <h3>Como pensar em unidades (análise dimensional)</h3>
  <p>Toda fórmula carrega unidades. Conferir a unidade do resultado é uma forma rápida de achar erros. Exemplo com a Lista 2, Ex. 1 (área em m², aluguel em R$):</p>
  <div class="tbl"><table>
    <thead><tr><th>Grandeza</th><th class="r">Valor</th><th>Unidade</th><th>Por quê</th></tr></thead>
    <tbody>
      <tr><td>\\(\\overline{area}\\), \\(s_{area}\\)</td><td class="r">60; 10</td><td>m²</td><td>Média e desvio-padrão têm a unidade da variável</td></tr>
      <tr><td>\\(Var(area)\\)</td><td class="r">100</td><td>(m²)²</td><td>Desvio ao quadrado</td></tr>
      <tr><td>\\(\\overline{aluguel}\\), \\(s_{aluguel}\\)</td><td class="r">2.000; 300</td><td>R$</td><td>—</td></tr>
      <tr><td>\\(Cov(area,aluguel)\\)</td><td class="r">2.400</td><td>m² · R$</td><td>Produto de um desvio de área por um desvio de aluguel</td></tr>
      <tr><td>\\(Corr\\)</td><td class="r">0,80</td><td>sem unidade</td><td>Cov ÷ (\\(s_x s_y\\)): m²·R$ ÷ (m²·R$)</td></tr>
      <tr><td>\\(\\hat\\beta_1=Cov/Var\\)</td><td class="r">24</td><td>R$ por m²</td><td>(m²·R$) ÷ (m²)² = R$/m²</td></tr>
      <tr><td>\\(\\hat\\beta_0\\), \\(\\hat y\\), \\(\\hat u\\)</td><td class="r">560; 2.240; 60</td><td>R$</td><td>Mesma unidade de y</td></tr>
    </tbody>
  </table></div>
  <p>E com os 5 indivíduos da Aula 3 (anos de estudo × R$/hora):</p>
  <div class="tbl"><table>
    <thead><tr><th>Grandeza</th><th class="r">Valor</th><th>Unidade</th></tr></thead>
    <tbody>
      <tr><td>\\(SQT_x\\)</td><td class="r">40</td><td>anos²</td></tr>
      <tr><td>\\(\\hat\\beta_1\\)</td><td class="r">1,15</td><td>(R$/hora) por ano de estudo</td></tr>
      <tr><td>SQR, \\(\\hat\\sigma^2\\)</td><td class="r">4,30; 1,433</td><td>(R$/hora)²</td></tr>
      <tr><td>\\(\\hat\\sigma\\)</td><td class="r">1,197</td><td>R$/hora</td></tr>
      <tr><td>\\(\\widehat{Var}(\\hat\\beta_1)\\)</td><td class="r">0,0358</td><td>[(R$/hora) por ano]²</td></tr>
      <tr><td>\\(ep(\\hat\\beta_1)\\)</td><td class="r">0,189</td><td>(R$/hora) por ano, a mesma de \\(\\hat\\beta_1\\)</td></tr>
      <tr><td>t, \\(R^2\\)</td><td class="r">6,08; 0,925</td><td>sem unidade</td></tr>
    </tbody>
  </table></div>
  <div class="box def"><span class="lbl">Por que as regras de escala da Aula 4 funcionam</span>
    <p>\\(\\hat\\beta_1\\) tem unidade “y por x”. Se y passa de reais para milhares de reais, o mesmo efeito vira um número 1.000 vezes menor. Se x passa de anos para meses, “por mês” é 12 vezes menor que “por ano”. \\(R^2\\), t e elasticidades não têm unidade, então não mudam.</p>
  </div>
''')
for gname in groups:
    out.append(f'  <h3 class="dgroup">{gname}</h3>\n  <div class="dgrid">')
    for (g,name,tex,mean,unit,where,care,kw) in E:
        if g!=gname: continue
        s=html.escape((name+" "+kw+" "+where+" "+mean).lower(),quote=True)
        out.append(f'''    <div class="fentry" data-s="{s}">
      <div class="fh"><b>{name}</b><span class="src">{where}</span></div>
      <div class="mathblock">\\[{tex}\\]</div>
      <div class="fl"><span>Significa</span>{mean}</div>
      <div class="fl"><span>Unidade</span>{unit}</div>''' + (f'''
      <div class="fl warn"><span>Cuidado</span>{care}</div>''' if care else "") + '''
    </div>''')
    out.append('  </div>')
out.append('''  <h3>Cartões de revisão (unidades, hipóteses, conceitos)</h3>
  <div class="flash-grid">
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Unidade</small>Unidade de \\(\\hat\\beta_1\\)</div><div class="face back">Unidade de y por unidade de x (ex.: R$ por m²)</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Unidade</small>Unidade de \\(\\hat\\beta_0\\)</div><div class="face back">A mesma de y</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Unidade</small>Unidade da variância</div><div class="face back">Unidade da variável ao quadrado</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Unidade</small>Unidade da covariância</div><div class="face back">Unidade de x vezes unidade de y</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Unidade</small>Correlação, \\(R^2\\), t, elasticidade</div><div class="face back">Sem unidade</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Unidade</small>SQT, SQE, SQR e \\(\\hat\\sigma^2\\)</div><div class="face back">Unidade de y ao quadrado</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Unidade</small>\\(ep(\\hat\\beta_1)\\)</div><div class="face back">A mesma de \\(\\hat\\beta_1\\) (y por x)</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Unidade</small>Coeficiente do log–nível</div><div class="face back">Proporção por unidade de x (× 100 = %)</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Aula 5</small>RLS.1</div><div class="face back">Linearidade nos parâmetros: \\(y_i=\\beta_0+\\beta_1x_i+u_i\\)</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Aula 5</small>RLS.2</div><div class="face back">Amostragem aleatória (pares iid)</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Aula 5</small>RLS.3</div><div class="face back">Variação em x: \\(SQT_x&gt;0\\)</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Aula 5</small>RLS.4</div><div class="face back">Média condicional zero: \\(E[u\\mid x]=0\\). Sustenta o não viés</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Aula 5</small>RLS.5</div><div class="face back">Homocedasticidade: \\(Var(u\\mid x)=\\sigma^2\\). Dá a fórmula da variância e o BLUE</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Aula 6</small>RLS.6</div><div class="face back">\\(u\\mid X\\sim N(0,\\sigma^2)\\): torna a t exata</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Aula 5</small>Não viesado × consistente</div><div class="face back">Não viesado: \\(E(\\hat\\beta_1)=\\beta_1\\) com n fixo. Consistente: \\(\\text{plim}\\,\\hat\\beta_1=\\beta_1\\) quando n → ∞</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Aula 5</small>Precisão × eficiência</div><div class="face back">Precisão: dispersão de um estimador. Eficiência: comparar estimadores (menor variância)</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Aula 5</small>BLUE</div><div class="face back">Best Linear Unbiased Estimator: menor variância entre lineares não viesados (Gauss–Markov)</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Prática 4–5</small>Variável omitida</div><div class="face back">Estima-se \\(\\beta_1+\\) (efeito de Z em Y) × (inclinação de Z em X): 0,8 + 1,2 × 0,7 = 1,64</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Prática 4–5</small>Erro de medida em X</div><div class="face back">Atenuação: a inclinação vai para zero</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Aula 6</small>Erro tipo I × tipo II</div><div class="face back">I: rejeitar H₀ verdadeira (α). II: não rejeitar H₀ falsa (β)</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Aula 6</small>p-valor</div><div class="face back">P(estatística tão ou mais extrema | H₀). Não é P(H₀)</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Aula 6</small>Robusto</div><div class="face back">Corrige a incerteza sob heterocedasticidade; não corrige viés</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Log</small>\\(\\ln(ab)\\) e \\(\\ln(a^b)\\)</div><div class="face back">\\(\\ln a+\\ln b\\) e \\(b\\ln a\\)</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Log</small>Exato no log–nível</div><div class="face back">\\(100(e^{\\beta_1\\Delta x}-1)\\%\\)</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Derivada</small>Regra da cadeia</div><div class="face back">\\([f(g(x))]'=f'(g(x))\\cdot g'(x)\\)</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Derivada</small>Máximo ou mínimo?</div><div class="face back">\\(f'=0\\); \\(f''\\lt0\\) máximo, \\(f''&gt;0\\) mínimo</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>Integral</small>Teorema Fundamental</div><div class="face back">\\(\\int_a^bf=F(b)-F(a)\\), com \\(F'=f\\)</div></div></div>
    <div class="flash" role="button" tabindex="0"><div class="inner"><div class="face"><small>λ</small>Multiplicador de Lagrange</div><div class="face back">\\(\\lambda=df^*/dc\\): quanto o ótimo muda se a restrição afrouxa 1 unidade</div></div></div>
  </div>
  <div class="quiz" data-answer="c"><div class="qh">Unidades</div>
    <p>y é o salário mensal em reais e x são anos de experiência. A unidade de \\(ep(\\hat\\beta_1)\\) é:</p>
    <div class="opts"><button data-k="a">a) reais</button><button data-k="b">b) anos</button><button data-k="c">c) reais por ano de experiência</button><button data-k="d">d) sem unidade</button></div>
    <div class="fb" hidden>O erro-padrão tem a mesma unidade do coeficiente que ele mede. Por isso t = coeficiente ÷ ep não tem unidade.</div></div>
  <div class="quiz" data-answer="a"><div class="qh">Unidades</div>
    <p>Se x está em metros e y em reais, qual é a unidade de \\(SQT_x\\)?</p>
    <div class="opts"><button data-k="a">a) metros ao quadrado</button><button data-k="b">b) reais ao quadrado</button><button data-k="c">c) reais por metro</button><button data-k="d">d) sem unidade</button></div>
    <div class="fb" hidden>\\(SQT_x=\\sum(x_i-\\bar x)^2\\) soma desvios de x ao quadrado. SQT (sem o x) seria em reais ao quadrado.</div></div>
  <div class="done-row"><button class="btn done-btn" data-done="dicionario" aria-pressed="false">Marcar como concluído</button></div>
</section>
''')
open(OUT,"w").write("\n".join(out))
print("entries:",len(E),"groups:",len(groups))

import { useScrollReveal } from '../hooks/useScrollReveal'

function NeuralNetwork() {
  return (
    <div className="relative w-full h-80 md:h-full min-h-[320px]">
      {/* Animated orbs */}
      {[
        { size: 80, top: '10%', left: '20%', delay: '0s', color: 'from-neon-blue/30 to-neon-cyan/10' },
        { size: 60, top: '50%', left: '60%', delay: '2s', color: 'from-neon-violet/30 to-neon-blue/10' },
        { size: 50, top: '30%', left: '45%', delay: '4s', color: 'from-neon-cyan/30 to-neon-violet/10' },
        { size: 40, top: '70%', left: '25%', delay: '1s', color: 'from-neon-blue/20 to-transparent' },
        { size: 35, top: '20%', left: '75%', delay: '3s', color: 'from-neon-violet/20 to-transparent' },
        { size: 45, top: '65%', left: '70%', delay: '5s', color: 'from-neon-cyan/25 to-transparent' },
      ].map((orb, i) => (
        <div
          key={i}
          className={`absolute rounded-full bg-gradient-to-br ${orb.color} border border-white/10`}
          style={{
            width: orb.size,
            height: orb.size,
            top: orb.top,
            left: orb.left,
            animation: `float ${6 + i * 2}s ease-in-out infinite ${orb.delay}`,
          }}
        >
          <div className="absolute inset-2 rounded-full bg-white/5 backdrop-blur-sm" />
        </div>
      ))}

      {/* Connection lines via SVG */}
      <svg className="absolute inset-0 w-full h-full" style={{ opacity: 0.15 }}>
        <line x1="25%" y1="15%" x2="50%" y2="35%" stroke="url(#line-grad)" strokeWidth="1">
          <animate attributeName="opacity" values="0.3;0.8;0.3" dur="3s" repeatCount="indefinite" />
        </line>
        <line x1="50%" y1="35%" x2="65%" y2="55%" stroke="url(#line-grad)" strokeWidth="1">
          <animate attributeName="opacity" values="0.5;1;0.5" dur="4s" repeatCount="indefinite" />
        </line>
        <line x1="65%" y1="55%" x2="30%" y2="75%" stroke="url(#line-grad)" strokeWidth="1">
          <animate attributeName="opacity" values="0.2;0.7;0.2" dur="3.5s" repeatCount="indefinite" />
        </line>
        <line x1="30%" y1="75%" x2="75%" y2="70%" stroke="url(#line-grad)" strokeWidth="1">
          <animate attributeName="opacity" values="0.4;0.9;0.4" dur="5s" repeatCount="indefinite" />
        </line>
        <line x1="80%" y1="25%" x2="50%" y2="35%" stroke="url(#line-grad)" strokeWidth="1">
          <animate attributeName="opacity" values="0.3;0.6;0.3" dur="4.5s" repeatCount="indefinite" />
        </line>
        <defs>
          <linearGradient id="line-grad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#3b82f6" />
            <stop offset="100%" stopColor="#06b6d4" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  )
}

export default function About() {
  const sectionRef = useScrollReveal()

  return (
    <section id="sobre" className="relative py-24 sm:py-32 px-6" ref={sectionRef}>
      <div className="max-w-7xl mx-auto relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Left column */}
          <div>
            <div className="scroll-reveal mb-12">
              <h2 className="font-[Sora] text-3xl sm:text-4xl font-bold text-white tracking-tight mb-6">
                O que <span className="gradient-text">Fazemos</span>
              </h2>
              <p className="text-white/50 text-base leading-relaxed">
                Desenvolvemos soluções de automação empresarial usando IA (Inteligência Artificial) e RPA (Automação Robótica de Processos) para atendimento inteligente 24/7, prospecção e qualificação de leads (SDR), otimizar vendas, análise de dados, automações de marketing e tráfego, além de operações internas diversas como agendamentos, envio de notificações e lembretes, financeiro, cobranças, recrutamento e seleção, etc.
              </p>
            </div>

            <div className="scroll-reveal">
              <h2 className="font-[Sora] text-3xl sm:text-4xl font-bold text-white tracking-tight mb-6">
                Para quem <span className="gradient-text">Fazemos</span>
              </h2>
              <p className="text-white/50 text-base leading-relaxed">
                Empresas com equipes enxutas, que desejam eliminar tarefas manuais, implementar novos departamentos, escalar processos e aumentar a lucratividade sem aumentar os custos com equipe e mão de obra.
              </p>
            </div>
          </div>

          {/* Right column - Neural Network */}
          <div className="scroll-reveal">
            <NeuralNetwork />
          </div>
        </div>

        {/* Separator */}
        <div className="mt-24 h-px bg-gradient-to-r from-transparent via-neon-blue/30 to-transparent" />
      </div>
    </section>
  )
}

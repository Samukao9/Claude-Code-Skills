import { useScrollReveal } from '../hooks/useScrollReveal'
import { CheckCircle2 } from 'lucide-react'

const props = [
  {
    title: 'Redução de custos operacionais e de mão de obra',
    desc: 'Aumento na produtividade sem precisar contratar mais funcionários.',
  },
  {
    title: 'Atendimento mais rápido e eficiente para seus clientes',
    desc: 'Gestão automatizada de vendas, marketing e suporte técnico.',
  },
  {
    title: 'Análises de dados e insights estratégicos em tempo real',
    desc: 'Mais clareza e assertividade nas tomadas de decisão, mais economia e aumento do faturamento.',
  },
]

export default function Benefits() {
  const sectionRef = useScrollReveal()

  return (
    <section id="beneficios" className="relative py-24 sm:py-32 px-6" ref={sectionRef}>
      <div className="orb orb-cyan w-[500px] h-[500px] top-0 left-1/4 opacity-10" />

      <div className="max-w-7xl mx-auto relative z-10">
        <div className="text-center mb-16">
          <h2 className="scroll-reveal font-[Sora] text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-tight mb-6">
            Automação inteligente para{' '}
            <span className="gradient-text">maximizar eficiência</span>
          </h2>
          <p className="scroll-reveal text-white/50 text-lg max-w-3xl mx-auto">
            Nosso serviço full-time garante que sua operação esteja sempre rodando no máximo desempenho, com suporte, monitoramento e melhorias contínuas.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {props.map((prop, i) => (
            <div
              key={i}
              className="scroll-reveal glass-card p-10 group text-center"
              style={{ transitionDelay: `${i * 100}ms` }}
            >
              <div className="w-16 h-16 rounded-2xl glass flex items-center justify-center mx-auto mb-8 group-hover:shadow-[0_0_40px_rgba(6,182,212,0.3)] transition-all duration-500">
                <CheckCircle2 size={28} className="text-neon-cyan-light" />
              </div>
              <h3 className="font-[Sora] text-xl font-semibold text-white mb-4 leading-snug">
                {prop.title}
              </h3>
              <p className="text-white/40 text-base leading-relaxed">{prop.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

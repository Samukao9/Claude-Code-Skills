import { useScrollReveal } from '../hooks/useScrollReveal'
import { CircleDot, Network, GitFork, ArrowRight } from 'lucide-react'

const services = [
  {
    icon: CircleDot,
    title: 'Agentes Autônomos de IA',
    desc: 'Essa solução entrega automação confiável que impulsiona o desempenho do seu negócio.',
    details: null,
  },
  {
    icon: Network,
    title: 'Automação Inteligente',
    desc: 'Personalizamos soluções tecnológicas para otimizar processos e maximizar resultados.',
    details:
      'Atendimento 24/7, prospecção e qualificação de leads (SDR), vendas, análise de dados, automações de marketing e tráfego, agendamentos, notificações e lembretes, financeiro, cobranças, recrutamento e seleção.',
  },
  {
    icon: GitFork,
    title: 'Consultoria Tech',
    desc: 'Criado para resolver desafios únicos e proporcionar eficiência personalizada.',
    details: null,
  },
]

export default function Solutions() {
  const sectionRef = useScrollReveal()

  return (
    <section id="solucoes" className="relative py-24 sm:py-32 px-6" ref={sectionRef}>
      <div className="orb orb-blue w-[600px] h-[600px] -bottom-40 right-0 opacity-15" />
      <div className="orb orb-violet w-[400px] h-[400px] top-20 -left-20 opacity-10" />

      <div className="max-w-7xl mx-auto relative z-10">
        <div className="text-center mb-16">
          <h2 className="scroll-reveal font-[Sora] text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-tight mb-6">
            Revolucione sua empresa com{' '}
            <span className="gradient-text">automação inteligente</span>
          </h2>
          <p className="scroll-reveal text-white/50 text-lg max-w-3xl mx-auto">
            Explore nossa gama de serviços especializados, projetados para aumentar a eficiência e garantir sua satisfação.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {services.map((service, i) => (
            <div
              key={i}
              className="scroll-reveal glass-card p-10 group flex flex-col"
              style={{ transitionDelay: `${i * 150}ms` }}
            >
              {/* Animated icon */}
              <div className="w-16 h-16 rounded-2xl glass flex items-center justify-center mb-8 relative">
                <service.icon size={28} className="text-neon-blue-light relative z-10" />
                <div className="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-500 bg-gradient-to-br from-neon-blue/20 to-neon-cyan/10" />
              </div>

              <h3 className="font-[Sora] text-2xl font-semibold text-white mb-4">
                {service.title}
              </h3>
              <p className="text-white/50 text-base leading-relaxed mb-4">{service.desc}</p>
              {service.details && (
                <p className="text-white/30 text-sm leading-relaxed mb-6">{service.details}</p>
              )}

              <div className="mt-auto">
                <button className="inline-flex items-center gap-2 text-neon-blue-light hover:text-neon-cyan-light transition-colors text-sm font-medium group/btn">
                  Saiba mais
                  <ArrowRight size={16} className="group-hover/btn:translate-x-1 transition-transform" />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

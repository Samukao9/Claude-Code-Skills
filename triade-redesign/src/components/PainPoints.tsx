import { useScrollReveal } from '../hooks/useScrollReveal'
import { Clock, TrendingDown, Filter, Settings, MessageCircleX, Rocket } from 'lucide-react'
import { useRef, type MouseEvent } from 'react'

const pains = [
  {
    icon: Clock,
    title: 'Sua equipe perde tempo com tarefas manuais e repetitivas',
    sub: 'que poderiam ser automatizadas',
  },
  {
    icon: TrendingDown,
    title: 'O custo operacional só aumenta',
    sub: 'mas a produtividade e os lucros não acompanham o ritmo',
  },
  {
    icon: Filter,
    title: 'Os leads chegam, mas muitos se perdem',
    sub: 'por falta de resposta rápida e qualificação adequada',
  },
  {
    icon: Settings,
    title: 'Os processos internos são burocráticos e demorados',
    sub: 'atrasando vendas e impactando a experiência do cliente',
  },
  {
    icon: MessageCircleX,
    title: 'O atendimento ao cliente é demorado ou ineficiente',
    sub: 'gerando insatisfação e reduzindo taxas de conversão',
  },
  {
    icon: Rocket,
    title: 'A tecnologia da empresa não acompanha o crescimento do negócio',
    sub: 'dificultando a escalabilidade',
  },
]

function TiltCard({ children, className }: { children: React.ReactNode; className?: string }) {
  const cardRef = useRef<HTMLDivElement>(null)

  const handleMouseMove = (e: MouseEvent) => {
    const card = cardRef.current
    if (!card) return
    const rect = card.getBoundingClientRect()
    const x = e.clientX - rect.left
    const y = e.clientY - rect.top
    const centerX = rect.width / 2
    const centerY = rect.height / 2
    const rotateX = ((y - centerY) / centerY) * -8
    const rotateY = ((x - centerX) / centerX) * 8
    card.style.transform = `perspective(800px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.02)`
  }

  const handleMouseLeave = () => {
    const card = cardRef.current
    if (card) card.style.transform = 'perspective(800px) rotateX(0) rotateY(0) scale(1)'
  }

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
      className={className}
      style={{ transition: 'transform 0.3s cubic-bezier(0.22, 1, 0.36, 1)' }}
    >
      {children}
    </div>
  )
}

export default function PainPoints() {
  const sectionRef = useScrollReveal()

  return (
    <section id="problema" className="relative py-24 sm:py-32 px-6" ref={sectionRef}>
      <div className="orb orb-violet w-[500px] h-[500px] -top-40 right-0 opacity-15" />

      <div className="max-w-7xl mx-auto relative z-10">
        <div className="text-center mb-16">
          <h2 className="scroll-reveal font-[Sora] text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-tight mb-6">
            Sua empresa poderia crescer mais, mas algo está{' '}
            <span className="relative inline-block">
              <span className="gradient-text">travando</span>
              <span className="absolute -bottom-1 left-0 right-0 h-1 bg-gradient-to-r from-neon-blue to-neon-cyan rounded-full" style={{ animation: 'glow-ring 2s ease-in-out infinite' }} />
            </span>
            ?
          </h2>
          <p className="scroll-reveal text-white/50 text-lg max-w-3xl mx-auto mb-4">
            Você já sentiu que, apesar dos esforços, sua empresa ainda enfrenta desafios que impedem um crescimento mais rápido e eficiente?
          </p>
          <p className="scroll-reveal text-white/40 text-base max-w-2xl mx-auto">
            Veja se alguma dessas situações lhe parece familiar:
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {pains.map((pain, i) => (
            <TiltCard
              key={i}
              className="scroll-reveal glass-card p-8 group cursor-default"
            >
              <div className="w-14 h-14 rounded-2xl glass flex items-center justify-center mb-6 group-hover:shadow-[0_0_30px_rgba(59,130,246,0.3)] transition-all duration-500">
                <pain.icon size={24} className="text-neon-blue-light" />
              </div>
              <h3 className="font-[Sora] text-lg font-semibold text-white mb-2 leading-snug">
                {pain.title}
              </h3>
              <p className="text-white/40 text-sm leading-relaxed">{pain.sub}</p>
            </TiltCard>
          ))}
        </div>
      </div>
    </section>
  )
}

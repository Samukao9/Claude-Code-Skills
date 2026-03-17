import { useRef, useState, useEffect } from 'react'
import { useScrollReveal } from '../hooks/useScrollReveal'
import { ChevronLeft, ChevronRight, GraduationCap, Calculator, Stethoscope, ShoppingCart, Truck, Home, Scale } from 'lucide-react'

const cases = [
  { icon: GraduationCap, name: 'Escolas Particulares e Públicas', desc: 'Automatize matrículas, comunicação com pais, gestão de notas e agendamentos escolares.' },
  { icon: Calculator, name: 'Escritórios de Contabilidade', desc: 'Otimize processos fiscais, envio de documentos, lembretes de prazos e atendimento ao cliente.' },
  { icon: Stethoscope, name: 'Clínicas de Especialidades', desc: 'Agendamento inteligente, lembretes de consultas, triagem inicial e gestão de prontuários.' },
  { icon: ShoppingCart, name: 'E-commerces e Lojas Virtuais', desc: 'Automação de atendimento, recuperação de carrinhos, gestão de pedidos e marketing personalizado.' },
  { icon: Truck, name: 'Empresas de Logística e Transporte', desc: 'Rastreamento automatizado, notificações de entrega, gestão de frotas e otimização de rotas.' },
  { icon: Home, name: 'Imobiliárias e Construtoras', desc: 'Qualificação de leads, agendamento de visitas, acompanhamento de vendas e pós-venda.' },
  { icon: Scale, name: 'Escritórios de Advocacia', desc: 'Gestão de prazos processuais, atendimento inicial automatizado e organização documental.' },
]

export default function UseCases() {
  const sectionRef = useScrollReveal()
  const scrollRef = useRef<HTMLDivElement>(null)
  const [canScrollLeft, setCanScrollLeft] = useState(false)
  const [canScrollRight, setCanScrollRight] = useState(true)
  const autoPlayRef = useRef<ReturnType<typeof setInterval>>()
  const isPaused = useRef(false)

  const checkScroll = () => {
    const el = scrollRef.current
    if (!el) return
    setCanScrollLeft(el.scrollLeft > 10)
    setCanScrollRight(el.scrollLeft < el.scrollWidth - el.clientWidth - 10)
  }

  const scroll = (dir: 'left' | 'right') => {
    const el = scrollRef.current
    if (!el) return
    const cardWidth = 340
    el.scrollBy({ left: dir === 'left' ? -cardWidth : cardWidth, behavior: 'smooth' })
  }

  useEffect(() => {
    const el = scrollRef.current
    if (!el) return
    el.addEventListener('scroll', checkScroll, { passive: true })
    checkScroll()

    autoPlayRef.current = setInterval(() => {
      if (isPaused.current) return
      if (!canScrollRight) {
        el.scrollTo({ left: 0, behavior: 'smooth' })
      } else {
        scroll('right')
      }
    }, 4000)

    return () => {
      el.removeEventListener('scroll', checkScroll)
      clearInterval(autoPlayRef.current)
    }
  }, [canScrollRight])

  return (
    <section id="cases" className="relative py-24 sm:py-32 px-6" ref={sectionRef}>
      <div className="max-w-7xl mx-auto relative z-10">
        <div className="flex items-end justify-between mb-12">
          <h2 className="scroll-reveal font-[Sora] text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-tight">
            Casos de <span className="gradient-text">Uso</span>
          </h2>
          <div className="hidden sm:flex gap-3">
            <button
              onClick={() => scroll('left')}
              disabled={!canScrollLeft}
              className="w-12 h-12 rounded-full glass flex items-center justify-center text-white/60 hover:text-white disabled:opacity-30 transition-all"
            >
              <ChevronLeft size={20} />
            </button>
            <button
              onClick={() => scroll('right')}
              disabled={!canScrollRight}
              className="w-12 h-12 rounded-full glass flex items-center justify-center text-white/60 hover:text-white disabled:opacity-30 transition-all"
            >
              <ChevronRight size={20} />
            </button>
          </div>
        </div>

        <div
          ref={scrollRef}
          onMouseEnter={() => (isPaused.current = true)}
          onMouseLeave={() => (isPaused.current = false)}
          className="flex gap-6 overflow-x-auto pb-4 scrollbar-hide snap-x snap-mandatory"
          style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
        >
          {cases.map((c, i) => (
            <div
              key={i}
              className="glass-card p-8 min-w-[300px] sm:min-w-[340px] flex-shrink-0 snap-start group"
            >
              <div className="w-14 h-14 rounded-2xl glass flex items-center justify-center mb-6 group-hover:shadow-[0_0_30px_rgba(139,92,246,0.3)] transition-all duration-500">
                <c.icon size={24} className="text-neon-violet-light" />
              </div>
              <h3 className="font-[Sora] text-lg font-semibold text-white mb-3">{c.name}</h3>
              <p className="text-white/40 text-sm leading-relaxed">{c.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

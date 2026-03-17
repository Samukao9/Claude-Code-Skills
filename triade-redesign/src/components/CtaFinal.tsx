import { useScrollReveal } from '../hooks/useScrollReveal'
import { MessageCircle } from 'lucide-react'

export default function CtaFinal() {
  const sectionRef = useScrollReveal()

  return (
    <section id="cta_final" className="relative py-24 sm:py-32 px-6 overflow-hidden" ref={sectionRef}>
      {/* Intense background */}
      <div className="absolute inset-0 bg-gradient-to-br from-neon-blue/10 via-deep-900 to-neon-violet/10" />
      <div className="orb orb-blue w-[600px] h-[600px] -top-40 -left-40 opacity-25" style={{ animation: 'float-slow 12s ease-in-out infinite' }} />
      <div className="orb orb-violet w-[500px] h-[500px] -bottom-40 -right-40 opacity-25" style={{ animation: 'float-slow 15s ease-in-out infinite 3s' }} />
      <div className="orb orb-cyan w-[400px] h-[400px] top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-15" style={{ animation: 'float 10s ease-in-out infinite' }} />

      <div className="max-w-4xl mx-auto relative z-10 text-center">
        <h2 className="scroll-reveal font-[Sora] text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-white tracking-tight mb-6">
          Impulsione resultados com{' '}
          <span className="gradient-text">inteligência autônoma</span>
        </h2>
        <p className="scroll-reveal text-white/50 text-lg sm:text-xl max-w-2xl mx-auto mb-12">
          Descubra como transformar sua empresa com soluções inteligentes e inove agora mesmo.
        </p>

        <div className="scroll-reveal flex flex-col sm:flex-row items-center justify-center gap-4">
          <a
            href="https://calendly.com/contato-triadetecnologiaesolucoes/45min"
            target="_blank"
            rel="noopener noreferrer"
            className="px-10 py-5 rounded-full bg-gradient-to-r from-neon-blue to-neon-cyan text-white font-semibold text-lg btn-ripple cta-pulse transition-all duration-300 hover:scale-105"
          >
            Agendar Demonstração
          </a>
          <button className="px-10 py-5 rounded-full glass text-white/80 hover:text-white font-semibold text-lg transition-all duration-300 hover:scale-105 inline-flex items-center gap-3">
            <MessageCircle size={20} />
            Converse com Nosso Agente de IA
          </button>
        </div>
      </div>
    </section>
  )
}

import { ChevronDown } from 'lucide-react'

export default function Hero() {
  return (
    <section id="hero" className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 grid-pattern" />
      <div className="orb orb-blue w-[600px] h-[600px] -top-40 -left-40 opacity-30" style={{ animation: 'float-slow 15s ease-in-out infinite' }} />
      <div className="orb orb-violet w-[500px] h-[500px] top-1/3 -right-32 opacity-25" style={{ animation: 'float-slow 18s ease-in-out infinite 3s' }} />
      <div className="orb orb-cyan w-[400px] h-[400px] bottom-0 left-1/3 opacity-20" style={{ animation: 'float-slow 20s ease-in-out infinite 6s' }} />

      <div className="relative z-10 max-w-5xl mx-auto px-6 text-center pt-24 pb-32">
        {/* Badge */}
        <div
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-full glass mb-10 text-sm text-white/70"
          style={{ animation: 'badge-float 3s ease-in-out infinite' }}
        >
          <span>🤖</span>
          <span>Agentes de IA Autônomos</span>
          <span className="w-1 h-1 rounded-full bg-white/30" />
          <span>Trabalhando 24/7 por você</span>
        </div>

        {/* Heading */}
        <h1 className="font-[Sora] text-4xl sm:text-5xl md:text-6xl lg:text-7xl font-bold tracking-tight leading-[1.1] mb-8">
          <span className="text-white">Soluções de </span>
          <span className="gradient-text">Inteligência Artificial</span>
          <span className="text-white"> para automatizar e escalar seu negócio</span>
        </h1>

        {/* Subtitle */}
        <p className="text-lg sm:text-xl text-white/50 max-w-3xl mx-auto mb-6 leading-relaxed">
          Você se sente sobrecarregado, com equipe enxuta e não consegue fazer sua empresa crescer por falta de recursos e mão de obra?
        </p>

        {/* Support text */}
        <p className="text-base sm:text-lg text-white/40 max-w-2xl mx-auto mb-12 leading-relaxed">
          Reduza custos operacionais e aumente suas vendas com um exército de Agentes Autônomos de IA avançada trabalhando pra você.
        </p>

        {/* CTAs */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <a
            href="#solucoes"
            className="px-8 py-4 rounded-full bg-gradient-to-r from-neon-blue to-neon-cyan text-white font-semibold text-lg btn-ripple cta-pulse transition-all duration-300 hover:scale-105"
          >
            Explorar Soluções
          </a>
          <a
            href="https://calendly.com/contato-triadetecnologiaesolucoes/45min"
            target="_blank"
            rel="noopener noreferrer"
            className="px-8 py-4 rounded-full glass text-white/80 hover:text-white font-semibold text-lg transition-all duration-300 hover:scale-105"
          >
            Agendar Demonstração
          </a>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 flex flex-col items-center gap-2 text-white/30">
        <span className="text-xs tracking-widest uppercase">Scroll</span>
        <ChevronDown size={20} style={{ animation: 'scroll-down 2s ease-in-out infinite' }} />
      </div>
    </section>
  )
}

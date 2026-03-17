import { useScrollReveal } from '../hooks/useScrollReveal'
import { ArrowRight } from 'lucide-react'

const articles = [
  {
    title: 'As 5 Maiores Mentiras sobre Inteligência Artificial e Automação Empresarial',
    excerpt: 'E a Verdade que Ninguém Conta! Desmistificamos os principais mitos sobre IA e automação no mundo dos negócios.',
    categories: ['Automações', 'Inteligência Artificial'],
    gradient: 'from-neon-blue/20 via-neon-cyan/10 to-neon-violet/20',
  },
  {
    title: 'Como soluções inteligentes promovem transformação digital',
    excerpt: 'A transformação digital deixou de ser uma tendência para se tornar uma necessidade estratégica.',
    categories: ['Automações', 'Casos de Uso', 'Inteligência Artificial'],
    gradient: 'from-neon-violet/20 via-neon-blue/10 to-neon-cyan/20',
  },
]

export default function Articles() {
  const sectionRef = useScrollReveal()

  return (
    <section id="artigos" className="relative py-24 sm:py-32 px-6" ref={sectionRef}>
      <div className="max-w-7xl mx-auto relative z-10">
        <div className="text-center mb-16">
          <h2 className="scroll-reveal font-[Sora] text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-tight mb-6">
            Artigos & <span className="gradient-text">Novidades</span>
          </h2>
          <p className="scroll-reveal text-white/40 text-base max-w-3xl mx-auto leading-relaxed">
            Explore nossa seção de Artigos & Novidades e fique sabendo tudo o que acontece no mundo das Automações e os avanços da Inteligência Artificial. Descubra informações detalhadas, insights inovadores e recursos práticos para transformar sua visão sobre automação inteligente e IA.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {articles.map((article, i) => (
            <div
              key={i}
              className="scroll-reveal glass-card overflow-hidden group cursor-pointer"
              style={{ transitionDelay: `${i * 150}ms` }}
            >
              {/* Placeholder image area */}
              <div className={`h-48 sm:h-56 bg-gradient-to-br ${article.gradient} relative overflow-hidden`}>
                <div className="absolute inset-0 grid-pattern opacity-50" />
                <div className="absolute bottom-4 left-6 flex gap-2">
                  {article.categories.map((cat) => (
                    <span key={cat} className="px-3 py-1 rounded-full glass text-xs text-white/70 font-medium">
                      {cat}
                    </span>
                  ))}
                </div>
              </div>

              <div className="p-8">
                <h3 className="font-[Sora] text-xl font-semibold text-white mb-3 leading-snug group-hover:text-neon-blue-light transition-colors">
                  {article.title}
                </h3>
                <p className="text-white/40 text-sm leading-relaxed mb-4">{article.excerpt}</p>
                <span className="inline-flex items-center gap-2 text-neon-blue-light text-sm font-medium group-hover:gap-3 transition-all">
                  Leia mais <ArrowRight size={14} />
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

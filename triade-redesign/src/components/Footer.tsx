import { Facebook, Instagram, Linkedin, Youtube, Twitter } from 'lucide-react'

const socialLinks = [
  { icon: Facebook, href: 'https://www.facebook.com/', label: 'Facebook' },
  { icon: Instagram, href: 'https://www.instagram.com/', label: 'Instagram' },
  { icon: Linkedin, href: 'https://www.linkedin.com/', label: 'LinkedIn' },
  { icon: Youtube, href: 'https://www.youtube.com/', label: 'YouTube' },
  { icon: Twitter, href: 'https://twitter.com/', label: 'X (Twitter)' },
]

const columns = [
  {
    title: 'Produtos',
    links: ['Product Overview', 'Pricing Plans', 'Product Support', 'Product FAQ'],
  },
  {
    title: 'Artigos',
    links: ['Blog', 'Cases de Uso', 'Whitepapers', 'Industry Insights', 'Novidades', 'Webinars'],
  },
  {
    title: 'Sobre',
    links: ['Sobre Nós', 'Nosso Time', 'Carreiras', 'Prêmios', 'Depoimentos', 'Contato'],
  },
]

// TikTok icon (not available in lucide-react)
function TikTokIcon({ size = 20 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 12a4 4 0 1 0 4 4V4a5 5 0 0 0 5 5" />
    </svg>
  )
}

export default function Footer() {
  return (
    <footer className="relative bg-deep-900/50 border-t border-white/5 pt-16 pb-8 px-6">
      <div className="max-w-7xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 mb-16">
          {/* Brand column */}
          <div>
            <a href="#hero" className="font-[Sora] text-xl font-bold tracking-tight inline-block mb-6">
              <span className="gradient-text">Tríade</span>
              <span className="text-white/80 ml-1">IA</span>
            </a>
            <p className="text-white/40 text-sm leading-relaxed mb-8">
              Somos uma agência especializada em automação IA, oferecendo soluções sob demanda para empresas que querem crescer sem aumentar custos com equipe. Nosso serviço full-time garante que sua operação esteja sempre rodando no máximo desempenho, com suporte, monitoramento e melhorias contínuas.
            </p>
            <div className="flex gap-3">
              {socialLinks.map(({ icon: Icon, href, label }) => (
                <a
                  key={label}
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={label}
                  className="w-10 h-10 rounded-xl glass flex items-center justify-center text-white/40 hover:text-white hover:shadow-[0_0_20px_rgba(59,130,246,0.2)] transition-all duration-300"
                >
                  <Icon size={18} />
                </a>
              ))}
              <a
                href="https://www.tiktok.com/"
                target="_blank"
                rel="noopener noreferrer"
                aria-label="TikTok"
                className="w-10 h-10 rounded-xl glass flex items-center justify-center text-white/40 hover:text-white hover:shadow-[0_0_20px_rgba(59,130,246,0.2)] transition-all duration-300"
              >
                <TikTokIcon size={18} />
              </a>
            </div>
          </div>

          {/* Link columns */}
          {columns.map((col) => (
            <div key={col.title}>
              <h4 className="font-[Sora] text-sm font-semibold text-white mb-6 uppercase tracking-wider">
                {col.title}
              </h4>
              <ul className="space-y-3">
                {col.links.map((link) => (
                  <li key={link}>
                    <a href="#" className="text-white/40 hover:text-white/70 text-sm transition-colors duration-200">
                      {link}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        {/* Copyright */}
        <div className="border-t border-white/5 pt-8 text-center">
          <p className="text-white/30 text-sm">
            © Tríade Tecnologia e Soluções 2025 | Todos os direitos reservados
          </p>
        </div>
      </div>
    </footer>
  )
}

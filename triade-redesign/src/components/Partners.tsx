import { useScrollReveal } from '../hooks/useScrollReveal'

const rows = [
  ['Google Cloud', 'AWS', 'OpenAI', 'Google Gemini', 'Microsoft Azure', 'DeepSeek'],
  ['Meta', 'Google Ads', 'HostGator', 'Bubble', 'Supabase', 'Firebase'],
  ['Twilio', 'ElevenLabs', 'HeyGen', 'WhatsApp Business', 'N8N', 'Typebot'],
  ['Evolution API', 'Figma', 'Stripe/Asaas', 'Adobe', 'Odoo', 'ClickUp'],
]

function MarqueeRow({ items, reverse, speed = 30 }: { items: string[]; reverse?: boolean; speed?: number }) {
  const doubled = [...items, ...items]

  return (
    <div className="overflow-hidden py-2">
      <div
        className="flex gap-4 w-max"
        style={{
          animation: `${reverse ? 'marquee-right' : 'marquee-left'} ${speed}s linear infinite`,
        }}
      >
        {doubled.map((item, i) => (
          <div
            key={i}
            className="glass px-6 py-3 rounded-xl text-sm font-mono font-medium text-white/50 hover:text-white hover:shadow-[0_0_20px_rgba(59,130,246,0.2)] hover:border-white/20 transition-all duration-300 whitespace-nowrap cursor-default"
          >
            {item}
          </div>
        ))}
      </div>
    </div>
  )
}

export default function Partners() {
  const sectionRef = useScrollReveal()

  return (
    <section id="parceiros" className="relative py-24 sm:py-32 overflow-hidden" ref={sectionRef}>
      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <h2 className="scroll-reveal font-[Sora] text-3xl sm:text-4xl md:text-5xl font-bold text-white tracking-tight text-center mb-16">
          Nossos Parceiros de <span className="gradient-text">Tecnologia</span>
        </h2>
      </div>

      <div className="space-y-4">
        {rows.map((row, i) => (
          <MarqueeRow key={i} items={row} reverse={i % 2 === 1} speed={25 + i * 5} />
        ))}
      </div>
    </section>
  )
}
